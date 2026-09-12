import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../api'

const AuthContext = createContext(null)
const TOKEN_KEY = 'skillbridge_token'

export function AuthProvider({ children }) {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadProfile = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) {
      setLoading(false)
      return
    }
    try {
      const { data } = await api.get('/students/me')
      setProfile(data)
    } catch {
      localStorage.removeItem(TOKEN_KEY)
      setProfile(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadProfile()
  }, [loadProfile])

  async function register(email, password) {
    await api.post('/auth/register', { email, password, role: 'student' })
    await login(email, password)
  }

  async function login(email, password) {
    const { data } = await api.post('/auth/login', { email, password })
    localStorage.setItem(TOKEN_KEY, data.access_token)
    await loadProfile()
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
    setProfile(null)
  }

  // True once the student has picked a branch and at least one skill —
  // used to route people through onboarding before they see the feed.
  const isOnboarded = Boolean(profile?.branch_id && profile?.skills?.length > 0)

  return (
    <AuthContext.Provider
      value={{ profile, setProfile, loading, isOnboarded, register, login, logout, refresh: loadProfile }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
