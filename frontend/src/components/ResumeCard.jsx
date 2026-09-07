function ResumeCard({
  resume,
  onActivate,
  onParse,
  activating,
  parsing,
}) {
  const status = resume.parsing_status?.toUpperCase()

  return (
    <div className="resume-card">
      <div className="resume-card-main">
        <div className="resume-file-icon">
          PDF
        </div>

        <div className="resume-info">
          <h3>{resume.original_filename}</h3>

          <div className="resume-meta">
            <span>
              Status: {status}
            </span>

            <span>
              {new Date(
                resume.created_at,
              ).toLocaleDateString()}
            </span>

            {resume.is_active && (
              <span className="active-badge">
                Active Resume
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="resume-actions">
        {status !== 'COMPLETED' &&
          status !== 'PROCESSING' && (
            <button
              type="button"
              className="secondary-button"
              onClick={() => onParse(resume.id)}
              disabled={parsing}
            >
              {parsing ? 'Parsing...' : 'Parse Resume'}
            </button>
          )}

        {status === 'PROCESSING' && (
          <span className="processing-text">
            Parsing in progress...
          </span>
        )}

        {!resume.is_active && (
          <button
            type="button"
            className="primary-button"
            onClick={() => onActivate(resume.id)}
            disabled={activating}
          >
            {activating
              ? 'Activating...'
              : 'Make Active'}
          </button>
        )}
      </div>
    </div>
  )
}

export default ResumeCard