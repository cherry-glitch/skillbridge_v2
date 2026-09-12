import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'

const STATUS_STYLES = {
  applied: 'text-ink/60',
  shortlisted: 'text-brand',
  selected: 'text-brand',
  rejected: 'text-accent',
}

export default function Applications() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/internships/applications/me').then(({ data }) => {
      setApplications(data)
      setLoading(false)
    })
  }, [])

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="font-display text-2xl mb-1">Your applications</h1>
      <p className="text-ink/60 mb-6">Track status across everything you've applied to.</p>

      {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

      {!loading && applications.length === 0 && (
        <div className="card text-center">
          <p className="text-ink/60 mb-3">You haven't applied to anything yet.</p>
          <Link to="/" className="btn-primary inline-flex">See your feed</Link>
        </div>
      )}

      <div className="space-y-3">
        {applications.map((a) => (
          <div key={a.id} className="card flex items-center justify-between">
            <div>
              <p className="font-medium">{a.title}</p>
              <p className="text-sm text-ink/50">{a.company_name} · applied {new Date(a.applied_at).toLocaleDateString()}</p>
            </div>
            <div className="text-right">
              <p className={`text-sm font-medium capitalize ${STATUS_STYLES[a.status] || 'text-ink/60'}`}>{a.status}</p>
              <p className="text-xs text-ink/40 font-mono">{a.match_score}% match</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
