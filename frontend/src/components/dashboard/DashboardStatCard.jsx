function DashboardStatCard({
  label,
  value,
  description,
  icon,
  tone = 'default',
}) {
  return (
    <article className={`dashboard-stat-card dashboard-stat-card-${tone}`}>
      <div className="dashboard-stat-top">
        <span className="dashboard-stat-label">{label}</span>
        <span className="dashboard-stat-icon" aria-hidden="true">
          {icon}
        </span>
      </div>

      <div className="dashboard-stat-value">{value}</div>

      <p className="dashboard-stat-description">{description}</p>
    </article>
  )
}

export default DashboardStatCard