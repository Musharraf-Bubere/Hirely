import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { getMyApplications } from '../services/applications'
import { getJob } from '../services/jobs'

import './Applications.css'

const STATUS_CONFIG = {
  applied: {
    label: 'Applied',
    className: 'status-applied',
    icon: '✓',
  },
  shortlisted: {
    label: 'Shortlisted',
    className: 'status-shortlisted',
    icon: '★',
  },
  interview: {
    label: 'Interview',
    className: 'status-interview',
    icon: '◉',
  },
  hired: {
    label: 'Hired',
    className: 'status-hired',
    icon: '✓',
  },
  rejected: {
    label: 'Rejected',
    className: 'status-rejected',
    icon: '×',
  },
}

function formatStatus(status) {
  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function formatDate(dateValue) {
  if (!dateValue) {
    return 'Date unavailable'
  }

  const date = new Date(dateValue)

  if (Number.isNaN(date.getTime())) {
    return 'Date unavailable'
  }

  return new Intl.DateTimeFormat('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(date)
}

function getJobInitials(title = 'Job') {
  const words = title
    .trim()
    .split(/\s+/)
    .filter(Boolean)

  if (words.length === 0) {
    return 'J'
  }

  if (words.length === 1) {
    return words[0].slice(0, 2).toUpperCase()
  }

  return `${words[0][0]}${words[1][0]}`.toUpperCase()
}

function getEmploymentLabel(value) {
  if (!value) {
    return null
  }

  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function getExperienceLabel(value) {
  if (!value) {
    return null
  }

  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function ApplicationSkeleton() {
  return (
    <div className="application-skeleton-list">
      {[1, 2, 3].map((item) => (
        <div className="application-skeleton" key={item}>
          <div className="skeleton skeleton-avatar" />

          <div className="skeleton-content">
            <div className="skeleton skeleton-title" />
            <div className="skeleton skeleton-meta" />
            <div className="skeleton skeleton-meta short" />
          </div>

          <div className="skeleton skeleton-status" />
        </div>
      ))}
    </div>
  )
}

function ApplicationCard({ application }) {
  const {
    id,
    job_id: jobId,
    status,
    created_at: createdAt,
    updated_at: updatedAt,
    job,
    jobLoading,
  } = application

  const statusConfig = STATUS_CONFIG[status] || {
    label: formatStatus(status || 'unknown'),
    className: 'status-default',
    icon: '•',
  }

  const jobTitle = job?.title || 'Job opportunity'
  const location = job?.location || 'Location not specified'
  const employmentType = getEmploymentLabel(job?.employment_type)
  const experienceLevel = getExperienceLabel(job?.experience_level)

  return (
    <article className="application-card">
      <div className="application-card-main">
        <div className="application-job-avatar">
          {jobLoading ? '...' : getJobInitials(jobTitle)}
        </div>

        <div className="application-content">
          <div className="application-heading-row">
            <div>
              <span className="application-eyebrow">
                Application
              </span>

              <h2>{jobLoading ? 'Loading opportunity...' : jobTitle}</h2>
            </div>

            <span className={`application-status ${statusConfig.className}`}>
              <span className="status-icon">
                {statusConfig.icon}
              </span>
              {statusConfig.label}
            </span>
          </div>

          {jobLoading ? (
            <div className="application-inline-loading">
              Loading job details...
            </div>
          ) : (
            <>
              <div className="application-meta">
                <span>
                  <span className="meta-icon">⌖</span>
                  {location}
                </span>

                {employmentType && (
                  <span>
                    <span className="meta-icon">◫</span>
                    {employmentType}
                  </span>
                )}

                {experienceLevel && (
                  <span>
                    <span className="meta-icon">◎</span>
                    {experienceLevel}
                  </span>
                )}
              </div>

              <div className="application-timeline">
                <div className="timeline-item">
                  <span className="timeline-dot active" />

                  <div>
                    <span className="timeline-label">
                      Applied
                    </span>
                    <span className="timeline-date">
                      {formatDate(createdAt)}
                    </span>
                  </div>
                </div>

                {updatedAt && updatedAt !== createdAt && (
                  <div className="timeline-item">
                    <span className="timeline-dot" />

                    <div>
                      <span className="timeline-label">
                        Last updated
                      </span>
                      <span className="timeline-date">
                        {formatDate(updatedAt)}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>

      <div className="application-card-footer">
        <span className="application-id">
          Application ID: {id.slice(0, 8)}...
        </span>

        {jobId && (
          <Link
            to={`/candidate/jobs/${jobId}`}
            className="application-view-button"
          >
            View Job
            <span>→</span>
          </Link>
        )}
      </div>
    </article>
  )
}

export default function Applications() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadApplications() {
      setLoading(true)
      setError('')

      try {
        const applicationData = await getMyApplications()

        if (!isMounted) {
          return
        }

        const applicationList = Array.isArray(applicationData)
          ? applicationData
          : []

        const enrichedApplications = applicationList.map(
          (application) => ({
            ...application,
            job: null,
            jobLoading: true,
          }),
        )

        setApplications(enrichedApplications)

        const jobResults = await Promise.all(
          enrichedApplications.map(async (application) => {
            try {
              const job = await getJob(application.job_id)

              return {
                applicationId: application.id,
                job,
              }
            } catch {
              return {
                applicationId: application.id,
                job: null,
              }
            }
          }),
        )

        if (!isMounted) {
          return
        }

        setApplications((currentApplications) =>
          currentApplications.map((application) => {
            const jobResult = jobResults.find(
              (result) =>
                result.applicationId === application.id,
            )

            return {
              ...application,
              job: jobResult?.job || null,
              jobLoading: false,
            }
          }),
        )
      } catch (requestError) {
        if (!isMounted) {
          return
        }

        setError(
          requestError?.message ||
            'Unable to load your applications right now.',
        )
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadApplications()

    return () => {
      isMounted = false
    }
  }, [])

  const summary = useMemo(() => {
    const total = applications.length

    const active = applications.filter(
      (application) =>
        ['applied', 'shortlisted', 'interview'].includes(
          application.status,
        ),
    ).length

    const interviews = applications.filter(
      (application) => application.status === 'interview',
    ).length

    const hired = applications.filter(
      (application) => application.status === 'hired',
    ).length

    return {
      total,
      active,
      interviews,
      hired,
    }
  }, [applications])

  return (
    <main className="applications-page">
      <section className="applications-header">
        <div className="applications-header-copy">
          <span className="page-eyebrow">
            Career activity
          </span>

          <h1>My Applications</h1>

          <p>
            Track the opportunities you&apos;ve applied to and
            follow your application journey in one place.
          </p>
        </div>

        <Link
          to="/candidate/jobs"
          className="applications-primary-button"
        >
          <span>Explore Jobs</span>
          <span>→</span>
        </Link>
      </section>

      {!loading && !error && applications.length > 0 && (
        <section className="application-summary">
          <div className="summary-card">
            <span className="summary-icon">◫</span>
            <div>
              <span className="summary-value">
                {summary.total}
              </span>
              <span className="summary-label">
                Total applications
              </span>
            </div>
          </div>

          <div className="summary-card">
            <span className="summary-icon">◌</span>
            <div>
              <span className="summary-value">
                {summary.active}
              </span>
              <span className="summary-label">
                Active applications
              </span>
            </div>
          </div>

          <div className="summary-card">
            <span className="summary-icon">◎</span>
            <div>
              <span className="summary-value">
                {summary.interviews}
              </span>
              <span className="summary-label">
                Interviews
              </span>
            </div>
          </div>

          <div className="summary-card">
            <span className="summary-icon">✦</span>
            <div>
              <span className="summary-value">
                {summary.hired}
              </span>
              <span className="summary-label">
                Hired
              </span>
            </div>
          </div>
        </section>
      )}

      <section className="applications-section">
        <div className="section-heading">
          <div>
            <span className="section-eyebrow">
              Application history
            </span>

            <h2>Your applications</h2>
          </div>

          {!loading && applications.length > 0 && (
            <span className="application-count">
              {applications.length}{' '}
              {applications.length === 1
                ? 'application'
                : 'applications'}
            </span>
          )}
        </div>

        {loading && <ApplicationSkeleton />}

        {!loading && error && (
          <div className="applications-feedback error">
            <div className="feedback-icon">!</div>

            <div>
              <h3>Couldn&apos;t load applications</h3>
              <p>{error}</p>
            </div>
          </div>
        )}

        {!loading && !error && applications.length === 0 && (
          <div className="applications-feedback empty">
            <div className="empty-visual">
              <span>⌕</span>
            </div>

            <h3>No applications yet</h3>

            <p>
              Start exploring opportunities that match your
              skills and career goals.
            </p>

            <Link
              to="/candidate/jobs"
              className="applications-primary-button"
            >
              Find Opportunities
              <span>→</span>
            </Link>
          </div>
        )}

        {!loading && !error && applications.length > 0 && (
          <div className="application-list">
            {applications.map((application) => (
              <ApplicationCard
                key={application.id}
                application={application}
              />
            ))}
          </div>
        )}
      </section>
    </main>
  )
}