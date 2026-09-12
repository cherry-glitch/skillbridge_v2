import Navbar from './Navbar.jsx'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-paper">
      <Navbar />
      {children}
    </div>
  )
}
