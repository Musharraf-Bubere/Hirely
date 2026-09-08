import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import JobCard from '../components/JobCard'
import { getJobs } from '../services/jobs'

import './Jobs.css'

function Jobs() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [search, setSearch] = useState('')
  const [location, setLocation] = useState('')
  const [employmentType, setEmploymentType] = useState('')
  const [experienceLevel, setExperienceLevel] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadJobs() {
      try {
        setLoading(true)
        setError('')

        const data = await getJobs()

        if (!ignore) {
          setJobs(Array.isArray(data) ? data : [])
        }
      } catch (err) {
        if (!ignore) {
          setError(err.message || 'Unable to load jobs.')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadJobs()

    return () => {
      ignore = true
    }
  }, [])

  const employmentTypes = useMemo(() => {
    return [
      ...new Set(
        jobs
          .map((job) => job.employment_type)
          .filter(Boolean),
      ),
    ].sort()
  }, [jobs])

  const experienceLevels = useMemo(() => {
    return [
      ...new Set(
        jobs
          .map((job) => job.experience_level)
          .filter(Boolean),
      ),
    ].sort()
  }, [jobs])

  const filteredJobs = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase()
    const normalizedLocation = location.trim().toLowerCase()

    return jobs.filter((job) => {
      const searchableText = [
        job.title,
        job.description,
        job.location,
        job.employment_type,
        job.experience_level,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()

      const matchesSearch =
        !normalizedSearch ||
        searchableText.includes(normalizedSearch)

      const matchesLocation =
        !normalizedLocation ||
        job.location?.toLowerCase().includes(normalizedLocation)

      const matchesEmployment =
        !employmentType ||
        job.employment_type === employmentType

      const matchesExperience =
        !experienceLevel ||
        job.experience_level === experienceLevel

      return (
        matchesSearch &&
        matchesLocation &&
        matchesEmployment &&
        matchesExperience
      )
    })
  }, [
    jobs,
    search,
    location,
    employmentType,
    experienceLevel,
  ])

  function clearFilters() {
    setSearch('')
    setLocation('')
    setEmploymentType('')
    setExperienceLevel('')
  }

  const hasFilters =
    search ||
    location ||
    employmentType ||
    experienceLevel

  return (
    <section className="jobs-page">
      <div className="jobs-container">
        <header className="jobs-hero">
          <div>
            <span className="jobs-overline">
              HIRELY OPPORTUNITIES
            </span>

            <h1>
              Find work that
              <span> fits you.</span>
            </h1>

            <p>
              Explore active opportunities and discover roles where your
              skills and experience can make an impact.
            </p>
          </div>

          <div className="jobs-hero-decoration" aria-hidden="true">
            <div className="jobs-orbit jobs-orbit-one" />
            <div className="jobs-orbit jobs-orbit-two" />
            <div className="jobs-orbit-core">
              ✦
            </div>
          </div>
        </header>

        <section className="job-search-panel">
          <div className="job-search-main">
            <span className="search-icon" aria-hidden="true">
              ⌕
            </span>

            <input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by role, skill, or keyword..."
              aria-label="Search jobs"
            />
          </div>

          <div className="job-filter">
            <span aria-hidden="true">⌖</span>

            <input
              type="text"
              value={location}
              onChange={(event) => setLocation(event.target.value)}
              placeholder="Location"
              aria-label="Filter by location"
            />
          </div>

          <div className="job-filter">
            <span aria-hidden="true">◷</span>

            <select
              value={employmentType}
              onChange={(event) =>
                setEmploymentType(event.target.value)
              }
              aria-label="Filter by employment type"
            >
              <option value="">Employment type</option>

              {employmentTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div className="job-filter">
            <span aria-hidden="true">◎</span>

            <select
              value={experienceLevel}
              onChange={(event) =>
                setExperienceLevel(event.target.value)
              }
              aria-label="Filter by experience level"
            >
              <option value="">Experience level</option>

              {experienceLevels.map((level) => (
                <option key={level} value={level}>
                  {level}
                </option>
              ))}
            </select>
          </div>

          {hasFilters && (
            <button
              type="button"
              className="clear-filters-button"
              onClick={clearFilters}
            >
              Clear
            </button>
          )}
        </section>

        <div className="jobs-results-header">
          <div>
            <span className="jobs-results-label">
              OPEN POSITIONS
            </span>

            <h2>
              {loading
                ? 'Finding opportunities...'
                : `${filteredJobs.length} ${filteredJobs.length === 1 ? 'opportunity' : 'opportunities'}`}
            </h2>
          </div>

          <span className="jobs-results-status">
            <span />
            Live openings
          </span>
        </div>

        {error && (
          <div className="jobs-error" role="alert">
            <div className="jobs-error-icon">!</div>

            <div>
              <strong>Unable to load opportunities</strong>
              <p>{error}</p>
            </div>

            <button
              type="button"
              onClick={() => window.location.reload()}
            >
              Retry
            </button>
          </div>
        )}

        {loading ? (
          <div className="jobs-grid">
            {Array.from({ length: 6 }).map((_, index) => (
              <div
                key={index}
                className="job-skeleton"
              >
                <div className="skeleton-line skeleton-company" />
                <div className="skeleton-line skeleton-title" />
                <div className="skeleton-line skeleton-title-short" />
                <div className="skeleton-meta">
                  <div />
                  <div />
                  <div />
                </div>
                <div className="skeleton-line skeleton-description" />
                <div className="skeleton-line skeleton-description-short" />
              </div>
            ))}
          </div>
        ) : filteredJobs.length > 0 ? (
          <div className="jobs-grid">
            {filteredJobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
              />
            ))}
          </div>
        ) : (
          <div className="jobs-empty-state">
            <div className="jobs-empty-icon">
              ⌕
            </div>

            <span className="jobs-overline">
              NO MATCHES
            </span>

            <h2>
              We couldn't find that opportunity.
            </h2>

            <p>
              Try changing your search or removing one of the filters.
            </p>

            {hasFilters && (
              <button
                type="button"
                className="primary-button"
                onClick={clearFilters}
              >
                Clear filters
              </button>
            )}

            {!hasFilters && (
              <Link
                to="/"
                className="secondary-button"
              >
                Return home
              </Link>
            )}
          </div>
        )}
      </div>
    </section>
  )
}

export default Jobs