import { useEffect, useState } from 'react'
import api from '../api'
import InternshipCard from '../components/InternshipCard.jsx'

export default function Feed() {
  const [internships, setInternships] = useState([])
  const [matchById, setMatchById] = useState({})
  const [appliedIds, setAppliedIds] = useState(new Set())
  const [applyingId, setApplyingId] = useState(null)
  const [loading, setLoading] = useState(true)

  async function load() {
    setLoading(true)
    const [internshipsRes, matchesRes, applicationsRes] = await Promise.all([
      api.get('/internships'),
      api.get('/internships/matches'),
      api.get('/internships/applications/me'),
    ])
    setInternships(internshipsRes.data)
    const matchMap = {}
    matchesRes.data.forEach((m) => { matchMap[m.internship_id] = m })
    setMatchById(matchMap)
    setAppliedIds(new Set(applicationsRes.data.map((a) => a.internship_id)))
    setLoading(false)
  }

  useEffect(() => {
    load()
  }, [])

  async function apply(internshipId) {
    setApplyingId(internshipId)
    try {
      await api.post(`/internships/${internshipId}/apply`)
      setAppliedIds((prev) => new Set(prev).add(internshipId))
    } finally {
      setApplyingId(null)
    }
  }

  const sorted = [...internships].sort((a, b) => {
    const scoreA = matchById[a.id]?.score ?? 0
    const scoreB = matchById[b.id]?.score ?? 0
    return scoreB - scoreA
  })

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="font-display text-2xl mb-1">Your feed</h1>
      <p className="text-ink/60 mb-6">Opportunities ranked by how well they fit your profile.</p>

      {loading && <p className="text-ink/50 font-mono text-sm">loading…</p>}

      <div className="space-y-4">
        {sorted.map((internship) => (
          <InternshipCard
            key={internship.id}
            internship={internship}
            matchInfo={matchById[internship.id]}
            onApply={() => apply(internship.id)}
            applying={applyingId === internship.id}
            applied={appliedIds.has(internship.id)}
          />
        ))}
        {!loading && sorted.length === 0 && (
          <p className="text-ink/50 text-sm">No opportunities posted yet — check back soon.</p>
        )}
      </div>
    </div>
  )
}
