import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import {
  applyToJob,
  getJob,
  matchCandidateToJob,
} from '../services/jobs'

import { getMyApplications } from '../services/applications'

import './Jobs.css'

function formatPercentage(value) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return null
  }

  return Math.round(
    Math.max(0, Math.min(1, value)) * 100,
  )
}

function formatSkillList(skills) {
  if (!Array.isArray(skills)) {
    return []
  }

  return skills.filter(
    (skill) =>
      typeof skill === 'string' &&
      skill.trim().length > 0,
  )
}

function formatApplicationStatus(status) {
  if (!status) {
    return 'Applied'
  }

  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function JobDetail() {
  const { jobId } = useParams()
  const navigate = useNavigate()

  const [job, setJob] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [actionLoading, setActionLoading] = useState('')
  const [actionMessage, setActionMessage] = useState('')
  const [actionError, setActionError] = useState('')

  const [matchResult, setMatchResult] = useState(null)

  const [application, setApplication] = useState(null)
  const [applicationLoading, setApplicationLoading] = useState(false)

  useEffect(() => {
    let ignore = false

    async function loadJob() {
      try {
        setLoading(true)
        setError('')

        const data = await getJob(jobId)

        if (!ignore) {
          setJob(data)
        }
      } catch (err) {
        if (!ignore) {
          setError(
            err.message ||
              'Unable to load this opportunity.',
          )
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadJob()

    return () => {
      ignore = true
    }
  }, [jobId])

  useEffect(() => {
    let ignore = false

    async function loadApplication() {
      const token = localStorage.getItem(
        'hirely_access_token',
      )

      if (!token) {
        return
      }

      try {
        setApplicationLoading(true)

        const applications = await getMyApplications()

        if (ignore || !Array.isArray(applications)) {
          return
        }

        const existingApplication = applications.find(
          (item) => item.job_id === jobId,
        )

        if (!ignore) {
          setApplication(existingApplication || null)
        }
      } catch {
        /*
         * Application lookup should never prevent the job
         * detail page from loading.
         *
         * This also keeps public job pages usable when the
         * current token belongs to a non-candidate user.
         */
      } finally {
        if (!ignore) {
          setApplicationLoading(false)
        }
      }
    }

    loadApplication()

    return () => {
      ignore = true
    }
  }, [jobId])

  async function handleApply() {
    const token = localStorage.getItem(
      'hirely_access_token',
    )

    if (!token) {
      navigate('/login', {
        state: {
          from: `/jobs/${jobId}`,
        },
      })

      return
    }

    if (application) {
      navigate('/candidate/applications')
      return
    }

    try {
      setActionLoading('apply')
      setActionMessage('')
      setActionError('')

      const createdApplication = await applyToJob(jobId)

      setApplication(
        createdApplication || {
          job_id: jobId,
          status: 'applied',
        },
      )

      setActionMessage(
        'Application submitted successfully.',
      )
    } catch (err) {
      setActionError(
        err.message ||
          'Unable to submit your application.',
      )
    } finally {
      setActionLoading('')
    }
  }

  async function handleMatch() {
    const token = localStorage.getItem(
      'hirely_access_token',
    )

    if (!token) {
      navigate('/login', {
        state: {
          from: `/jobs/${jobId}`,
        },
      })

      return
    }

    try {
      setActionLoading('match')
      setActionMessage('')
      setActionError('')
      setMatchResult(null)

      const result = await matchCandidateToJob(jobId)

      if (
        !result ||
        !result.score ||
        typeof result.score.overall_score !== 'number'
      ) {
        setActionError(
          'The matching engine returned an invalid match result.',
        )
        return
      }

      setMatchResult(result)
    } catch (err) {
      setActionError(
        err.message ||
          'Unable to calculate your AI match.',
      )
    } finally {
      setActionLoading('')
    }
  }

  function handleCoverLetter() {
    const token = localStorage.getItem(
      'hirely_access_token',
    )

    if (!token) {
      navigate('/login', {
        state: {
          from: `/jobs/${jobId}`,
        },
      })

      return
    }

    navigate(
      `/candidate/cover-letter?job_id=${jobId}`,
    )
  }

  const matchSummary = useMemo(() => {
    if (!matchResult?.score) {
      return null
    }

    return {
      overall: formatPercentage(
        matchResult.score.overall_score,
      ),
      required: formatPercentage(
        matchResult.score.required_skill_score,
      ),
      preferred: formatPercentage(
        matchResult.score.preferred_skill_score,
      ),
      semantic: formatPercentage(
        matchResult.score.semantic_similarity,
      ),
    }
  }, [matchResult])

  if (loading) {
    return (
      <section className="job-detail-page">
        <div className="jobs-container">
          <div className="job-detail-skeleton">
            <div className="skeleton-line skeleton-company" />

            <div className="skeleton-line skeleton-detail-title" />

            <div className="skeleton-line skeleton-detail-text" />

            <div className="skeleton-line skeleton-detail-text-short" />

            <div className="detail-skeleton-body">
              <div>
                <div className="skeleton-line skeleton-heading" />

                <div className="skeleton-line skeleton-body" />

                <div className="skeleton-line skeleton-body" />

                <div className="skeleton-line skeleton-body-short" />
              </div>

              <div className="skeleton-detail-side" />
            </div>
          </div>
        </div>
      </section>
    )
  }

  if (error || !job) {
    return (
      <section className="job-detail-page">
        <div className="jobs-container">
          <div className="job-not-found">
            <div className="jobs-empty-icon">
              !
            </div>

            <span className="jobs-overline">
              OPPORTUNITY UNAVAILABLE
            </span>

            <h1>
              This opportunity could not be loaded.
            </h1>

            <p>
              {error ||
                'The requested job is no longer available.'}
            </p>

            <Link
              to="/jobs"
              className="primary-button"
            >
              Browse opportunities
            </Link>
          </div>
        </div>
      </section>
    )
  }

  const salary =
    job.salary_min || job.salary_max
      ? `₹${job.salary_min?.toLocaleString('en-IN') || '—'} - ₹${job.salary_max?.toLocaleString('en-IN') || '—'}`
      : 'Salary not specified'

  const requiredMatched = formatSkillList(
    matchResult?.skills?.required_matched,
  )

  const requiredMissing = formatSkillList(
    matchResult?.skills?.required_missing,
  )

  const preferredMatched = formatSkillList(
    matchResult?.skills?.preferred_matched,
  )

  const preferredMissing = formatSkillList(
    matchResult?.skills?.preferred_missing,
  )

  const hasApplication = Boolean(application)

  const applicationStatus = application
    ? formatApplicationStatus(application.status)
    : ''

  return (
    <section className="job-detail-page">
      <div className="jobs-container">
        <Link
          to="/jobs"
          className="back-to-jobs"
        >
          <span aria-hidden="true">
            ←
          </span>

          Back to opportunities
        </Link>

        <header className="job-detail-hero">
          <div className="job-detail-company-mark">
            {job.title?.charAt(0)?.toUpperCase() ||
              'J'}
          </div>

          <div className="job-detail-heading">
            <span className="job-active-badge">
              <span />
              Active opportunity
            </span>

            <h1>{job.title}</h1>

            <p>
              Hirely opportunity

              <span>•</span>

              {job.location ||
                'Location not specified'}
            </p>
          </div>
        </header>

        <div className="job-detail-layout">
          <main className="job-detail-main">
            <div className="job-detail-meta">
              <div>
                <span>EMPLOYMENT</span>

                <strong>
                  {job.employment_type ||
                    'Not specified'}
                </strong>
              </div>

              <div>
                <span>EXPERIENCE</span>

                <strong>
                  {job.experience_level ||
                    'Not specified'}
                </strong>
              </div>

              <div>
                <span>LOCATION</span>

                <strong>
                  {job.location ||
                    'Not specified'}
                </strong>
              </div>

              <div>
                <span>COMPENSATION</span>

                <strong>{salary}</strong>
              </div>
            </div>

            <article className="job-description-section">
              <span className="jobs-overline">
                THE OPPORTUNITY
              </span>

              <h2>
                About this role
              </h2>

              <div className="job-description-content">
                {job.description
                  ?.split('\n')
                  .filter(Boolean)
                  .map((paragraph, index) => (
                    <p key={index}>
                      {paragraph}
                    </p>
                  ))}
              </div>
            </article>
          </main>

          <aside className="job-action-panel">
            <div className="job-action-panel-inner">
              <span className="jobs-overline">
                READY TO MOVE?
              </span>

              <h2>
                Take the next step in your career.
              </h2>

              <p>
                Apply directly or use Hirely's AI
                matching engine to understand how your
                profile aligns with this opportunity.
              </p>

              {applicationLoading ? (
                <button
                  type="button"
                  className="primary-button job-apply-button"
                  disabled
                >
                  Checking application...
                </button>
              ) : hasApplication ? (
                <>
                  <button
                    type="button"
                    className="primary-button job-apply-button"
                    disabled
                  >
                    <span aria-hidden="true">
                      ✓
                    </span>

                    {applicationStatus}
                  </button>

                  <Link
                    to="/candidate/applications"
                    className="job-match-button"
                  >
                    <span aria-hidden="true">
                      →
                    </span>

                    View my application
                  </Link>
                </>
              ) : (
                <button
                  type="button"
                  className="primary-button job-apply-button"
                  onClick={handleApply}
                  disabled={actionLoading !== ''}
                >
                  {actionLoading === 'apply'
                    ? 'Submitting...'
                    : 'Apply for this role'}

                  {actionLoading !== 'apply' && (
                    <span aria-hidden="true">
                      →
                    </span>
                  )}
                </button>
              )}

              <button
                type="button"
                className="job-match-button"
                onClick={handleMatch}
                disabled={actionLoading !== ''}
              >
                <span aria-hidden="true">
                  ✦
                </span>

                {actionLoading === 'match'
                  ? 'Analyzing your profile...'
                  : 'Check my AI match'}
              </button>

              <button
                type="button"
                className="job-match-button"
                onClick={handleCoverLetter}
                disabled={actionLoading !== ''}
              >
                <span aria-hidden="true">
                  ✎
                </span>

                Generate Cover Letter
              </button>

              {actionMessage && (
                <div className="job-action-success">
                  <span>✓</span>

                  {actionMessage}
                </div>
              )}

              {actionError && (
                <div className="job-action-error">
                  <span>!</span>

                  {actionError}
                </div>
              )}

              {matchResult && matchSummary && (
                <div className="job-match-result">
                  <div className="match-result-heading">
                    <div>
                      <span>
                        AI MATCH
                      </span>

                      <strong>
                        {matchSummary.overall}%
                      </strong>
                    </div>

                    <span className="match-confidence-label">
                      Strong alignment
                    </span>
                  </div>

                  <div className="match-result-bar">
                    <div
                      style={{
                        width: `${matchSummary.overall}%`,
                      }}
                    />
                  </div>

                  <div className="match-signal-grid">
                    <div className="match-signal">
                      <span>
                        Required skills
                      </span>

                      <strong>
                        {matchSummary.required}%
                      </strong>
                    </div>

                    <div className="match-signal">
                      <span>
                        Preferred skills
                      </span>

                      <strong>
                        {matchSummary.preferred}%
                      </strong>
                    </div>

                    <div className="match-signal">
                      <span>
                        Semantic similarity
                      </span>

                      <strong>
                        {matchSummary.semantic}%
                      </strong>
                    </div>
                  </div>

                  {requiredMatched.length > 0 && (
                    <div className="match-skill-section">
                      <span className="match-skill-label">
                        Required skills matched
                      </span>

                      <div className="match-skill-list">
                        {requiredMatched.map(
                          (skill) => (
                            <span
                              key={`required-matched-${skill}`}
                              className="match-skill match-skill-success"
                            >
                              ✓ {skill}
                            </span>
                          ),
                        )}
                      </div>
                    </div>
                  )}

                  {requiredMissing.length > 0 && (
                    <div className="match-skill-section">
                      <span className="match-skill-label">
                        Required skills to develop
                      </span>

                      <div className="match-skill-list">
                        {requiredMissing.map(
                          (skill) => (
                            <span
                              key={`required-missing-${skill}`}
                              className="match-skill match-skill-missing"
                            >
                              {skill}
                            </span>
                          ),
                        )}
                      </div>
                    </div>
                  )}

                  {preferredMatched.length > 0 && (
                    <div className="match-skill-section">
                      <span className="match-skill-label">
                        Preferred skills matched
                      </span>

                      <div className="match-skill-list">
                        {preferredMatched.map(
                          (skill) => (
                            <span
                              key={`preferred-matched-${skill}`}
                              className="match-skill match-skill-preferred"
                            >
                              ✓ {skill}
                            </span>
                          ),
                        )}
                      </div>
                    </div>
                  )}

                  {preferredMissing.length > 0 && (
                    <div className="match-skill-section">
                      <span className="match-skill-label">
                        Preferred skills not found
                      </span>

                      <div className="match-skill-list">
                        {preferredMissing.map(
                          (skill) => (
                            <span
                              key={`preferred-missing-${skill}`}
                              className="match-skill match-skill-missing"
                            >
                              {skill}
                            </span>
                          ),
                        )}
                      </div>
                    </div>
                  )}

                  <p>
                    This score combines deterministic skill
                    matching with semantic similarity from
                    Hirely's matching engine.
                  </p>
                </div>
              )}
            </div>
          </aside>
        </div>
      </div>
    </section>
  )
}

export default JobDetail