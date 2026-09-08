import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { getRecruiterJobs } from '../services/recruiter'

import './Recruiter.css'

function formatEmploymentType(value) {
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

function JobListSkeleton() {
  return (
    <div className="recruiter-job-list">
      {[1, 2, 3].map((item) => (
        <div className="recruiter-job-skeleton" key={item}>
          <div className="recruiter-skeleton recruiter-skeleton-icon" />

          <div className="recruiter-skeleton-content">
            <div className="recruiter-skeleton recruiter-skeleton-title" />
            <div className="recruiter-skeleton recruiter-skeleton-meta" />
          </div>

          <div className="recruiter-skeleton recruiter-skeleton-action" />
        </div>
      ))}
    </div>
  )
}

export default function RecruiterJobs() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState('active')

  useEffect(() => {
    let isMounted = true

    async function loadJobs() {
      setLoading(true)
      setError('')

      try {
        const data = await getRecruiterJobs()

        if (!isMounted) {
          return
        }

        const recruiterJobs = Array.isArray(data)
          ? data
          : []

        setJobs(recruiterJobs)
      } catch (requestError) {
        if (!isMounted) {
          return
        }

        setError(
          requestError?.message ||
            'Unable to load your jobs.',
        )
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadJobs()

    return () => {
      isMounted = false
    }
  }, [])

  const filteredJobs = useMemo(() => {
    if (filter === 'all') {
      return jobs
    }

    return jobs.filter((job) => job.is_active)
  }, [jobs, filter])

  return (
    <main className="recruiter-page">
      <section className="recruiter-page-header">
        <div>
          <span className="recruiter-eyebrow">
            Hiring workspace
          </span>

          <h1>My Jobs</h1>

          <p>
            Create and manage the opportunities you&apos;re
            hiring for.
          </p>
        </div>

        <Link
          to="/recruiter/jobs/create"
          className="recruiter-primary-button"
        >
          + Create Job
        </Link>
      </section>

      <section className="recruiter-jobs-toolbar">
        <div className="recruiter-filter-group">
          <button
            type="button"
            className={
              filter === 'active'
                ? 'recruiter-filter active'
                : 'recruiter-filter'
            }
            onClick={() => setFilter('active')}
          >
            Active
          </button>

          <button
            type="button"
            className={
              filter === 'all'
                ? 'recruiter-filter active'
                : 'recruiter-filter'
            }
            onClick={() => setFilter('all')}
          >
            All Jobs
          </button>
        </div>

        {!loading && (
          <span className="recruiter-results-count">
            {filteredJobs.length}{' '}
            {filteredJobs.length === 1 ? 'job' : 'jobs'}
          </span>
        )}
      </section>

      {loading && <JobListSkeleton />}

      {!loading && error && (
        <div className="recruiter-feedback error">
          <div className="recruiter-feedback-icon">!</div>

          <div>
            <h3>Couldn&apos;t load jobs</h3>
            <p>{error}</p>
          </div>
        </div>
      )}

      {!loading && !error && filteredJobs.length === 0 && (
        <div className="recruiter-empty-card large">
          <div className="recruiter-empty-icon">
            ◉
          </div>

          <h3>
            {filter === 'active'
              ? 'No active jobs'
              : 'No jobs yet'}
          </h3>

          <p>
            {filter === 'active'
              ? 'Create a new opportunity or check all jobs.'
              : 'Create your first job to start hiring.'}
          </p>

          <Link
            to="/recruiter/jobs/create"
            className="recruiter-secondary-button"
          >
            Create Job
          </Link>
        </div>
      )}

      {!loading && !error && filteredJobs.length > 0 && (
        <div className="recruiter-full-job-list">
          {filteredJobs.map((job) => (
            <article
              className="recruiter-full-job-card"
              key={job.id}
            >
              <div className="recruiter-job-icon large">
                {job.title?.slice(0, 2).toUpperCase() || 'JB'}
              </div>

              <div className="recruiter-full-job-content">
                <div className="recruiter-full-job-heading">
                  <div>
                    <span className="recruiter-card-eyebrow">
                      Job opportunity
                    </span>

                    <h2>{job.title}</h2>
                  </div>

                  <span
                    className={
                      job.is_active
                        ? 'recruiter-active-badge'
                        : 'recruiter-inactive-badge'
                    }
                  >
                    {job.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>

                <div className="recruiter-job-meta">
                  <span>
                    ⌖{' '}
                    {job.location ||
                      'Location not specified'}
                  </span>

                  <span>
                    ◉{' '}
                    {formatEmploymentType(
                      job.employment_type,
                    )}
                  </span>

                  {job.experience_level && (
                    <span>
                      ◎ {job.experience_level}
                    </span>
                  )}

                  <span>
                    ₹{' '}
                    {formatSalary(
                      job.salary_min,
                      job.salary_max,
                    )}
                  </span>
                </div>

                <p className="recruiter-job-description">
                  {job.description}
                </p>

                <div className="recruiter-full-job-footer">
                  <span className="recruiter-job-id">
                    Job ID: {job.id.slice(0, 8)}...
                  </span>

                  <div className="recruiter-job-actions">
                    <Link
                      to={`/recruiter/jobs/${job.id}`}
                      className="recruiter-outline-button"
                    >
                      View Job
                    </Link>

                    <Link
                      to={`/recruiter/jobs/${job.id}/candidates`}
                      className="recruiter-primary-small-button"
                    >
                      Find Candidates →
                    </Link>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </main>
  )
}