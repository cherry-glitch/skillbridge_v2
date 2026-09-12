export default function InternshipCard({ internship, matchInfo, onApply, applying, applied }) {
  const score = matchInfo?.score
  const eligible = matchInfo ? matchInfo.is_eligible : true
  const matchedSet = new Set(matchInfo?.matched_skills || [])
  const missingSet = new Set(matchInfo?.missing_skills || [])

  const allSkillNames = [
    ...(internship.required_skills || []).map((s) => ({ ...s, kind: 'required' })),
    ...(internship.preferred_skills || []).map((s) => ({ ...s, kind: 'preferred' })),
  ]

  return (
    <div className="card">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="font-semibold text-lg">{internship.title}</p>
          <p className="text-ink/60 text-sm">{internship.company_name}</p>
        </div>
        {typeof score === 'number' && (
          <div className="text-right shrink-0">
            <p className={`font-display text-2xl ${eligible ? 'text-brand' : 'text-ink/30'}`}>{score}%</p>
            <p className="text-xs text-ink/40">{eligible ? 'match' : 'not eligible'}</p>
          </div>
        )}
      </div>

      <p className="text-sm text-ink/70 mt-3">{internship.description}</p>

      {allSkillNames.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-4">
          {allSkillNames.map((s) => (
            <span
              key={`${s.kind}-${s.id}`}
              className={`text-xs px-2.5 py-1 rounded-full border ${
                matchedSet.has(s.id)
                  ? 'border-brand text-brand bg-brandlight'
                  : missingSet.has(s.id)
                  ? 'border-accent/40 text-accent bg-accent/5'
                  : 'border-line text-ink/50'
              }`}
            >
              {s.name}{s.kind === 'preferred' ? ' (preferred)' : ''}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between mt-4">
        <p className="text-xs text-ink/40">Eligible: {internship.eligible_branches.toUpperCase()}</p>
        {onApply && (
          <button onClick={onApply} disabled={applying || applied || !eligible} className="btn-secondary text-sm px-4 py-2">
            {applied ? 'Applied' : applying ? 'Applying…' : eligible ? 'Apply' : 'Not eligible'}
          </button>
        )}
      </div>
    </div>
  )
}
