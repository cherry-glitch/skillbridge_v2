import { useEffect, useState } from 'react'
import api from '../api'
import SkillChip from '../components/SkillChip.jsx'
import { useAuth } from '../context/AuthContext.jsx'

export default function Profile() {
  const { profile, setProfile } = useAuth()
  const [branches, setBranches] = useState([])
  const [skills, setSkills] = useState([])
  const [selectedIds, setSelectedIds] = useState(new Set())
  const [editing, setEditing] = useState(false)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    api.get('/skills/branches').then(({ data }) => setBranches(data))
  }, [])

  useEffect(() => {
    if (profile?.skills) {
      setSelectedIds(new Set(profile.skills.map((s) => s.id)))
    }
  }, [profile])

  useEffect(() => {
    if (!profile?.branch_id) return
    api.get('/skills', { params: { branch: profile.branch_id } }).then(({ data }) => setSkills(data))
  }, [profile?.branch_id])

  function toggleSkill(id) {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  async function saveSkills() {
    setBusy(true)
    try {
      const { data } = await api.put('/students/me/skills', { skill_ids: Array.from(selectedIds) })
      setProfile(data)
      setEditing(false)
    } finally {
      setBusy(false)
    }
  }

  const branchName = branches.find((b) => b.id === profile?.branch_id)?.name || profile?.branch_id

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="font-display text-2xl mb-1">Your profile</h1>
      <p className="text-ink/60 mb-6">This is what employers and matching see.</p>

      <div className="card mb-6">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm text-ink/60">Profile strength</p>
          <p className="text-sm font-medium text-brand">{Math.round(profile?.readiness_score || 0)}%</p>
        </div>
        <div className="h-2 rounded-full bg-line overflow-hidden">
          <div className="h-full bg-brand rounded-full" style={{ width: `${Math.min(100, profile?.readiness_score || 0)}%` }} />
        </div>
        <p className="text-xs text-ink/40 mt-2">Add more skills to strengthen your profile.</p>
      </div>

      <div className="card mb-6">
        <p className="text-sm text-ink/60 mb-1">Branch</p>
        <p className="font-medium">{branchName || 'Not set'}</p>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-ink/60">Skills</p>
          {!editing && <button onClick={() => setEditing(true)} className="text-sm text-brand font-medium">Edit</button>}
        </div>

        {!editing && (
          <div className="flex flex-wrap gap-2">
            {(profile?.skills || []).map((s) => (
              <span key={s.id} className="chip chip-off cursor-default">{s.name}</span>
            ))}
            {(profile?.skills || []).length === 0 && <p className="text-sm text-ink/40">No skills added yet.</p>}
          </div>
        )}

        {editing && (
          <>
            <div className="flex flex-wrap gap-2 mb-4">
              {skills.map((s) => (
                <SkillChip key={s.id} label={s.name} selected={selectedIds.has(s.id)} onClick={() => toggleSkill(s.id)} />
              ))}
            </div>
            <div className="flex items-center gap-3">
              <button onClick={() => setEditing(false)} className="btn-secondary">Cancel</button>
              <button onClick={saveSkills} disabled={busy} className="btn-primary">
                {busy ? 'Saving…' : 'Save skills'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
