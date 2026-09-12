import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      await register(email, password)
      navigate('/onboarding')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not create account. Try a different email.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-sm card">
        <p className="font-display text-2xl text-brand mb-1">Join SkillBridge</p>
        <p className="text-ink/60 mb-6">Takes a minute. Then pick your branch and skills.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm text-ink/60">Email</label>
            <input
              type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
              className="field-input mt-1" placeholder="you@college.edu"
            />
          </div>
          <div>
            <label className="text-sm text-ink/60">Password</label>
            <input
              type="password" required minLength={6} value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="field-input mt-1" placeholder="At least 6 characters"
            />
          </div>
          {error && <p className="text-sm text-accent">{error}</p>}
          <button type="submit" disabled={busy} className="btn-primary w-full">
            {busy ? 'Creating account…' : 'Create account'}
          </button>
        </form>

        <p className="text-sm text-ink/60 mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-brand font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
