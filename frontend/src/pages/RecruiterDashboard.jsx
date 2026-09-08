import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'
import {
  getRecruiterApplications,
  getRecruiterJobs,
} from '../services/recruiter'
import { getJob } from '../services/jobs'

import './Recruiter.css'

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

function formatStatus(status) {
  if (!status) {
    return 'Unknown'
  }

  return status
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function formatEmploymentType(value) {
  if (!value) {
    return 'Not specified'
  }

  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function JobSkeleton() {
  return (
    <div className="recruiter-job-skeleton">
      <div className="recruiter-skeleton recruiter-skeleton-icon" />

      <div className="recruiter-skeleton-content">
        <div className="recruiter-skeleton recruiter-skeleton-title" />
        <div className="recruiter-skeleton recruiter-skeleton-meta" />
      </div>

      <div className="recruiter-skeleton recruiter-skeleton-action" />
    </div>
  )
}

export default function RecruiterDashboard() {
  const { user } = useAuth()

  const [jobs, setJobs] = useState([])
  const [applications, setApplications] = useState([])
  const [recentApplications, setRecentApplications] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadDashboard() {
      setLoading(true)
      setError('')

      try {
        const [jobData, applicationData] =
          await Promise.all([
            getRecruiterJobs(),
            getRecruiterApplications(),
          ])

        if (!isMounted) {
          return
        }

        const recruiterId = user?.id

        const allJobs = Array.isArray(jobData)
          ? jobData
          : []

        const recruiterJobs = recruiterId
          ? allJobs.filter(
              (job) => job.recruiter_id === recruiterId,
            )
          : []

        const recruiterApplications = Array.isArray(
          applicationData,
        )
          ? applicationData
          : []

        setJobs(recruiterJobs)
        setApplications(recruiterApplications)

        const sortedApplications = [
          ...recruiterApplications,
        ].sort(
          (first, second) =>
            new Date(second.created_at).getTime() -
            new Date(first.created_at).getTime(),
        )

        const latestApplications =
          sortedApplications.slice(0, 5)

        const enrichedApplications =
          await Promise.all(
            latestApplications.map(async (application) => {
              try {
                const job = await getJob(application.job_id)

                return {
                  ...application,
                  job,
                }
              } catch {
                return {
                  ...application,
                  job: null,
                }
              }
            }),
          )

        if (!isMounted) {
          return
        }

        setRecentApplications(enrichedApplications)
      } catch (requestError) {
        if (!isMounted) {
          return
        }

        setError(
          requestError?.message ||
            'Unable to load the recruiter dashboard.',
        )
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadDashboard()

    return () => {
      isMounted = false
    }
  }, [user?.id])

  const metrics = useMemo(() => {
    const activeJobs = jobs.filter(
      (job) => job.is_active,
    ).length

    const interviews = applications.filter(
      (application) => application.status === 'interview',
    ).length

    const hired = applications.filter(
      (application) => application.status === 'hired',
    ).length

    return {
      activeJobs,
      applications: applications.length,
      interviews,
      hired,
    }
  }, [jobs, applications])

  const recentJobs = jobs.slice(0, 4)

  if (loading) {
    return (
      <main className="recruiter-page">
        <section className="recruiter-page-header">
          <div>
            <span className="recruiter-eyebrow">
              Recruiter workspace
            </span>

            <h1>Recruiter Dashboard</h1>

            <p>
              Manage your hiring pipeline and discover strong
              candidates with Hirely AI.
            </p>
          </div>
        </section>

        <section className="recruiter-metrics">
          {[1, 2, 3, 4].map((item) => (
            <div
              className="recruiter-metric-card loading"
              key={item}
            >
              <div className="recruiter-skeleton metric-icon" />

              <div>
                <div className="recruiter-skeleton metric-number" />
                <div className="recruiter-skeleton metric-label" />
              </div>
            </div>
          ))}
        </section>

        <section className="recruiter-section">
          <div className="recruiter-section-header">
            <div>
              <span className="recruiter-section-eyebrow">
                Your hiring workspace
              </span>
              <h2>Active jobs</h2>
            </div>
          </div>

          <div className="recruiter-job-list">
            {[1, 2, 3].map((item) => (
              <JobSkeleton key={item} />
            ))}
          </div>
        </section>
      </main>
    )
  }

  if (error) {
    return (
      <main className="recruiter-page">
        <section className="recruiter-page-header">
          <div>
            <span className="recruiter-eyebrow">
              Recruiter workspace
            </span>

            <h1>Recruiter Dashboard</h1>

            <p>
              Manage your hiring pipeline and discover strong
              candidates with Hirely AI.
            </p>
          </div>
        </section>

        <div className="recruiter-feedback error">
          <div className="recruiter-feedback-icon">!</div>

          <div>
            <h3>Dashboard unavailable</h3>
            <p>{error}</p>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="recruiter-page">
      <section className="recruiter-page-header">
        <div>
          <span className="recruiter-eyebrow">
            Recruiter workspace
          </span>

          <h1>
            Welcome
            {user?.email ? `, ${user.email.split('@')[0]}` : ''}
          </h1>

          <p>
            Manage your hiring pipeline and discover strong
            candidates with Hirely AI.
          </p>
        </div>

        <Link
          to="/recruiter/jobs/create"
          className="recruiter-primary-button"
        >
          <span>+ Create Job</span>
        </Link>
      </section>

      <section className="recruiter-metrics">
        <article className="recruiter-metric-card">
          <div className="recruiter-metric-icon jobs">
            ◫
          </div>

          <div>
            <span className="recruiter-metric-number">
              {metrics.activeJobs}
            </span>

            <span className="recruiter-metric-label">
              Active jobs
            </span>
          </div>
        </article>

        <article className="recruiter-metric-card">
          <div className="recruiter-metric-icon applications">
            ◎
          </div>

          <div>
            <span className="recruiter-metric-number">
              {metrics.applications}
            </span>

            <span className="recruiter-metric-label">
              Applications
            </span>
          </div>
        </article>

        <article className="recruiter-metric-card">
          <div className="recruiter-metric-icon interviews">
            ◉
          </div>

          <div>
            <span className="recruiter-metric-number">
              {metrics.interviews}
            </span>

            <span className="recruiter-metric-label">
              Interviews
            </span>
          </div>
        </article>

        <article className="recruiter-metric-card">
          <div className="recruiter-metric-icon hired">
            ✦
          </div>

          <div>
            <span className="recruiter-metric-number">
              {metrics.hired}
            </span>

            <span className="recruiter-metric-label">
              Hired
            </span>
          </div>
        </article>
      </section>

      <div className="recruiter-dashboard-grid">
        <section className="recruiter-section">
          <div className="recruiter-section-header">
            <div>
              <span className="recruiter-section-eyebrow">
                Hiring pipeline
              </span>

              <h2>Active jobs</h2>
            </div>

            <Link
              to="/recruiter/jobs"
              className="recruiter-text-link"
            >
              View all →
            </Link>
          </div>

          {recentJobs.length === 0 ? (
            <div className="recruiter-empty-card">
              <div className="recruiter-empty-icon">
                ◫
              </div>

              <h3>No jobs yet</h3>

              <p>
                Create your first job to start building your
                hiring pipeline.
              </p>

              <Link
                to="/recruiter/jobs/create"
                className="recruiter-secondary-button"
              >
                Create your first job
              </Link>
            </div>
          ) : (
            <div className="recruiter-job-list">
              {recentJobs.map((job) => (
                <article
                  className="recruiter-job-card"
                  key={job.id}
                >
                  <div className="recruiter-job-icon">
                    {job.title
                      ?.slice(0, 2)
                      .toUpperCase() || 'JB'}
                  </div>

                  <div className="recruiter-job-content">
                    <div className="recruiter-job-title-row">
                      <h3>{job.title}</h3>

                      <span className="recruiter-active-badge">
                        Active
                      </span>
                    </div>

                    <div className="recruiter-job-meta">
                      <span>
                        ⌖ {job.location || 'Location not specified'}
                      </span>

                      <span>
                        ◫ {formatEmploymentType(
                          job.employment_type,
                        )}
                      </span>

                      {job.experience_level && (
                        <span>
                          ◎ {job.experience_level}
                        </span>
                      )}
                    </div>
                  </div>

                  <Link
                    to={`/recruiter/jobs/${job.id}`}
                    className="recruiter-job-action"
                  >
                    Manage →
                  </Link>
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="recruiter-section recruiter-applications-section">
          <div className="recruiter-section-header">
            <div>
              <span className="recruiter-section-eyebrow">
                Candidate activity
              </span>

              <h2>Recent applications</h2>
            </div>

            <Link
              to="/recruiter/applications"
              className="recruiter-text-link"
            >
              View all →
            </Link>
          </div>

          {recentApplications.length === 0 ? (
            <div className="recruiter-empty-card compact">
              <div className="recruiter-empty-icon">
                ◎
              </div>

              <h3>No applications yet</h3>

              <p>
                Candidate applications will appear here as
                people apply to your jobs.
              </p>
            </div>
          ) : (
            <div className="recruiter-application-list">
              {recentApplications.map((application) => (
                <article
                  className="recruiter-application-row"
                  key={application.id}
                >
                  <div className="recruiter-candidate-avatar">
                    {application.candidate_id
                      ?.slice(0, 2)
                      .toUpperCase() || 'CA'}
                  </div>

                  <div className="recruiter-application-content">
                    <h3>
                      {application.job?.title ||
                        'Job application'}
                    </h3>

                    <span>
                      Candidate ID:{' '}
                      {application.candidate_id?.slice(
                        0,
                        8,
                      )}
                      ...
                    </span>

                    <small>
                      Applied {formatDate(application.created_at)}
                    </small>
                  </div>

                  <span
                    className={`recruiter-status recruiter-status-${application.status}`}
                  >
                    {formatStatus(application.status)}
                  </span>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  )
}