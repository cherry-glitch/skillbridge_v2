import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProtectedRoute({ children, requireOnboarded = true }) {
  const { profile, loading, isOnboarded } = useAuth()

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-ink/50 font-mono text-sm">loading…</div>
  }
  if (!profile) {
    return <Navigate to="/login" replace />
  }
  if (requireOnboarded && !isOnboarded) {
    return <Navigate to="/onboarding" replace />
  }
  return children
}
