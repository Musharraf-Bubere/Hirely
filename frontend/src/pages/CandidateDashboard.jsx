import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import CandidateProfileCard from '../components/CandidateProfileCard'
import DashboardStatCard from '../components/dashboard/DashboardStatCard'
import CareerHealthCard from '../components/dashboard/CareerHealthCard'
import ResumeOverviewCard from '../components/dashboard/ResumeOverviewCard'

import { getCandidateProfile } from '../services/candidate'
import { getResumes } from '../services/resume'

import './CandidateDashboard.css'

function CandidateDashboard() {
  const [profile, setProfile] = useState(null)
  const [resumes, setResumes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadDashboard() {
      setLoading(true)
      setError('')

      const [profileResult, resumesResult] = await Promise.allSettled([
        getCandidateProfile(),
        getResumes(),
      ])

      if (ignore) {
        return
      }

      if (profileResult.status === 'fulfilled') {
        setProfile(profileResult.value)
      } else if (
        !profileResult.reason?.message
          ?.toLowerCase()
          .includes('not found')
      ) {
        setError(profileResult.reason?.message || 'Unable to load your profile.')
      }

      if (resumesResult.status === 'fulfilled') {
        setResumes(Array.isArray(resumesResult.value) ? resumesResult.value : [])
      } else if (!error) {
        setError(
          resumesResult.reason?.message || 'Unable to load your resumes.',
        )
      }

      setLoading(false)
    }

    loadDashboard()

    return () => {
      ignore = true
    }
  }, [])

  const profileCompletion = useMemo(() => {
    if (!profile) {
      return 0
    }

    const checks = [
      Boolean(profile.first_name?.trim() && profile.last_name?.trim()),
      Boolean(profile.headline?.trim()),
      Boolean(profile.bio?.trim()),
      Boolean(profile.location?.trim()),
    ]

    const completed = checks.filter(Boolean).length

    return Math.round((completed / checks.length) * 100)
  }, [profile])

  const activeResume = useMemo(
    () => resumes.find((resume) => resume.is_active),
    [resumes],
  )

  const resumeReady =
    Boolean(activeResume) &&
    activeResume.parsing_status === 'COMPLETED'

  const firstName = profile?.first_name || 'there'

  const greeting = useMemo(() => {
    const hour = new Date().getHours()

    if (hour < 12) {
      return 'Good morning'
    }

    if (hour < 18) {
      return 'Good afternoon'
    }

    return 'Good evening'
  }, [])

  if (loading) {
    return (
      <section className="candidate-dashboard-page">
        <div className="dashboard-container">
          <div className="dashboard-loading">
            <div className="dashboard-skeleton dashboard-skeleton-small" />
            <div className="dashboard-skeleton dashboard-skeleton-title" />
            <div className="dashboard-skeleton dashboard-skeleton-text" />

            <div className="dashboard-skeleton-grid">
              <div className="dashboard-skeleton dashboard-skeleton-card" />
              <div className="dashboard-skeleton dashboard-skeleton-card" />
              <div className="dashboard-skeleton dashboard-skeleton-card" />
            </div>

            <div className="dashboard-skeleton dashboard-skeleton-large" />
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="candidate-dashboard-page">
      <div className="dashboard-container">
        {error && (
          <div className="dashboard-alert" role="alert">
            <span className="dashboard-alert-icon">!</span>
            <div>
              <strong>Some dashboard data could not be loaded.</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        <header className="candidate-dashboard-hero">
          <div>
            <span className="dashboard-overline">CANDIDATE WORKSPACE</span>

            <h1>
              {greeting}, {firstName}
              <span className="hero-wave">👋</span>
            </h1>

            <p>
              Keep your profile sharp, manage your resume, and get ready for
              AI-powered opportunities.
            </p>
          </div>

          <div className="dashboard-hero-actions">
            <Link to="/candidate/profile" className="secondary-button">
              Edit Profile
            </Link>

            <Link to="/candidate/resumes" className="primary-button">
              Manage Resume
            </Link>
          </div>
        </header>

        <div className="dashboard-stat-grid">
          <DashboardStatCard
            label="Profile"
            value={`${profileCompletion}%`}
            description={
              profileCompletion === 100
                ? 'Your core profile is complete.'
                : 'Complete your profile to improve readiness.'
            }
            icon="◎"
            tone={profileCompletion >= 80 ? 'success' : 'default'}
          />

          <DashboardStatCard
            label="Resume versions"
            value={resumes.length}
            description={
              resumes.length
                ? 'Resume versions available in your workspace.'
                : 'Upload your first resume to get started.'
            }
            icon="▤"
          />

          <DashboardStatCard
            label="Active resume"
            value={resumeReady ? 'Ready' : 'Setup'}
            description={
              resumeReady
                ? 'Your active resume is ready for matching.'
                : 'Activate a successfully parsed resume.'
            }
            icon="✦"
            tone={resumeReady ? 'success' : 'warning'}
          />

          <DashboardStatCard
            label="AI readiness"
            value={
              profileCompletion >= 80 && resumeReady
                ? 'Ready'
                : 'In progress'
            }
            description={
              profileCompletion >= 80 && resumeReady
                ? 'Your profile is prepared for AI matching.'
                : 'Finish your profile and resume setup.'
            }
            icon="⌁"
            tone={
              profileCompletion >= 80 && resumeReady
                ? 'success'
                : 'default'
            }
          />
        </div>

        <div className="dashboard-main-grid">
          <CareerHealthCard
            profile={profile}
            profileCompletion={profileCompletion}
            resumeReady={resumeReady}
            activeResume={activeResume}
          />

          <div className="dashboard-ai-card">
            <div className="ai-card-glow" />

            <div className="ai-card-icon" aria-hidden="true">
              ✦
            </div>

            <span className="dashboard-overline">HIRELY AI</span>

            <h2>Your career workspace is getting smarter.</h2>

            <p>
              Hirely uses your structured profile and resume to prepare
              semantic job matching, ranking, and explainable recommendations.
            </p>

            <div className="ai-card-status">
              <span className="ai-status-dot" />
              <span>
                {resumeReady
                  ? 'Resume intelligence is ready'
                  : 'Complete your resume setup to continue'}
              </span>
            </div>

            <Link to="/candidate/resumes" className="ai-card-link">
              {resumeReady ? 'Review Resume' : 'Prepare Resume'}
              <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>

        <div className="dashboard-content-grid">
          <ResumeOverviewCard
            resumes={resumes}
            activeResume={activeResume}
          />

          <article className="dashboard-surface opportunities-card">
            <div className="dashboard-section-heading">
              <div>
                <span className="dashboard-overline">OPPORTUNITIES</span>
                <h2>Recommended jobs</h2>
              </div>

              <span className="dashboard-coming-soon">
                AI matching next
              </span>
            </div>

            <div className="dashboard-empty-state">
              <div className="empty-state-orbit">
                <span>✦</span>
              </div>

              <h3>Your personalized matches are coming next.</h3>

              <p>
                Once job discovery is connected to the matching engine,
                Hirely will surface relevant opportunities based on your
                skills and semantic profile.
              </p>
            </div>
          </article>
        </div>

        <div className="dashboard-bottom-grid">
          <article className="dashboard-surface applications-card">
            <div className="dashboard-section-heading">
              <div>
                <span className="dashboard-overline">APPLICATIONS</span>
                <h2>Recent applications</h2>
              </div>

              <span className="dashboard-coming-soon">
                Coming next
              </span>
            </div>

            <div className="dashboard-empty-state dashboard-empty-state-compact">
              <div className="empty-state-icon">↗</div>

              <div>
                <h3>No applications to show yet</h3>
                <p>
                  Your application activity will appear here once the job
                  discovery and application workflow is connected.
                </p>
              </div>
            </div>
          </article>

          <article className="dashboard-surface profile-preview-card">
            <div className="dashboard-section-heading">
              <div>
                <span className="dashboard-overline">PROFILE</span>
                <h2>Professional profile</h2>
              </div>

              <Link to="/candidate/profile" className="dashboard-text-link">
                Edit
                <span aria-hidden="true">→</span>
              </Link>
            </div>

            {profile ? (
              <CandidateProfileCard profile={profile} />
            ) : (
              <div className="dashboard-empty-state dashboard-empty-state-compact">
                <div className="empty-state-icon">+</div>

                <div>
                  <h3>Complete your profile</h3>
                  <p>
                    Add your professional information so Hirely can build a
                    better candidate representation.
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
          </article>
        </div>
      </div>
    </section>
  )
}

export default CandidateDashboard