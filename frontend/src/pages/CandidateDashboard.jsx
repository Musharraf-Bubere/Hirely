import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import CandidateProfileCard from '../components/CandidateProfileCard'
import { getCandidateProfile } from '../services/candidate'

function CandidateDashboard() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getCandidateProfile()

        setProfile(data)
      } catch (err) {
        if (
          !err.message
            .toLowerCase()
            .includes('not found')
        ) {
          setError(err.message)
        }
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [])

  return (
    <section className="dashboard-section">
      <div className="container dashboard-container">
        <div className="dashboard-header">
          <div>
            <span className="eyebrow">
              CANDIDATE WORKSPACE
            </span>

            <h1>
              {profile
                ? `Welcome back, ${profile.first_name}`
                : 'Welcome to Hirely'}
            </h1>

            <p>
              Manage your profile, resume, job
              applications, and AI-powered career
              journey.
            </p>
          </div>
        </div>

        {error && (
          <div
            className="error-message"
            role="alert"
          >
            {error}
          </div>
        )}

        {loading ? (
          <div className="dashboard-card loading-card">
            <p>Loading your profile...</p>
          </div>
        ) : profile ? (
          <CandidateProfileCard profile={profile} />
        ) : (
          <div className="dashboard-card setup-card">
            <div className="setup-icon">+</div>

            <div>
              <span className="card-label">
                GET STARTED
              </span>

              <h2>
                Create your candidate profile
              </h2>

              <p>
                Tell Hirely about your professional
                background. Your profile will help power
                future job matching and AI
                recommendations.
              </p>

              <Link
                to="/candidate/profile"
                className="primary-button"
              >
                Create Profile
              </Link>
            </div>
          </div>
        )}

        <div className="dashboard-grid">
          <div className="dashboard-card feature-card">
            <span className="card-label">
              RESUME
            </span>

            <h2>Resume</h2>

            <p>
              Upload and manage your resumes. AI-powered
              resume parsing extracts structured
              information for matching.
            </p>

            <Link
              to="/candidate/resumes"
              className="secondary-button"
            >
              Manage Resumes
            </Link>
          </div>

          <div className="dashboard-card feature-card">
            <span className="card-label">
              AI MATCHING
            </span>

            <h2>Job Matches</h2>

            <p>
              Discover jobs that match your skills and
              professional profile using Hirely's
              semantic matching engine.
            </p>

            <span className="coming-soon">
              AI matching next
            </span>
          </div>

          <div className="dashboard-card feature-card">
            <span className="card-label">
              APPLICATIONS
            </span>

            <h2>Applications</h2>

            <p>
              Track your job applications and monitor
              their progress from one workspace.
            </p>

            <span className="coming-soon">
              Applications next
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}

export default CandidateDashboard