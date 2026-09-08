import { Link } from 'react-router-dom'

function ResumeOverviewCard({ resumes, activeResume }) {
  const totalResumes = resumes.length
  const completedResumes = resumes.filter(
    (resume) => resume.parsing_status === 'COMPLETED',
  ).length

  const processingResume = resumes.find(
    (resume) => resume.parsing_status === 'PROCESSING',
  )

  const resumeReady =
    Boolean(activeResume) && activeResume.parsing_status === 'COMPLETED'

  let statusLabel = 'No active resume'
  let statusClass = 'resume-status-warning'

  if (resumeReady) {
    statusLabel = 'Ready for matching'
    statusClass = 'resume-status-success'
  } else if (processingResume) {
    statusLabel = 'Processing'
    statusClass = 'resume-status-processing'
  }

  return (
    <article className="resume-overview-card dashboard-surface">
      <div className="dashboard-section-heading">
        <div>
          <span className="dashboard-overline">RESUME CENTER</span>
          <h2>Your resume</h2>
        </div>

        <Link to="/candidate/resumes" className="dashboard-text-link">
          Manage
          <span aria-hidden="true">→</span>
        </Link>
      </div>

      {activeResume ? (
        <div className="active-resume-panel">
          <div className="resume-file-icon" aria-hidden="true">
            PDF
          </div>

          <div className="active-resume-content">
            <div className="active-resume-title-row">
              <h3>{activeResume.original_filename}</h3>

              <span className={`resume-status ${statusClass}`}>
                <span className="status-dot" />
                {statusLabel}
              </span>
            </div>

            <p>
              {activeResume.parsing_status === 'COMPLETED'
                ? 'Your structured resume data is available for AI-powered matching.'
                : 'Your resume is being prepared for AI-powered features.'}
            </p>
          </div>
        </div>
      ) : (
        <div className="resume-empty-state">
          <div className="resume-empty-icon" aria-hidden="true">
            +
          </div>

          <div>
            <h3>Add your resume</h3>
            <p>
              Upload a resume so Hirely can extract your professional
              information and prepare it for AI matching.
            </p>
          </div>

          <Link to="/candidate/resumes" className="primary-button">
            Upload Resume
          </Link>
        </div>
      )}

      <div className="resume-summary-grid">
        <div className="resume-summary-item">
          <span>Resume versions</span>
          <strong>{totalResumes}</strong>
        </div>

        <div className="resume-summary-item">
          <span>Parsed successfully</span>
          <strong>{completedResumes}</strong>
        </div>

        <div className="resume-summary-item">
          <span>Active resume</span>
          <strong>{resumeReady ? 'Yes' : 'No'}</strong>
        </div>
      </div>
    </article>
  )
}

export default ResumeOverviewCard