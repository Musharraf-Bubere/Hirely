import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import {
  explainCandidatesForJob,
  getRecruiterApplications,
  getRecruiterJobs,
  matchCandidatesToJob,
  updateApplicationStatus,
} from '../services/recruiter'

import './RecruiterCandidates.css'

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

function percentage(value) {
  if (value == null || Number.isNaN(Number(value))) {
    return 0
  }

  return Math.round(Number(value) * 100)
}

function scoreClass(score) {
  if (score >= 80) {
    return 'excellent'
  }

  if (score >= 60) {
    return 'good'
  }

  if (score >= 40) {
    return 'average'
  }

  return 'low'
}

function formatApplicationStatus(status) {
  if (!status) {
    return 'Applied'
  }

  return String(status)
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function getErrorMessage(error, fallback) {
  if (typeof error === 'string' && error.trim()) {
    return error
  }

  if (typeof error?.message === 'string' && error.message.trim()) {
    return error.message
  }

  if (typeof error?.detail === 'string' && error.detail.trim()) {
    return error.detail
  }

  if (typeof error?.response?.data?.detail === 'string') {
    return error.response.data.detail
  }

  if (Array.isArray(error?.detail) && error.detail.length > 0) {
    return error.detail
      .map((item) => {
        if (typeof item === 'string') {
          return item
        }

        return item?.msg || item?.message || JSON.stringify(item)
      })
      .join(', ')
  }

  return fallback
}

function CandidateInitial({ rank }) {
  return (
    <div className="candidate-rank-badge">
      <span>#</span>
      {rank}
    </div>
  )
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
  if (!skills?.length) {
    return null
  }

  return (
    <div className="candidate-skill-group">
      <span className={`candidate-skill-group-title ${type}`}>
        {title}
      </span>

      <div className="candidate-skill-list">
        {skills.map((skill) => (
          <span
            className={`candidate-skill-pill ${type}`}
            key={skill}
          >
            {type === 'matched' ? '✓' : '×'} {skill}
          </span>
        ))}
      </div>
    </div>
  )
}

function ExplanationSection({ explanation }) {
  if (!explanation) {
    return null
  }

  return (
    <div className="candidate-explanation">
      <div className="candidate-explanation-header">
        <div className="candidate-ai-icon">✦</div>

        <div>
          <span className="candidate-section-eyebrow">
            AI analysis
          </span>

          <h4>Why this candidate matches</h4>
        </div>
      </div>

      <p className="candidate-explanation-summary">
        {explanation.summary}
      </p>

      <div className="candidate-explanation-grid">
        {explanation.strengths?.length > 0 && (
          <div className="candidate-explanation-column">
            <h5>Strengths</h5>

            <ul>
              {explanation.strengths.map((strength) => (
                <li key={strength}>
                  <span>✓</span>
                  {strength}
                </li>
              ))}
            </ul>
          </div>
        )}

        {explanation.gaps?.length > 0 && (
          <div className="candidate-explanation-column">
            <h5>Gaps</h5>

            <ul>
              {explanation.gaps.map((gap) => (
                <li key={gap}>
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
          <strong>AI caveats</strong>

          <ul>
            {explanation.caveats.map((caveat) => (
              <li key={caveat}>{caveat}</li>
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
  if (!application) {
    return (
      <div className="candidate-action-panel">
        <div className="candidate-action-header">
          <div>
            <span className="candidate-section-eyebrow">
              Recruiter decision
            </span>

            <h4>Application not found</h4>
          </div>
        </div>

        <p className="candidate-action-message">
          This candidate does not have an application for this job.
          Recruiter actions are unavailable.
        </p>
      </div>
    )
  }

  const currentStatus = String(
    application.status || 'applied',
  ).toLowerCase()

  const isTerminal =
    currentStatus === 'hired' || currentStatus === 'rejected'

  const canShortlist = currentStatus === 'applied'

  const canInterview =
    currentStatus === 'applied' ||
    currentStatus === 'shortlisted'

  const canHire =
    currentStatus === 'interview'

  const canReject =
    currentStatus !== 'rejected' &&
    currentStatus !== 'hired'

  return (
    <div className="candidate-action-panel">
      <div className="candidate-action-header">
        <div>
          <span className="candidate-section-eyebrow">
            Recruiter decision
          </span>

          <h4>Application status</h4>
        </div>

        <span
          className={`candidate-status-badge status-${String(
            currentStatus,
          ).toLowerCase()}`}
        >
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
              disabled={updatingStatus}
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
              disabled={updatingStatus}
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
              disabled={updatingStatus}
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
              disabled={updatingStatus}
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
            ? 'This candidate has been hired for this application.'
            : 'This application has been rejected.'}
        </p>
      )}
    </div>
  )
}

function CandidateCard({
  result,
  explanation,
  application,
  updatingStatus,
  onStatusChange,
}) {
  const [expanded, setExpanded] = useState(false)

  return (
    <article className="candidate-match-card">
      <div className="candidate-match-card-top">
        <div className="candidate-identity">
          <CandidateInitial rank={result.rank} />

          <div>
            <span className="candidate-card-eyebrow">
              Ranked candidate
            </span>

            <h3>Candidate #{result.rank}</h3>

            <p className="candidate-id">
              ID: {String(result.candidate_id).slice(0, 12)}...
            </p>
          </div>
        </div>

        <ScoreRing score={result.overall_score} />
      </div>

      <div className="candidate-score-section">
        <div className="candidate-score-section-heading">
          <div>
            <span className="candidate-section-eyebrow">
              AI matching signals
            </span>

            <h4>Match breakdown</h4>
          </div>
        </div>

        <div className="candidate-score-grid">
          <ScoreBar
            label="Required skills"
            value={result.required_skill_score}
          />

          <ScoreBar
            label="Preferred skills"
            value={result.preferred_skill_score}
          />

          <ScoreBar
            label="Semantic similarity"
            value={result.semantic_similarity}
          />
        </div>
      </div>

      <div className="candidate-skills-section">
        <div className="candidate-section-heading">
          <span className="candidate-section-eyebrow">
            Skills
          </span>

          <h4>Skill compatibility</h4>
        </div>

        <SkillGroup
          title="Required matched"
          skills={result.required_matched}
          type="matched"
        />

        <SkillGroup
          title="Required missing"
          skills={result.required_missing}
          type="missing"
        />

        <SkillGroup
          title="Preferred matched"
          skills={result.preferred_matched}
          type="matched"
        />

        <SkillGroup
          title="Preferred missing"
          skills={result.preferred_missing}
          type="missing"
        />
      </div>

      {explanation && (
        <ExplanationSection explanation={explanation} />
      )}

      <RecruiterActionPanel
        application={application}
        updatingStatus={updatingStatus}
        onStatusChange={onStatusChange}
      />

      <div className="candidate-card-footer">
        <span className="candidate-confidence">
          {application
            ? `Application: ${formatApplicationStatus(
                application.status,
              )}`
            : explanation
              ? 'AI explanation generated'
              : 'AI ranking completed'}
        </span>

        <button
          type="button"
          className="candidate-expand-button"
          onClick={() => setExpanded((current) => !current)}
        >
          {expanded ? 'Hide details ↑' : 'View details ↓'}
        </button>
      </div>

      {expanded && (
        <div className="candidate-detail-panel">
          <div>
            <span>Overall match</span>
            <strong>{percentage(result.overall_score)}%</strong>
          </div>

          <div>
            <span>Required skill match</span>
            <strong>
              {percentage(result.required_skill_score)}%
            </strong>
          </div>

          <div>
            <span>Preferred skill match</span>
            <strong>
              {percentage(result.preferred_skill_score)}%
            </strong>
          </div>

          <div>
            <span>Semantic similarity</span>
            <strong>
              {percentage(result.semantic_similarity)}%
            </strong>
          </div>
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

function EmptyResults() {
  return (
    <section className="candidate-empty-state">
      <div className="candidate-empty-icon">✦</div>

      <span className="candidate-section-eyebrow">
        AI candidate matching
      </span>

      <h2>Ready to find your strongest candidates?</h2>

      <p>
        Hirely will analyze eligible candidate resumes against this
        job and rank them using skills, semantic similarity, and
        the matching engine.
      </p>
    </section>
  )
}

export default function RecruiterCandidates() {
  const { jobId } = useParams()

  const [job, setJob] = useState(null)
  const [results, setResults] = useState([])
  const [explanations, setExplanations] = useState({})
  const [applications, setApplications] = useState([])
  const [loadingJob, setLoadingJob] = useState(true)
  const [matching, setMatching] = useState(false)
  const [explaining, setExplaining] = useState(false)
  const [loadingApplications, setLoadingApplications] =
    useState(true)
  const [updatingApplicationId, setUpdatingApplicationId] =
    useState(null)
  const [updatingStatus, setUpdatingStatus] = useState('')
  const [actionSuccess, setActionSuccess] = useState('')
  const [error, setError] = useState('')
  const [matchCompleted, setMatchCompleted] = useState(false)

  useEffect(() => {
    let isMounted = true

    async function loadJob() {
      setLoadingJob(true)
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
          setError(
            'Job not found or you do not have access to this job.',
          )
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
          setLoadingJob(false)
        }
      }
    }

    loadJob()

    return () => {
      isMounted = false
    }
  }, [jobId])

  useEffect(() => {
    let isMounted = true

    async function loadApplications() {
      setLoadingApplications(true)

      try {
        const data = await getRecruiterApplications()

        if (!isMounted) {
          return
        }

        setApplications(Array.isArray(data) ? data : [])
      } catch (requestError) {
        if (!isMounted) {
          return
        }

        setError(
          requestError?.message ||
            'Unable to load recruiter applications.',
        )
      } finally {
        if (isMounted) {
          setLoadingApplications(false)
        }
      }
    }

    loadApplications()

    return () => {
      isMounted = false
    }
  }, [])

  async function handleRunMatching() {
    setMatching(true)
    setError('')
    setActionSuccess('')
    setExplanations({})

    try {
      const data = await matchCandidatesToJob(jobId)

      const rankedCandidates = Array.isArray(data) ? data : []

      setResults(rankedCandidates)
      setMatchCompleted(true)
    } catch (requestError) {
      setError(
        requestError?.message ||
          'Unable to run AI candidate matching.',
      )
    } finally {
      setMatching(false)
    }
  }

  async function handleGenerateExplanations() {
    setExplaining(true)
    setError('')
    setActionSuccess('')

    try {
      const data = await explainCandidatesForJob(jobId, 5)

      const finalResults = Array.isArray(data) ? data : []

      const explanationMap = {}

      finalResults.forEach((item) => {
        if (item?.candidate_id) {
          explanationMap[item.candidate_id] = item.explanation
        } else if (item?.match?.candidate_id) {
          explanationMap[item.match.candidate_id] =
            item.explanation
        }
      })

      const normalizedResults = finalResults
        .map((item) => item?.match || item)
        .filter(Boolean)

      setResults((currentResults) => {
        if (!normalizedResults.length) {
          return currentResults
        }

        return normalizedResults
      })

      setExplanations(explanationMap)
    } catch (requestError) {
      setError(
        requestError?.message ||
          'Unable to generate AI explanations.',
      )
    } finally {
      setExplaining(false)
    }
  }

  async function handleStatusChange(application, nextStatus) {
    if (!application?.id) {
      return
    }

    const normalizedStatus = String(nextStatus).toLowerCase()

    setUpdatingApplicationId(application.id)
    setUpdatingStatus(normalizedStatus)
    setError('')
    setActionSuccess('')

    try {
      const updatedApplication =
        await updateApplicationStatus(
          application.id,
          normalizedStatus,
        )

      setApplications((currentApplications) =>
        currentApplications.map((item) =>
          item.id === updatedApplication.id
            ? updatedApplication
            : item,
        ),
      )

      setActionSuccess(
        `Application moved to ${formatApplicationStatus(
          updatedApplication.status,
        )}.`,
      )
    } catch (requestError) {
      setError(
        getErrorMessage(
          requestError,
          'Unable to update application status.',
        ),
      )
    } finally {
      setUpdatingApplicationId(null)
      setUpdatingStatus('')
    }
  }

  function getApplicationForCandidate(candidateId) {
    return applications.find(
      (application) =>
        String(application.candidate_id) === String(candidateId) &&
        String(application.job_id) === String(jobId),
    )
  }

  const topMatch = useMemo(() => {
    if (!results.length) {
      return null
    }

    return [...results].sort(
      (first, second) =>
        Number(second.overall_score) -
        Number(first.overall_score),
    )[0]
  }, [results])

  if (loadingJob) {
    return (
      <main className="recruiter-candidates-page">
        <div className="candidate-page-loading">
          <div className="candidate-loading-orb">✦</div>
          <h2>Preparing hiring workspace...</h2>
          <p>Loading the selected job.</p>
        </div>
      </main>
    )
  }

  if (error && !job) {
    return (
      <main className="recruiter-candidates-page">
        <section className="candidate-page-error">
          <div className="candidate-error-icon">!</div>

          <span className="candidate-section-eyebrow">
            Candidate matching
          </span>

          <h1>Unable to open candidate matching</h1>

          <p>{error}</p>

          <Link
            to="/recruiter/jobs"
            className="candidate-primary-button"
          >
            Back to Jobs
          </Link>
        </section>
      </main>
    )
  }

  return (
    <main className="recruiter-candidates-page">
      <section className="candidate-page-header">
        <div className="candidate-header-main">
          <Link
            to={`/recruiter/jobs/${job.id}`}
            className="candidate-back-link"
          >
            ← Back to Job
          </Link>

          <span className="candidate-section-eyebrow">
            Recruiter intelligence
          </span>

          <h1>Find Candidates</h1>

          <p>
            Use Hirely AI to identify, rank, and evaluate the
            strongest candidates for <strong>{job.title}</strong>.
          </p>
        </div>

        <div className="candidate-header-actions">
          <button
            type="button"
            className="candidate-primary-button"
            onClick={handleRunMatching}
            disabled={matching}
          >
            {matching ? (
              <>
                <span className="candidate-button-spinner" />
                Matching candidates...
              </>
            ) : (
              <>✦ Run AI Matching</>
            )}
          </button>
        </div>
      </section>

      <section className="candidate-job-summary">
        <div className="candidate-job-summary-icon">
          {job.title?.slice(0, 2).toUpperCase() || 'JB'}
        </div>

        <div className="candidate-job-summary-main">
          <span className="candidate-card-eyebrow">
            Matching against
          </span>

          <h2>{job.title}</h2>

          <div className="candidate-job-meta">
            <span>⌖ {job.location || 'Remote / Flexible'}</span>
            <span>
              ◉ {formatEmploymentType(job.employment_type)}
            </span>
            <span>
              ◌ {formatExperienceLevel(job.experience_level)}
            </span>
            <span>
              ₹ {formatSalary(job.salary_min, job.salary_max)}
            </span>
          </div>
        </div>

        {topMatch && (
          <div className="candidate-top-match">
            <span>Top match</span>
            <strong>
              {percentage(topMatch.overall_score)}%
            </strong>
          </div>
        )}
      </section>

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

      <section className="candidate-results-section">
        <div className="candidate-results-header">
          <div>
            <span className="candidate-section-eyebrow">
              Candidate intelligence
            </span>

            <h2>Ranked candidates</h2>

            <p>
              {matchCompleted
                ? `${results.length} eligible candidate${
                    results.length === 1 ? '' : 's'
                  } ranked by Hirely AI.`
                : 'Run AI matching to generate your candidate ranking.'}
            </p>
          </div>

          {matchCompleted && results.length > 0 && (
            <button
              type="button"
              className="candidate-secondary-button"
              onClick={handleGenerateExplanations}
              disabled={explaining}
            >
              {explaining ? (
                <>
                  <span className="candidate-button-spinner dark" />
                  Generating explanations...
                </>
              ) : (
                <>✦ Generate AI Explanations</>
              )}
            </button>
          )}
        </div>

        {matching && <CandidateListSkeleton />}

        {!matching && !matchCompleted && <EmptyResults />}

        {!matching &&
          matchCompleted &&
          results.length === 0 && (
            <section className="candidate-empty-state">
              <div className="candidate-empty-icon">⌕</div>

              <span className="candidate-section-eyebrow">
                No eligible candidates
              </span>

              <h2>No candidates could be ranked</h2>

              <p>
                Hirely could not find candidates with an eligible
                completed resume for this matching workflow.
              </p>
            </section>
          )}

        {!matching && results.length > 0 && (
          <div className="candidate-results-list">
            {results.map((result) => {
              const application =
                getApplicationForCandidate(result.candidate_id)

              const isUpdating =
                updatingApplicationId === application?.id

              return (
                <CandidateCard
                  key={result.candidate_id}
                  result={result}
                  explanation={
                    explanations[result.candidate_id] || null
                  }
                  application={application}
                  updatingStatus={
                    isUpdating ? updatingStatus : ''
                  }
                  onStatusChange={(nextStatus) =>
                    handleStatusChange(
                      application,
                      nextStatus,
                    )
                  }
                />
              )
            })}
          </div>
        )}

        {loadingApplications && matchCompleted && (
          <p className="candidate-application-loading">
            Loading application status...
          </p>
        )}
      </section>
    </main>
  )
}