import { Link } from 'react-router-dom'

function CareerHealthCard({
  profile,
  profileCompletion,
  resumeReady,
  activeResume,
}) {
  const profileReady = profileCompletion >= 80
  const careerReady = profileReady && resumeReady

  return (
    <article className="career-health-card dashboard-surface">
      <div className="dashboard-section-heading">
        <div>
          <span className="dashboard-overline">CAREER READINESS</span>
          <h2>Build a stronger profile</h2>
        </div>

        <span
          className={`readiness-badge ${
            careerReady ? 'readiness-ready' : 'readiness-progress'
          }`}
        >
          {careerReady ? 'Ready for matching' : 'In progress'}
        </span>
      </div>

      <div className="health-progress-row">
        <div className="health-progress">
          <div
            className="health-progress-fill"
            style={{ width: `${profileCompletion}%` }}
          />
        </div>

        <strong>{profileCompletion}%</strong>
      </div>

      <div className="health-checklist">
        <div className={`health-item ${profileReady ? 'is-complete' : ''}`}>
          <span className="health-item-icon">
            {profileReady ? '✓' : '1'}
          </span>

          <div>
            <strong>Complete your profile</strong>
            <p>
              {profileReady
                ? 'Your core professional information is complete.'
                : 'Add your professional details to improve your profile.'}
            </p>
          </div>

          {!profileReady && (
            <Link to="/candidate/profile" className="health-action">
              Update
            </Link>
          )}
        </div>

        <div className={`health-item ${resumeReady ? 'is-complete' : ''}`}>
          <span className="health-item-icon">
            {resumeReady ? '✓' : '2'}
          </span>

          <div>
            <strong>Activate a resume</strong>
            <p>
              {resumeReady
                ? `${activeResume?.original_filename || 'Your resume'} is ready for AI matching.`
                : 'Upload and activate a parsed resume to unlock matching.'}
            </p>
          </div>

          {!resumeReady && (
            <Link to="/candidate/resumes" className="health-action">
              Manage
            </Link>
          )}
        </div>

        <div className={`health-item ${careerReady ? 'is-complete' : ''}`}>
          <span className="health-item-icon">
            {careerReady ? '✓' : '3'}
          </span>

          <div>
            <strong>AI matching readiness</strong>
            <p>
              {careerReady
                ? 'Your profile is ready for semantic job matching.'
                : 'Complete the steps above to prepare your profile.'}
            </p>
          </div>
        </div>
      </div>
    </article>
  )
}

export default CareerHealthCard