import { useEffect, useMemo, useState, useCallback } from 'react'
import { Link, useParams } from 'react-router-dom'

import {
  getCandidateIntelligence,
  getRecruiterJobs,
  updateApplicationStatus,
} from '../services/recruiter'

import './RecruiterCandidates.css'

function formatEmploymentType(value) {
  if (!value) return 'Not specified'
  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

function formatExperienceLevel(value) {
  if (!value) return 'Not specified'
  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

function formatSalary(min, max) {
  if (min == null && max == null) return 'Salary not specified'
  const formatAmount = (amt) => new Intl.NumberFormat('en-IN').format(amt)
  if (min != null && max != null) return `₹${formatAmount(min)} – ₹${formatAmount(max)}`
  if (min != null) return `From ₹${formatAmount(min)}`
  return `Up to ₹${formatAmount(max)}`
}

function percentage(value) {
  if (value == null || Number.isNaN(Number(value))) return 0
  return Math.round(Number(value) * 100)
}

function scoreClass(score) {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'average'
  return 'low'
}

function formatApplicationStatus(status) {
  if (!status) return 'Not Applied'
  return String(status)
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

function getInitials(name) {
  if (!name) return 'CD'
  const parts = name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return parts[0].slice(0, 2).toUpperCase()
}

function ScoreRing({ score }) {
  const value = percentage(score)
  return (
    <div className={`candidate-score-ring ${scoreClass(value)}`}>
      <div className="candidate-score-ring-inner">
        <strong>{value}%</strong>
        <span>Match</span>
      </div>
    </div>
  )
}

function ScoreBar({ label, value }) {
  const score = percentage(value)
  return (
    <div className="candidate-score-bar-row">
      <div className="candidate-score-bar-header">
        <span>{label}</span>
        <strong>{score}%</strong>
      </div>
      <div className="candidate-score-bar-track">
        <div
          className={`candidate-score-bar-fill ${scoreClass(score)}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  )
}

function SkillGroup({ title, skills, type }) {
  if (!skills?.length) return null
  return (
    <div className="candidate-skill-group">
      <span className={`candidate-skill-group-title ${type}`}>{title}</span>
      <div className="candidate-skill-list">
        {skills.map((skill) => (
          <span className={`candidate-skill-pill ${type}`} key={skill}>
            {type === 'matched' ? '✓' : '×'} {skill}
          </span>
        ))}
      </div>
    </div>
  )
}

function ExplanationSection({ explanation }) {
  if (!explanation) return null
  return (
    <div className="candidate-explanation">
      <div className="candidate-explanation-header">
        <div className="candidate-ai-icon">✦</div>
        <div>
          <span className="candidate-section-eyebrow">AI Match Analysis</span>
          <h4>Why this candidate matches</h4>
        </div>
      </div>

      <p className="candidate-explanation-summary">{explanation.summary}</p>

      <div className="candidate-explanation-grid">
        {explanation.strengths?.length > 0 && (
          <div className="candidate-explanation-column">
            <h5>Key Strengths</h5>
            <ul>
              {explanation.strengths.map((str, idx) => (
                <li key={`str-${idx}`}>
                  <span>✓</span>
                  {str}
                </li>
              ))}
            </ul>
          </div>
        )}

        {explanation.gaps?.length > 0 && (
          <div className="candidate-explanation-column">
            <h5>Skill / Experience Gaps</h5>
            <ul>
              {explanation.gaps.map((gap, idx) => (
                <li key={`gap-${idx}`}>
                  <span>!</span>
                  {gap}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {explanation.caveats?.length > 0 && (
        <div className="candidate-caveats">
          <strong>Advisory Considerations</strong>
          <ul>
            {explanation.caveats.map((cav, idx) => (
              <li key={`cav-${idx}`}>{cav}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function RecruiterActionPanel({
  application,
  updatingStatus,
  onStatusChange,
}) {
  if (!application?.application_id) {
    return (
      <div className="candidate-action-panel">
        <div className="candidate-action-header">
          <div>
            <span className="candidate-section-eyebrow">Recruiter Status</span>
            <h4>Application Status</h4>
          </div>
          <span className="candidate-status-badge status-not-applied">
            Not Applied
          </span>
        </div>
        <p className="candidate-action-message">
          This candidate matches your job criteria from Hirely&apos;s talent pool, but has not yet submitted a direct application for this role.
        </p>
      </div>
    )
  }

  const currentStatus = String(application.status || 'applied').toLowerCase()
  const isTerminal = currentStatus === 'hired' || currentStatus === 'rejected'
  const canShortlist = currentStatus === 'applied'
  const canInterview = currentStatus === 'applied' || currentStatus === 'shortlisted'
  const canHire = currentStatus === 'interview'
  const canReject = currentStatus !== 'rejected' && currentStatus !== 'hired'

  return (
    <div className="candidate-action-panel">
      <div className="candidate-action-header">
        <div>
          <span className="candidate-section-eyebrow">Recruiter Decision</span>
          <h4>Application Status</h4>
        </div>
        <span className={`candidate-status-badge status-${currentStatus}`}>
          {formatApplicationStatus(currentStatus)}
        </span>
      </div>

      {!isTerminal && (
        <div className="candidate-action-buttons">
          {canShortlist && (
            <button
              type="button"
              className="candidate-action-button shortlist"
              onClick={() => onStatusChange('shortlisted')}
              disabled={Boolean(updatingStatus)}
            >
              {updatingStatus === 'shortlisted' ? (
                <>
                  <span className="candidate-action-spinner" />
                  Updating...
                </>
              ) : (
                <>✓ Shortlist</>
              )}
            </button>
          )}

          {canInterview && (
            <button
              type="button"
              className="candidate-action-button interview"
              onClick={() => onStatusChange('interview')}
              disabled={Boolean(updatingStatus)}
            >
              {updatingStatus === 'interview' ? (
                <>
                  <span className="candidate-action-spinner" />
                  Updating...
                </>
              ) : (
                <>◉ Move to Interview</>
              )}
            </button>
          )}

          {canHire && (
            <button
              type="button"
              className="candidate-action-button hire"
              onClick={() => onStatusChange('hired')}
              disabled={Boolean(updatingStatus)}
            >
              {updatingStatus === 'hired' ? (
                <>
                  <span className="candidate-action-spinner" />
                  Updating...
                </>
              ) : (
                <>★ Hire Candidate</>
              )}
            </button>
          )}

          {canReject && (
            <button
              type="button"
              className="candidate-action-button reject"
              onClick={() => onStatusChange('rejected')}
              disabled={Boolean(updatingStatus)}
            >
              {updatingStatus === 'rejected' ? (
                <>
                  <span className="candidate-action-spinner" />
                  Updating...
                </>
              ) : (
                <>× Reject</>
              )}
            </button>
          )}
        </div>
      )}

      {isTerminal && (
        <p className="candidate-action-message">
          {currentStatus === 'hired'
            ? 'Candidate has been marked as Hired for this position.'
            : 'Candidate application was marked as Rejected.'}
        </p>
      )}
    </div>
  )
}

function CandidateCard({
  item,
  updatingStatus,
  onStatusChange,
}) {
  const [expanded, setExpanded] = useState(false)
  const cand = item.candidate

  return (
    <article className="candidate-match-card">
      <div className="candidate-match-card-top">
        <div className="candidate-identity">
          <div className="candidate-avatar">
            {getInitials(cand.full_name)}
          </div>
          <div>
            <div className="candidate-rank-row">
              <span className="candidate-rank-tag">#{item.rank} Match</span>
              {cand.location && (
                <span className="candidate-location-tag">⌖ {cand.location}</span>
              )}
            </div>
            <h3 className="candidate-name">{cand.full_name}</h3>
            {cand.headline && (
              <p className="candidate-headline">{cand.headline}</p>
            )}
          </div>
        </div>

        <ScoreRing score={item.overall_score} />
      </div>

      {/* Profile Experience & Education Snippet */}
      {(cand.experience?.length > 0 || cand.education?.length > 0) && (
        <div className="candidate-snippet-row">
          {cand.experience?.length > 0 && (
            <div className="candidate-snippet-item">
              <span className="candidate-snippet-label">Recent Role:</span>
              <strong>
                {cand.experience[0].job_title}
                {cand.experience[0].company ? ` at ${cand.experience[0].company}` : ''}
              </strong>
            </div>
          )}
          {cand.education?.length > 0 && (
            <div className="candidate-snippet-item">
              <span className="candidate-snippet-label">Education:</span>
              <span>
                {cand.education[0].degree}
                {cand.education[0].institution ? ` (${cand.education[0].institution})` : ''}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Match Signals Breakdown */}
      <div className="candidate-score-section">
        <div className="candidate-score-section-heading">
          <div>
            <span className="candidate-section-eyebrow">Match Signals</span>
            <h4>Deterministic Compatibility Breakdown</h4>
          </div>
        </div>

        <div className="candidate-score-grid">
          <ScoreBar
            label="Required skills"
            value={item.required_skill_score}
          />
          <ScoreBar
            label="Preferred skills"
            value={item.preferred_skill_score}
          />
          <ScoreBar
            label="Semantic similarity"
            value={item.semantic_similarity}
          />
        </div>
      </div>

      {/* Skill Compatibility */}
      <div className="candidate-skills-section">
        <div className="candidate-section-heading">
          <span className="candidate-section-eyebrow">Skill Alignment</span>
          <h4>Required & Preferred Skills</h4>
        </div>

        <SkillGroup
          title="Required Skills Matched"
          skills={item.required_matched}
          type="matched"
        />
        <SkillGroup
          title="Required Skills Missing"
          skills={item.required_missing}
          type="missing"
        />
        <SkillGroup
          title="Preferred Skills Matched"
          skills={item.preferred_matched}
          type="matched"
        />
        <SkillGroup
          title="Preferred Skills Missing"
          skills={item.preferred_missing}
          type="missing"
        />
      </div>

      {/* AI Explanation (if available) */}
      {item.explanation && (
        <ExplanationSection explanation={item.explanation} />
      )}

      {/* Recruiter Action Panel */}
      <RecruiterActionPanel
        application={item.application}
        updatingStatus={updatingStatus}
        onStatusChange={onStatusChange}
      />

      {/* Card Footer & Drawer Toggle */}
      <div className="candidate-card-footer">
        <span className="candidate-confidence">
          {item.application
            ? `Status: ${formatApplicationStatus(item.application.status)}`
            : item.explanation
              ? 'AI Explanation Generated'
              : 'Deterministic Match Verified'}
        </span>

        <button
          type="button"
          className="candidate-expand-button"
          onClick={() => setExpanded((prev) => !prev)}
        >
          {expanded ? 'Hide Full Qualifications ↑' : 'View Full Qualifications ↓'}
        </button>
      </div>

      {/* Full Qualifications Drawer */}
      {expanded && (
        <div className="candidate-detail-panel">
          {cand.bio && (
            <div className="candidate-detail-section">
              <h5>Candidate Bio</h5>
              <p>{cand.bio}</p>
            </div>
          )}

          {cand.skills?.length > 0 && (
            <div className="candidate-detail-section">
              <h5>All Verified Skills ({cand.skills.length})</h5>
              <div className="candidate-all-skills-wrapper">
                {cand.skills.map((sk) => (
                  <span key={sk} className="candidate-all-skill-tag">
                    {sk}
                  </span>
                ))}
              </div>
            </div>
          )}

          {cand.experience?.length > 0 && (
            <div className="candidate-detail-section">
              <h5>Work History</h5>
              <div className="candidate-work-history">
                {cand.experience.map((exp, idx) => (
                  <div key={`exp-${idx}`} className="candidate-history-item">
                    <div className="candidate-history-title-row">
                      <strong>{exp.job_title || 'Position'}</strong>
                      <span>{exp.company || 'Organization'}</span>
                    </div>
                    {(exp.start_date || exp.end_date) && (
                      <span className="candidate-history-dates">
                        {exp.start_date || '—'} to {exp.end_date || 'Present'}
                      </span>
                    )}
                    {exp.description && (
                      <p className="candidate-history-desc">{exp.description}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {cand.education?.length > 0 && (
            <div className="candidate-detail-section">
              <h5>Education</h5>
              <div className="candidate-education-list">
                {cand.education.map((edu, idx) => (
                  <div key={`edu-${idx}`} className="candidate-education-item">
                    <strong>{edu.degree || 'Degree'}</strong>
                    <span>
                      {edu.institution}
                      {edu.field_of_study ? ` • ${edu.field_of_study}` : ''}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </article>
  )
}

function CandidateListSkeleton() {
  return (
    <div className="candidate-results-list">
      {[1, 2, 3].map((item) => (
        <div className="candidate-skeleton-card" key={item}>
          <div className="candidate-skeleton candidate-skeleton-avatar" />
          <div className="candidate-skeleton-content">
            <div className="candidate-skeleton candidate-skeleton-title" />
            <div className="candidate-skeleton candidate-skeleton-line" />
            <div className="candidate-skeleton candidate-skeleton-line short" />
            <div className="candidate-skeleton candidate-skeleton-score" />
          </div>
        </div>
      ))}
    </div>
  )
}

export default function RecruiterCandidates() {
  const { jobId } = useParams()

  const [job, setJob] = useState(null)
  const [intelligence, setIntelligence] = useState(null)
  const [loadingJob, setLoadingJob] = useState(true)
  const [loadingIntelligence, setLoadingIntelligence] = useState(false)
  const [updatingApplicationId, setUpdatingApplicationId] = useState(null)
  const [updatingStatus, setUpdatingStatus] = useState('')
  const [actionSuccess, setActionSuccess] = useState('')
  const [error, setError] = useState('')

  // Search & Filter State
  const [searchQuery, setSearchQuery] = useState('')
  const [minScore, setMinScore] = useState('all')
  const [selectedSkill, setSelectedSkill] = useState('all')
  const [selectedStatus, setSelectedStatus] = useState('all')
  const [sortBy, setSortBy] = useState('overall_score')
  const [sortOrder, setSortOrder] = useState('desc')

  // Load Job Details & Initial Candidate Intelligence
  useEffect(() => {
    let isMounted = true

    async function loadWorkspace() {
      setLoadingJob(true)
      setLoadingIntelligence(true)
      setError('')

      try {
        const data = await getRecruiterJobs()
        if (!isMounted) return

        const jobs = Array.isArray(data) ? data : []
        const foundJob = jobs.find((item) => String(item.id) === String(jobId))

        if (!foundJob) {
          setError('Job not found or you do not have permission to view candidate intelligence for this job.')
          setJob(null)
          return
        }

        setJob(foundJob)

        const intelData = await getCandidateIntelligence(jobId, {
          query: null,
          min_score: null,
          skill: null,
          application_status: null,
          sort_by: 'overall_score',
          sort_order: 'desc',
          include_explanations: true,
          explanation_limit: 5,
        })
        if (!isMounted) return
        setIntelligence(intelData)
      } catch (err) {
        if (!isMounted) return
        setError(err?.message || 'Unable to load candidate intelligence workspace.')
      } finally {
        if (isMounted) {
          setLoadingJob(false)
          setLoadingIntelligence(false)
        }
      }
    }

    loadWorkspace()
    return () => {
      isMounted = false
    }
  }, [jobId])

  // Fetch Candidate Intelligence
  const fetchIntelligence = useCallback(async (customFilters = {}) => {
    if (!jobId) return

    setLoadingIntelligence(true)
    setError('')
    setActionSuccess('')

    const payload = {
      query: customFilters.query !== undefined ? customFilters.query : (searchQuery.trim() || null),
      min_score: (customFilters.minScore !== undefined ? customFilters.minScore : minScore) !== 'all'
        ? Number(customFilters.minScore || minScore)
        : null,
      skill: (customFilters.selectedSkill !== undefined ? customFilters.selectedSkill : selectedSkill) !== 'all'
        ? (customFilters.selectedSkill || selectedSkill)
        : null,
      application_status: (customFilters.selectedStatus !== undefined ? customFilters.selectedStatus : selectedStatus) !== 'all'
        ? (customFilters.selectedStatus || selectedStatus)
        : null,
      sort_by: customFilters.sortBy || sortBy,
      sort_order: customFilters.sortOrder || sortOrder,
      include_explanations: true,
      explanation_limit: 5,
    }

    try {
      const data = await getCandidateIntelligence(jobId, payload)
      setIntelligence(data)
    } catch (err) {
      setError(
        err?.message ||
          'Unable to retrieve candidate intelligence. Please ensure candidate profiles and resumes are available.',
      )
    } finally {
      setLoadingIntelligence(false)
    }
  }, [jobId, searchQuery, minScore, selectedSkill, selectedStatus, sortBy, sortOrder])

  // Handle application status change
  async function handleStatusChange(application, nextStatus) {
    if (!application?.application_id) return

    const normalizedStatus = String(nextStatus).toLowerCase()
    setUpdatingApplicationId(application.application_id)
    setUpdatingStatus(normalizedStatus)
    setError('')
    setActionSuccess('')

    try {
      const updated = await updateApplicationStatus(application.application_id, normalizedStatus)

      // Update in-memory intelligence state
      setIntelligence((prev) => {
        if (!prev) return prev
        const updatedResults = prev.results.map((item) => {
          if (item.application?.application_id === application.application_id) {
            return {
              ...item,
              application: {
                ...item.application,
                status: updated.status,
              },
            }
          }
          return item
        })
        return {
          ...prev,
          results: updatedResults,
        }
      })

      setActionSuccess(`Application status moved to ${formatApplicationStatus(updated.status)}.`)
    } catch (err) {
      setError(err?.message || 'Unable to update candidate application status.')
    } finally {
      setUpdatingApplicationId(null)
      setUpdatingStatus('')
    }
  }

  // Handle filter reset
  function handleResetFilters() {
    setSearchQuery('')
    setMinScore('all')
    setSelectedSkill('all')
    setSelectedStatus('all')
    setSortBy('overall_score')
    setSortOrder('desc')

    fetchIntelligence({
      query: null,
      minScore: 'all',
      selectedSkill: 'all',
      selectedStatus: 'all',
      sortBy: 'overall_score',
      sortOrder: 'desc',
    })
  }

  const hasActiveFilters = useMemo(() => {
    return (
      Boolean(searchQuery.trim()) ||
      minScore !== 'all' ||
      selectedSkill !== 'all' ||
      selectedStatus !== 'all' ||
      sortBy !== 'overall_score'
    )
  }, [searchQuery, minScore, selectedSkill, selectedStatus, sortBy])

  const topMatch = useMemo(() => {
    if (!intelligence?.results?.length) return null
    return [...intelligence.results].sort(
      (a, b) => Number(b.overall_score) - Number(a.overall_score),
    )[0]
  }, [intelligence])

  if (loadingJob) {
    return (
      <main className="recruiter-candidates-page">
        <div className="candidate-page-loading">
          <div className="candidate-loading-orb">✦</div>
          <h2>Preparing Hiring Workspace...</h2>
          <p>Loading candidate intelligence environment.</p>
        </div>
      </main>
    )
  }

  if (error && !job) {
    return (
      <main className="recruiter-candidates-page">
        <section className="candidate-page-error">
          <div className="candidate-error-icon">!</div>
          <span className="candidate-section-eyebrow">Candidate Intelligence</span>
          <h1>Unable to open workspace</h1>
          <p>{error}</p>
          <Link to="/recruiter/jobs" className="candidate-primary-button">
            Back to Jobs
          </Link>
        </section>
      </main>
    )
  }

  return (
    <main className="recruiter-candidates-page">
      {/* Header */}
      <section className="candidate-page-header">
        <div className="candidate-header-main">
          <Link to={`/recruiter/jobs/${job.id}`} className="candidate-back-link">
            ← Back to Job Detail
          </Link>
          <span className="candidate-section-eyebrow">
            Recruiter AI • Candidate Search & Intelligence
          </span>
          <h1>Candidate Intelligence</h1>
          <p>
            Search, filter, and rank qualified talent for{' '}
            <strong>{job.title}</strong> using deterministic skill alignment, semantic relevance, and AI insights.
          </p>
        </div>

        <div className="candidate-header-actions">
          <button
            type="button"
            className="candidate-primary-button"
            onClick={() => fetchIntelligence()}
            disabled={loadingIntelligence}
            title="Refresh candidate ranking with current filters"
          >
            {loadingIntelligence ? (
              <>
                <span className="candidate-button-spinner" />
                Analyzing candidates...
              </>
            ) : (
              <>↻ Refresh Intelligence</>
            )}
          </button>
        </div>
      </section>

      {/* Target Job Summary Banner */}
      <section className="candidate-job-summary">
        <div className="candidate-job-summary-icon">
          {job.title?.slice(0, 2).toUpperCase() || 'JB'}
        </div>

        <div className="candidate-job-summary-main">
          <span className="candidate-card-eyebrow">Target Opportunity</span>
          <h2>{job.title}</h2>
          <div className="candidate-job-meta">
            <span>⌖ {job.location || 'Remote / Flexible'}</span>
            <span>◉ {formatEmploymentType(job.employment_type)}</span>
            <span>◌ {formatExperienceLevel(job.experience_level)}</span>
            <span>₹ {formatSalary(job.salary_min, job.salary_max)}</span>
          </div>
        </div>

        <div className="candidate-job-summary-stats">
          {topMatch && (
            <div className="candidate-top-match">
              <span>Top Match</span>
              <strong>{percentage(topMatch.overall_score)}%</strong>
            </div>
          )}
          {intelligence && (
            <div className="candidate-stat-pill">
              <span>Pool Size</span>
              <strong>{intelligence.total_candidates}</strong>
            </div>
          )}
        </div>
      </section>

      {/* Advisory Banner */}
      <div className="candidate-advisory-banner">
        <span className="candidate-advisory-badge">Assistive Intelligence</span>
        <p>
          {intelligence?.disclaimer ||
            'Match scores and rankings are calculated deterministically by Hirely based on verified skills and semantic relevance. AI explanations are advisory.'}
        </p>
      </div>

      {/* Error & Success Messages */}
      {error && (
        <div className="candidate-inline-error">
          <span>!</span>
          <p>{error}</p>
        </div>
      )}

      {actionSuccess && (
        <div className="candidate-inline-success">
          <span>✓</span>
          <p>{actionSuccess}</p>
        </div>
      )}

      {/* Search & Filter Toolbar */}
      <section className="candidate-filter-toolbar">
        <div className="candidate-search-row">
          <div className="candidate-search-input-wrap">
            <span className="candidate-search-icon">🔍</span>
            <input
              type="text"
              className="candidate-search-input"
              placeholder="Search by candidate name, headline, skills, or company..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') fetchIntelligence()
              }}
            />
            {searchQuery && (
              <button
                type="button"
                className="candidate-search-clear"
                onClick={() => {
                  setSearchQuery('')
                  fetchIntelligence({ query: null })
                }}
              >
                ✕
              </button>
            )}
          </div>
          <button
            type="button"
            className="candidate-apply-search-btn"
            onClick={() => fetchIntelligence()}
          >
            Search
          </button>
        </div>

        <div className="candidate-filters-grid">
          {/* Min Score Filter */}
          <div className="candidate-filter-item">
            <label htmlFor="filter-score">Min Match Score:</label>
            <select
              id="filter-score"
              value={minScore}
              onChange={(e) => {
                const val = e.target.value
                setMinScore(val)
                fetchIntelligence({ minScore: val })
              }}
            >
              <option value="all">All Match Scores</option>
              <option value="0.80">≥ 80% (Exceptional Match)</option>
              <option value="0.60">≥ 60% (Strong Match)</option>
              <option value="0.40">≥ 40% (Moderate Match)</option>
            </select>
          </div>

          {/* Skill Filter */}
          <div className="candidate-filter-item">
            <label htmlFor="filter-skill">Skill Alignment:</label>
            <select
              id="filter-skill"
              value={selectedSkill}
              onChange={(e) => {
                const val = e.target.value
                setSelectedSkill(val)
                fetchIntelligence({ selectedSkill: val })
              }}
            >
              <option value="all">All Skills</option>
              {(intelligence?.available_skills || []).map((sk) => (
                <option key={sk} value={sk}>
                  {sk}
                </option>
              ))}
            </select>
          </div>

          {/* Application Status Filter */}
          <div className="candidate-filter-item">
            <label htmlFor="filter-status">Application Status:</label>
            <select
              id="filter-status"
              value={selectedStatus}
              onChange={(e) => {
                const val = e.target.value
                setSelectedStatus(val)
                fetchIntelligence({ selectedStatus: val })
              }}
            >
              <option value="all">All Candidates</option>
              <option value="applied">Applied</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="interview">Interviewing</option>
              <option value="hired">Hired</option>
              <option value="rejected">Rejected</option>
              <option value="not_applied">Not Applied Yet</option>
            </select>
          </div>

          {/* Sort By */}
          <div className="candidate-filter-item">
            <label htmlFor="filter-sort">Sort By:</label>
            <select
              id="filter-sort"
              value={sortBy}
              onChange={(e) => {
                const val = e.target.value
                setSortBy(val)
                fetchIntelligence({ sortBy: val })
              }}
            >
              <option value="overall_score">Highest Match Score</option>
              <option value="required_skills">Required Skills Match</option>
              <option value="semantic_similarity">Semantic Similarity</option>
              <option value="name">Candidate Name</option>
            </select>
          </div>

          {/* Reset Filters */}
          {hasActiveFilters && (
            <button
              type="button"
              className="candidate-reset-filters-btn"
              onClick={handleResetFilters}
            >
              Reset Filters ✕
            </button>
          )}
        </div>
      </section>

      {/* Results Header */}
      <section className="candidate-results-section">
        <div className="candidate-results-header">
          <div>
            <span className="candidate-section-eyebrow">Ranked Talent</span>
            <h2>Candidate Intelligence Results</h2>
            <p>
              {loadingIntelligence
                ? 'Evaluating candidate pool against job criteria...'
                : intelligence
                  ? `Showing ${intelligence.matched_count} of ${intelligence.total_candidates} eligible candidates.`
                  : 'Run matching to view candidate intelligence.'}
            </p>
          </div>
        </div>

        {/* Loading State */}
        {loadingIntelligence && <CandidateListSkeleton />}

        {/* Empty State: No eligible candidates in DB */}
        {!loadingIntelligence && intelligence && intelligence.total_candidates === 0 && (
          <section className="candidate-empty-state">
            <div className="candidate-empty-icon">⌕</div>
            <span className="candidate-section-eyebrow">Candidate Pool</span>
            <h2>No Eligible Candidates Available</h2>
            <p>
              Hirely could not find any candidates with an active, parsed resume in the platform. Once candidates upload and parse resumes, they will be ranked automatically.
            </p>
          </section>
        )}

        {/* Empty State: Filters yielded 0 results */}
        {!loadingIntelligence && intelligence && intelligence.total_candidates > 0 && intelligence.matched_count === 0 && (
          <section className="candidate-empty-state">
            <div className="candidate-empty-icon">⌕</div>
            <span className="candidate-section-eyebrow">Zero Matches</span>
            <h2>No Candidates Match Your Active Filters</h2>
            <p>
              Try expanding your criteria, clearing the search query, or adjusting the minimum score threshold.
            </p>
            <button
              type="button"
              className="candidate-secondary-button"
              onClick={handleResetFilters}
            >
              Clear All Filters
            </button>
          </section>
        )}

        {/* Candidate Cards List */}
        {!loadingIntelligence && intelligence && intelligence.results.length > 0 && (
          <div className="candidate-results-list">
            {intelligence.results.map((item) => (
              <CandidateCard
                key={item.candidate.id}
                item={item}
                updatingStatus={
                  updatingApplicationId === item.application?.application_id ? updatingStatus : ''
                }
                onStatusChange={(nextStatus) =>
                  handleStatusChange(item.application, nextStatus)
                }
              />
            ))}
          </div>
        )}
      </section>
    </main>
  )
}