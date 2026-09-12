import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Navbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  const linkClass = ({ isActive }) =>
    `px-3 py-2 text-sm font-medium rounded-md transition-colors ${
      isActive ? 'text-brand bg-brandlight' : 'text-ink/60 hover:text-ink'
    }`

  return (
    <header className="sticky top-0 z-10 bg-surface border-b border-line">
      <div className="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
        <NavLink to="/" className="font-display text-lg text-brand">
          SkillBridge
        </NavLink>
        <nav className="flex items-center gap-1">
          <NavLink to="/" end className={linkClass}>Feed</NavLink>
          <NavLink to="/applications" className={linkClass}>Applications</NavLink>
          <NavLink to="/profile" className={linkClass}>Profile</NavLink>
          <button onClick={handleLogout} className="ml-2 px-3 py-2 text-sm text-ink/50 hover:text-ink">
            Sign out
          </button>
        </nav>
      </div>
    </header>
  )
}
