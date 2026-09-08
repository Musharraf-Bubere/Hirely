import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { getRecruiterJobs } from '../services/recruiter'

import './RecruiterJobDetail.css'

function formatEmploymentType(value) {
  if (!value) {
    return 'Not specified'
  }

  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function formatExperienceLevel(value) {
  if (!value) {
    return 'Not specified'
  }

  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function formatSalary(min, max) {
  if (min == null && max == null) {
    return 'Salary not specified'
  }

  const formatAmount = (amount) =>
    new Intl.NumberFormat('en-IN').format(amount)

  if (min != null && max != null) {
    return `₹${formatAmount(min)} – ₹${formatAmount(max)}`
  }

  if (min != null) {
    return `From ₹${formatAmount(min)}`
  }

  return `Up to ₹${formatAmount(max)}`
}

function formatDate(value) {
  if (!value) {
    return 'Not available'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return 'Not available'
  }

  return date.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

function LoadingState() {
  return (
    <main className="recruiter-job-detail-page">
      <div className="recruiter-detail-skeleton">
        <div className="detail-skeleton-small" />
        <div className="detail-skeleton-title" />
        <div className="detail-skeleton-meta" />
        <div className="detail-skeleton-card" />
        <div className="detail-skeleton-card short" />
      </div>
    </main>
  )
}

export default function RecruiterJobDetail() {
  const { jobId } = useParams()

  const [job, setJob] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function loadJob() {
      setLoading(true)
      setError('')

      try {
        const data = await getRecruiterJobs()

        if (!isMounted) {
          return
        }

        const jobs = Array.isArray(data) ? data : []

        const foundJob = jobs.find(
          (item) => String(item.id) === String(jobId),
        )

        if (!foundJob) {
          setError('Job not found or you do not have access to this job.')
          setJob(null)
          return
        }

        setJob(foundJob)
      } catch (requestError) {
        if (!isMounted) {
          return
        }

        setError(
          requestError?.message ||
            'Unable to load this job. Please try again.',
        )
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadJob()

    return () => {
      isMounted = false
    }
  }, [jobId])

  if (loading) {
    return <LoadingState />
  }

  if (error || !job) {
    return (
      <main className="recruiter-job-detail-page">
        <section className="recruiter-detail-error">
          <div className="recruiter-detail-error-icon">!</div>

          <span className="recruiter-detail-eyebrow">
            Job opportunity
          </span>

          <h1>Unable to open this job</h1>

          <p>
            {error ||
              'The requested job could not be found.'}
          </p>

          <Link
            to="/recruiter/jobs"
            className="recruiter-detail-primary-button"
          >
            Back to Jobs
          </Link>
        </section>
      </main>
    )
  }

  return (
    <main className="recruiter-job-detail-page">
      <section className="recruiter-job-detail-header">
        <div className="recruiter-job-detail-header-main">
          <Link
            to="/recruiter/jobs"
            className="recruiter-detail-back-link"
          >
            ← Back to Jobs
          </Link>

          <div className="recruiter-job-detail-title-row">
            <div className="recruiter-detail-job-icon">
              {job.title?.slice(0, 2).toUpperCase() || 'JB'}
            </div>

            <div>
              <div className="recruiter-detail-eyebrow">
                Job opportunity
              </div>

              <h1>{job.title}</h1>

              <p>
                Created on {formatDate(job.created_at)}
              </p>
            </div>
          </div>
        </div>

        <div className="recruiter-detail-status-area">
          <span
            className={
              job.is_active
                ? 'recruiter-detail-status active'
                : 'recruiter-detail-status inactive'
            }
          >
            <span className="recruiter-detail-status-dot" />
            {job.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>
      </section>

      <section className="recruiter-detail-action-bar">
        <div>
          <strong>Ready to hire?</strong>
          <span>
            Find and evaluate candidates for this opportunity.
          </span>
        </div>

        <Link
          to={`/recruiter/jobs/${job.id}/candidates`}
          className="recruiter-detail-primary-button"
        >
          Find Candidates →
        </Link>
      </section>

      <section className="recruiter-detail-grid">
        <div className="recruiter-detail-main-column">
          <article className="recruiter-detail-card">
            <div className="recruiter-detail-card-header">
              <div>
                <span className="recruiter-detail-card-eyebrow">
                  Opportunity
                </span>

                <h2>Job Description</h2>
              </div>
            </div>

            <div className="recruiter-detail-description">
              {job.description ? (
                job.description
                  .split('\n')
                  .map((paragraph, index) => (
                    <p key={`${paragraph}-${index}`}>
                      {paragraph || '\u00A0'}
                    </p>
                  ))
              ) : (
                <p>No job description provided.</p>
              )}
            </div>
          </article>
        </div>

        <aside className="recruiter-detail-side-column">
          <article className="recruiter-detail-card">
            <div className="recruiter-detail-card-header">
              <div>
                <span className="recruiter-detail-card-eyebrow">
                  Position details
                </span>

                <h2>Job Information</h2>
              </div>
            </div>

            <div className="recruiter-detail-info-list">
              <div className="recruiter-detail-info-item">
                <span>Location</span>
                <strong>
                  {job.location || 'Not specified'}
                </strong>
              </div>

              <div className="recruiter-detail-info-item">
                <span>Employment Type</span>
                <strong>
                  {formatEmploymentType(
                    job.employment_type,
                  )}
                </strong>
              </div>

              <div className="recruiter-detail-info-item">
                <span>Experience Level</span>
                <strong>
                  {formatExperienceLevel(
                    job.experience_level,
                  )}
                </strong>
              </div>

              <div className="recruiter-detail-info-item">
                <span>Salary Range</span>
                <strong>
                  {formatSalary(
                    job.salary_min,
                    job.salary_max,
                  )}
                </strong>
              </div>
            </div>
          </article>

          <article className="recruiter-detail-card recruiter-detail-ai-card">
            <div className="recruiter-detail-ai-icon">✦</div>

            <span className="recruiter-detail-card-eyebrow">
              AI Hiring
            </span>

            <h2>AI Candidate Matching</h2>

            <p>
              Hirely can analyze eligible candidates and
              rank them according to skills, semantic
              similarity, and overall job fit.
            </p>

            <Link
              to={`/recruiter/jobs/${job.id}/candidates`}
              className="recruiter-detail-ai-link"
            >
              Explore matching →
            </Link>
          </article>
        </aside>
      </section>
    </main>
  )
}