import { Link } from 'react-router-dom'

function JobCard({ job }) {
  const location = job.location || 'Location not specified'
  const employmentType = job.employment_type || 'Employment type not specified'
  const experienceLevel = job.experience_level || 'Experience level not specified'

  const salary =
    job.salary_min || job.salary_max
      ? `₹${job.salary_min?.toLocaleString('en-IN') || '—'} - ₹${job.salary_max?.toLocaleString('en-IN') || '—'}`
      : null

  return (
    <article className="job-card">
      <div className="job-card-top">
        <div className="job-company-mark" aria-hidden="true">
          {job.title?.charAt(0)?.toUpperCase() || 'J'}
        </div>

        <div className="job-card-heading">
          <h2>{job.title}</h2>

          <p>
            Hirely opportunity
            <span>•</span>
            {location}
          </p>
        </div>

        <span className="job-active-badge">
          <span />
          Active
        </span>
      </div>

      <div className="job-meta">
        <span className="job-meta-item">
          <span aria-hidden="true">◷</span>
          {employmentType}
        </span>

        <span className="job-meta-item">
          <span aria-hidden="true">◎</span>
          {experienceLevel}
        </span>

        {salary && (
          <span className="job-meta-item">
            <span aria-hidden="true">₹</span>
            {salary}
          </span>
        )}
      </div>

      <p className="job-description">
        {job.description?.length > 190
          ? `${job.description.slice(0, 190)}...`
          : job.description}
      </p>

      <div className="job-card-footer">
        <span className="job-posting-note">
          Explore this opportunity
        </span>

        <Link
          to={`/jobs/${job.id}`}
          className="job-view-button"
        >
          View opportunity
          <span aria-hidden="true">→</span>
        </Link>
      </div>
    </article>
  )
}

export default JobCard