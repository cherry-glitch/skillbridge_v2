import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import SkillChip from '../components/SkillChip.jsx'
import { useAuth } from '../context/AuthContext.jsx'

export default function Onboarding() {
  const { profile, setProfile } = useAuth()
  const navigate = useNavigate()
  const [branches, setBranches] = useState([])
  const [branchId, setBranchId] = useState(profile?.branch_id || '')
  const [skills, setSkills] = useState([])
  const [selectedIds, setSelectedIds] = useState(new Set((profile?.skills || []).map((s) => s.id)))
  const [step, setStep] = useState(profile?.branch_id ? 2 : 1)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/skills/branches').then(({ data }) => setBranches(data))
  }, [])

  useEffect(() => {
    if (!branchId) return
    api.get('/skills', { params: { branch: branchId } }).then(({ data }) => setSkills(data))
  }, [branchId])

  function toggleSkill(id) {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  async function chooseBranch(id) {
    setBranchId(id)
    setStep(2)
  }

  async function finish() {
    setError('')
    if (selectedIds.size === 0) {
      setError('Pick at least one skill to continue.')
      return
    }
    setBusy(true)
    try {
      await api.put('/students/me/profile', { branch_id: branchId })
      const { data } = await api.put('/students/me/skills', { skill_ids: Array.from(selectedIds) })
      setProfile(data)
      navigate('/')
    } catch {
      setError('Something went wrong saving your profile. Try again.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-lg card">
        <p className="font-display text-2xl text-brand mb-1">Set up your profile</p>
        <p className="text-ink/60 mb-6">
          {step === 1 ? "What's your branch?" : 'Pick the skills you already have — you can update this anytime.'}
        </p>

        {step === 1 && (
          <div className="grid grid-cols-2 gap-3">
            {branches.map((b) => (
              <button
                key={b.id}
                onClick={() => chooseBranch(b.id)}
                className="text-left border border-line rounded-md p-4 hover:border-brand transition-colors"
              >
                <p className="font-medium">{b.name}</p>
                <p className="text-xs text-ink/40 uppercase mt-1">{b.id}</p>
              </button>
            ))}
          </div>
        )}

        {step === 2 && (
          <>
            <div className="flex flex-wrap gap-2 mb-6">
              {skills.map((s) => (
                <SkillChip
                  key={s.id}
                  label={s.name}
                  selected={selectedIds.has(s.id)}
                  onClick={() => toggleSkill(s.id)}
                />
              ))}
              {skills.length === 0 && <p className="text-sm text-ink/40">Loading skills…</p>}
            </div>
            {error && <p className="text-sm text-accent mb-3">{error}</p>}
            <div className="flex items-center gap-3">
              <button onClick={() => setStep(1)} className="btn-secondary">Back</button>
              <button onClick={finish} disabled={busy} className="btn-primary">
                {busy ? 'Saving…' : 'Finish setup'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
