export default function SkillChip({ label, selected, onClick, disabled }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`chip ${selected ? 'chip-on' : 'chip-off'} disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      {label}
    </button>
  )
}
