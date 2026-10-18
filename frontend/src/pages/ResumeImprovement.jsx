import { useEffect, useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

import { getJob } from '../services/jobs'
import { getResumeImprovement } from '../services/resumeImprovement'

import './ResumeImprovement.css'

function formatPercentage(value) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return 0
  }
  return Math.round(Math.max(0, Math.min(1, value)) * 100)
}

function getScoreLabel(score) {
  if (score >= 85) return 'Excellent match'
  if (score >= 70) return 'Strong match'
  if (score >= 55) return 'Moderate match'
  return 'Needs improvement'
}

function getPriorityClass(priority) {
  switch (priority?.toLowerCase()) {
    case 'high':
      return 'priority-badge-high'
    case 'medium':
      return 'priority-badge-medium'
    case 'low':
      return 'priority-badge-low'
    default:
      return 'priority-badge-medium'
  }
}

function getStatusBadge(status) {
  switch (status?.toLowerCase()) {
    case 'strong':
      return {
        label: 'Strong',
        className: 'section-badge-strong',
        icon: '✓',
      }
    case 'needs_improvement':
      return {
        label: 'Needs Attention',
        className: 'section-badge-warning',
        icon: '!',
      }
    case 'missing':
      return {
        label: 'Missing Section',
        className: 'section-badge-missing',
        icon: '✕',
      }
    default:
      return {
        label: status || 'Evaluated',
        className: 'section-badge-default',
        icon: '•',
      }
  }
}

function ResumeImprovement() {
  const [searchParams] = useSearchParams()
  const jobId = searchParams.get('job_id')

  const [job, setJob] = useState(null)
  const [jobLoading, setJobLoading] = useState(true)
  const [jobError, setJobError] = useState('')

  const [improvement, setImprovement] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [improvementError, setImprovementError] = useState('')
  const [copiedActionIndex, setCopiedActionIndex] = useState(null)
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [activeTab, setActiveTab] = useState('actions')

  useEffect(() => {
    let ignore = false

    async function loadJob() {
      if (!jobId) {
        setJobLoading(false)
        setJobError('No opportunity was selected for resume improvement.')
        return
      }

      try {
        setJobLoading(true)
        setJobError('')

        const data = await getJob(jobId)

        if (!ignore) {
          setJob(data)
        }
      } catch (err) {
        if (!ignore) {
          setJobError(
            err.message || 'Unable to load the selected opportunity.',
          )
        }
      } finally {
        if (!ignore) {
          setJobLoading(false)
        }
      }
    }

    loadJob()

    return () => {
      ignore = true
    }
  }, [jobId])

  async function handleGenerateImprovements() {
    if (!jobId) {
      setImprovementError('No opportunity was selected for resume improvement.')
      return
    }

    try {
      setGenerating(true)
      setImprovementError('')

      const response = await getResumeImprovement(jobId)

      if (!response || !response.resume_improvement) {
        setImprovementError(
          'The Resume Improvement service returned an incomplete response.',
        )
        return
      }

      setImprovement(response.resume_improvement)
    } catch (err) {
      setImprovementError(
        err.message ||
          'Unable to generate resume improvements. Please check that your active resume is uploaded and parsed.',
      )
    } finally {
      setGenerating(false)
    }
  }

  async function handleCopyText(text, index) {
    if (!text) return

    try {
      await navigator.clipboard.writeText(text)
      setCopiedActionIndex(index)
      setTimeout(() => {
        setCopiedActionIndex(null)
      }, 2000)
    } catch {
      // Fallback
    }
  }

  // Filter prioritized actions
  const filteredActions = useMemo(() => {
    const actions = Array.isArray(improvement?.prioritized_actions)
      ? improvement.prioritized_actions
      : []

    if (priorityFilter === 'all') {
      return actions
    }

    return actions.filter(
      (action) =>
        action.priority?.toLowerCase() === priorityFilter.toLowerCase(),
    )
  }, [improvement, priorityFilter])

  // Deterministic ATS score calculations
  const atsScore =
    typeof improvement?.ats_score === 'number' ? improvement.ats_score : null

  const scoreBreakdown = improvement?.score_breakdown
  const requiredScore = formatPercentage(scoreBreakdown?.required_skill_score)
  const preferredScore = formatPercentage(scoreBreakdown?.preferred_skill_score)
  const semanticScore = formatPercentage(
    scoreBreakdown?.semantic_relevance_score,
  )
  const completenessScore = formatPercentage(
    scoreBreakdown?.resume_completeness_score,
  )

  const missingRequired = Array.isArray(improvement?.missing_required_skills)
    ? improvement.missing_required_skills
    : []

  const missingPreferred = Array.isArray(improvement?.missing_preferred_skills)
    ? improvement.missing_preferred_skills
    : []

  const sectionImprovements = Array.isArray(improvement?.section_improvements)
    ? improvement.section_improvements
    : []

  const summaryImprovements = Array.isArray(improvement?.summary_improvements)
    ? improvement.summary_improvements
    : []

  const experienceImprovements = Array.isArray(
    improvement?.experience_improvements,
  )
    ? improvement.experience_improvements
    : []

  const projectImprovements = Array.isArray(improvement?.project_improvements)
    ? improvement.project_improvements
    : []

  const skillsImprovements = Array.isArray(improvement?.skills_improvements)
    ? improvement.skills_improvements
    : []

  const requiredSkillRecs = Array.isArray(
    improvement?.required_skill_recommendations,
  )
    ? improvement.required_skill_recommendations
    : []

  const preferredSkillRecs = Array.isArray(
    improvement?.preferred_skill_recommendations,
  )
    ? improvement.preferred_skill_recommendations
    : []

  // Loading state for Job Details
  if (jobLoading) {
    return (
      <section className="ri-page">
        <div className="ri-container">
          <div className="ri-loading-state">
            <div className="ri-loading-mark">⚡</div>
            <span className="ri-overline">AI RESUME IMPROVEMENT</span>
            <h1>Loading opportunity details...</h1>
            <p>Retrieving target role requirements and job context.</p>
          </div>
        </div>
      </section>
    )
  }

  // Error state for Job Details
  if (jobError || !job) {
    return (
      <section className="ri-page">
        <div className="ri-container">
          <div className="ri-error-state">
            <div className="ri-error-icon">!</div>
            <span className="ri-overline">OPPORTUNITY UNAVAILABLE</span>
            <h1>Unable to open resume improvement.</h1>
            <p>{jobError || 'The selected opportunity is unavailable.'}</p>
            <Link to="/candidate/jobs" className="primary-button">
              Browse opportunities
            </Link>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="ri-page">
      <div className="ri-container">
        {/* Top Navigation */}
        <div className="ri-nav-bar">
          <Link to={`/candidate/jobs/${jobId}`} className="ri-back-link">
            <span aria-hidden="true">←</span>
            Back to opportunity
          </Link>

          <Link
            to={`/candidate/ats-analysis?job_id=${jobId}`}
            className="ri-secondary-nav-link"
          >
            <span>◎</span>
            View ATS Analyzer
          </Link>
        </div>

        {/* Hero Section */}
        <header className="ri-hero">
          <div className="ri-hero-mark">⚡</div>
          <div className="ri-hero-content">
            <span className="ri-overline">AI RESUME IMPROVEMENT ASSISTANT</span>
            <h1>Actionable recommendations to land the interview.</h1>
            <p>
              Hirely compares your active resume against this role to provide
              grounded, section-by-section improvements, keyword alignment, and
              prioritized actions without inventing qualifications.
            </p>
          </div>
        </header>

        {/* Main 2-Column Layout */}
        <div className="ri-layout">
          {/* Sidebar: Target Job Summary */}
          <aside className="ri-job-card">
            <span className="ri-card-label">TARGET OPPORTUNITY</span>
            <h2>{job.title}</h2>

            <div className="ri-job-details">
              <div>
                <span>LOCATION</span>
                <strong>{job.location || 'Not specified'}</strong>
              </div>
              <div>
                <span>EMPLOYMENT</span>
                <strong>{job.employment_type || 'Not specified'}</strong>
              </div>
              <div>
                <span>EXPERIENCE</span>
                <strong>{job.experience_level || 'Not specified'}</strong>
              </div>
            </div>

            <div className="ri-job-description">
              <span className="ri-card-label">ROLE OVERVIEW</span>
              <p>{job.description}</p>
            </div>

            <div className="ri-grounding-note">
              <span className="ri-note-icon">🛡️</span>
              <div>
                <strong>Strict Grounding & Verification</strong>
                <p>
                  Recommendations never fabricate employers, dates, or metrics.
                  Actions requiring factual confirmation are flagged for your
                  personal review.
                </p>
              </div>
            </div>

            <div className="ri-sidebar-ats-link">
              <span className="ri-card-label">ATS DIAGNOSTICS</span>
              <p>Want a detailed diagnostic breakdown of your current match?</p>
              <Link
                to={`/candidate/ats-analysis?job_id=${jobId}`}
                className="ri-ats-cta-link"
              >
                Open ATS Analysis →
              </Link>
            </div>
          </aside>

          {/* Main Workspace */}
          <main className="ri-workspace">
            {!improvement ? (
              /* Empty / Initial State */
              <div className="ri-empty-state">
                <div className="ri-empty-icon">⚡</div>
                <span className="ri-overline">READY TO OPTIMIZE</span>
                <h2>Generate Tailored Resume Improvements</h2>
                <p>
                  Hirely will calculate your deterministic ATS alignment and
                  generate concrete, section-by-section suggestions to highlight
                  your relevant experience for this specific role.
                </p>

                <button
                  type="button"
                  className="primary-button ri-generate-button"
                  onClick={handleGenerateImprovements}
                  disabled={generating}
                >
                  {generating ? (
                    <>
                      <span className="ri-spinner" aria-hidden="true" />
                      Analyzing resume & generating improvements...
                    </>
                  ) : (
                    <>
                      Generate Resume Improvements
                      <span aria-hidden="true">✦</span>
                    </>
                  )}
                </button>

                {improvementError && (
                  <div className="ri-action-error">
                    <span aria-hidden="true">!</span>
                    <div>
                      <strong>Generation Issue:</strong> {improvementError}
                      {improvementError.includes('resume') && (
                        <div className="ri-error-sublink">
                          <Link to="/candidate/resumes">
                            Upload or activate your resume →
                          </Link>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              /* Results State */
              <div className="ri-results">
                {/* Results Header */}
                <div className="ri-results-header">
                  <div>
                    <span className="ri-overline">IMPROVEMENT PLAN READY</span>
                    <h2>Tailored Optimization Plan</h2>
                  </div>

                  <div className="ri-header-actions">
                    <button
                      type="button"
                      className="ri-secondary-button"
                      onClick={handleGenerateImprovements}
                      disabled={generating}
                    >
                      <span aria-hidden="true">↻</span>
                      {generating ? 'Regenerating...' : 'Regenerate'}
                    </button>
                  </div>
                </div>

                {improvementError && (
                  <div className="ri-action-error">
                    <span aria-hidden="true">!</span>
                    <div>{improvementError}</div>
                  </div>
                )}

                {/* ATS Deterministic Alignment Card */}
                <section className="ri-ats-score-card">
                  <div className="ri-score-main">
                    <div className="ri-score-visual">
                      <div className="ri-score-circle">
                        <strong>{atsScore ?? 0}</strong>
                        <span>/ 100</span>
                      </div>
                      <div className="ri-score-badge">
                        {atsScore !== null
                          ? getScoreLabel(atsScore)
                          : 'Evaluated'}
                      </div>
                    </div>

                    <div className="ri-score-info">
                      <span className="ri-overline">
                        DETERMINISTIC ATS ALIGNMENT
                      </span>
                      <h3>Hirely Deterministic Fit Score</h3>
                      <p>
                        Calculated deterministically using Hirely&apos;s 4-component
                        engine: 45% required skills, 15% preferred skills, 30%
                        semantic relevance, and 10% completeness.
                      </p>
                      <div className="ri-disclaimer-pill">
                        Deterministic calculation • Not an official third-party
                        ATS score
                      </div>
                    </div>
                  </div>

                  {/* 4 Deterministic Signal Bars */}
                  <div className="ri-breakdown-grid">
                    <div className="ri-breakdown-item">
                      <div className="ri-breakdown-header">
                        <span>Required Skills (45%)</span>
                        <strong>{requiredScore}%</strong>
                      </div>
                      <div className="ri-progress-bar">
                        <div
                          className="ri-progress-fill ri-progress-required"
                          style={{ width: `${requiredScore}%` }}
                        />
                      </div>
                    </div>

                    <div className="ri-breakdown-item">
                      <div className="ri-breakdown-header">
                        <span>Preferred Skills (15%)</span>
                        <strong>{preferredScore}%</strong>
                      </div>
                      <div className="ri-progress-bar">
                        <div
                          className="ri-progress-fill ri-progress-preferred"
                          style={{ width: `${preferredScore}%` }}
                        />
                      </div>
                    </div>

                    <div className="ri-breakdown-item">
                      <div className="ri-breakdown-header">
                        <span>Semantic Relevance (30%)</span>
                        <strong>{semanticScore}%</strong>
                      </div>
                      <div className="ri-progress-bar">
                        <div
                          className="ri-progress-fill ri-progress-semantic"
                          style={{ width: `${semanticScore}%` }}
                        />
                      </div>
                    </div>

                    <div className="ri-breakdown-item">
                      <div className="ri-breakdown-header">
                        <span>Completeness (10%)</span>
                        <strong>{completenessScore}%</strong>
                      </div>
                      <div className="ri-progress-bar">
                        <div
                          className="ri-progress-fill ri-progress-completeness"
                          style={{ width: `${completenessScore}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Missing Skills Warning */}
                  {(missingRequired.length > 0 ||
                    missingPreferred.length > 0) && (
                    <div className="ri-missing-skills-section">
                      {missingRequired.length > 0 && (
                        <div className="ri-missing-group">
                          <span className="ri-missing-label">
                            Missing Required Skills to Address:
                          </span>
                          <div className="ri-skill-pills">
                            {missingRequired.map((skill) => (
                              <span
                                key={`req-${skill}`}
                                className="ri-skill-pill ri-skill-missing-required"
                              >
                                ! {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {missingPreferred.length > 0 && (
                        <div className="ri-missing-group">
                          <span className="ri-missing-label">
                            Missing Preferred Skills:
                          </span>
                          <div className="ri-skill-pills">
                            {missingPreferred.map((skill) => (
                              <span
                                key={`pref-${skill}`}
                                className="ri-skill-pill ri-skill-missing-preferred"
                              >
                                • {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </section>

                {/* Overall Assessment Strategy Card */}
                {improvement.overall_assessment && (
                  <section className="ri-strategy-card">
                    <span className="ri-overline">EXECUTIVE STRATEGY</span>
                    <h3>High-Level Optimization Focus</h3>
                    <p>{improvement.overall_assessment}</p>
                  </section>
                )}

                {/* Tab Navigation for Deep Dive */}
                <div className="ri-tabs">
                  <button
                    type="button"
                    className={`ri-tab ${activeTab === 'actions' ? 'ri-tab-active' : ''}`}
                    onClick={() => setActiveTab('actions')}
                  >
                    Prioritized Actions (
                    {Array.isArray(improvement.prioritized_actions)
                      ? improvement.prioritized_actions.length
                      : 0}
                    )
                  </button>

                  <button
                    type="button"
                    className={`ri-tab ${activeTab === 'sections' ? 'ri-tab-active' : ''}`}
                    onClick={() => setActiveTab('sections')}
                  >
                    Section Guidance ({sectionImprovements.length})
                  </button>

                  <button
                    type="button"
                    className={`ri-tab ${activeTab === 'details' ? 'ri-tab-active' : ''}`}
                    onClick={() => setActiveTab('details')}
                  >
                    Deep-Dive Suggestions
                  </button>
                </div>

                {/* TAB 1: Prioritized Improvement Actions */}
                {activeTab === 'actions' && (
                  <section className="ri-tab-content">
                    {/* Priority Filter Controls */}
                    <div className="ri-filter-bar">
                      <span className="ri-filter-label">Filter priority:</span>
                      <div className="ri-filter-buttons">
                        {['all', 'high', 'medium', 'low'].map((level) => (
                          <button
                            key={level}
                            type="button"
                            className={`ri-filter-btn ${priorityFilter === level ? 'ri-filter-btn-active' : ''}`}
                            onClick={() => setPriorityFilter(level)}
                          >
                            {level.charAt(0).toUpperCase() + level.slice(1)}
                          </button>
                        ))}
                      </div>
                    </div>

                    {filteredActions.length === 0 ? (
                      <div className="ri-empty-filter">
                        <p>No actions found for the selected priority filter.</p>
                      </div>
                    ) : (
                      <div className="ri-actions-list">
                        {filteredActions.map((action, index) => {
                          const priorityClass = getPriorityClass(
                            action.priority,
                          )
                          const isCopied = copiedActionIndex === index

                          return (
                            <article
                              key={`action-${index}`}
                              className={`ri-action-card ${action.requires_candidate_verification ? 'ri-action-card-verify' : ''}`}
                            >
                              <div className="ri-action-header">
                                <div className="ri-action-meta">
                                  <span
                                    className={`ri-priority-badge ${priorityClass}`}
                                  >
                                    {action.priority?.toUpperCase()} PRIORITY
                                  </span>

                                  {action.category && (
                                    <span className="ri-category-badge">
                                      {action.category}
                                    </span>
                                  )}
                                </div>

                                <button
                                  type="button"
                                  className="ri-copy-btn"
                                  onClick={() =>
                                    handleCopyText(
                                      action.recommendation,
                                      index,
                                    )
                                  }
                                  title="Copy recommendation"
                                >
                                  {isCopied ? 'Copied! ✓' : 'Copy'}
                                </button>
                              </div>

                              <h3 className="ri-action-title">
                                {action.title}
                              </h3>

                              <div className="ri-action-body">
                                <div>
                                  <span className="ri-action-sublabel">
                                    RECOMMENDATION
                                  </span>
                                  <p className="ri-recommendation-text">
                                    {action.recommendation}
                                  </p>
                                </div>

                                {action.rationale && (
                                  <div className="ri-action-rationale">
                                    <span className="ri-action-sublabel">
                                      WHY THIS MATTERS
                                    </span>
                                    <p>{action.rationale}</p>
                                  </div>
                                )}
                              </div>

                              {/* Candidate Verification Flag */}
                              {action.requires_candidate_verification && (
                                <div className="ri-verification-box">
                                  <span
                                    className="ri-verification-icon"
                                    aria-hidden="true"
                                  >
                                    ⚠️
                                  </span>
                                  <div>
                                    <strong>
                                      Candidate Verification Required
                                    </strong>
                                    <p>
                                      Only incorporate this recommendation if
                                      you have genuine, verifiable hands-on
                                      experience. Never claim skills or metrics
                                      you did not personally deliver.
                                    </p>
                                  </div>
                                </div>
                              )}
                            </article>
                          )
                        })}
                      </div>
                    )}
                  </section>
                )}

                {/* TAB 2: Section-Level Guidance */}
                {activeTab === 'sections' && (
                  <section className="ri-tab-content">
                    <div className="ri-sections-grid">
                      {sectionImprovements.map((sec, idx) => {
                        const statusBadge = getStatusBadge(sec.current_status)

                        return (
                          <div
                            key={`section-${idx}`}
                            className="ri-section-card"
                          >
                            <div className="ri-section-header">
                              <div className="ri-section-title-wrap">
                                <h3>{sec.section_name}</h3>
                                <span
                                  className={`ri-status-badge ${statusBadge.className}`}
                                >
                                  <span aria-hidden="true">
                                    {statusBadge.icon}
                                  </span>
                                  {statusBadge.label}
                                </span>
                              </div>
                            </div>

                            {Array.isArray(sec.suggestions) &&
                            sec.suggestions.length > 0 ? (
                              <ul className="ri-suggestions-list">
                                {sec.suggestions.map((sug, sIdx) => (
                                  <li key={`sug-${idx}-${sIdx}`}>
                                    <span
                                      className="ri-sug-bullet"
                                      aria-hidden="true"
                                    >
                                      →
                                    </span>
                                    <span>{sug}</span>
                                  </li>
                                ))}
                              </ul>
                            ) : (
                              <p className="ri-empty-suggestions">
                                This section aligns well with no major adjustments
                                needed.
                              </p>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  </section>
                )}

                {/* TAB 3: Targeted Deep-Dive Suggestions */}
                {activeTab === 'details' && (
                  <section className="ri-tab-content">
                    <div className="ri-deepdive-grid">
                      {/* Summary Improvements */}
                      {summaryImprovements.length > 0 && (
                        <div className="ri-deepdive-card">
                          <div className="ri-deepdive-heading">
                            <span className="ri-deepdive-icon">📝</span>
                            <div>
                              <span className="ri-overline">SUMMARY</span>
                              <h3>Professional Headline & Summary</h3>
                            </div>
                          </div>
                          <ul className="ri-suggestions-list">
                            {summaryImprovements.map((item, i) => (
                              <li key={`sum-${i}`}>
                                <span className="ri-sug-bullet">→</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Experience Improvements */}
                      {experienceImprovements.length > 0 && (
                        <div className="ri-deepdive-card">
                          <div className="ri-deepdive-heading">
                            <span className="ri-deepdive-icon">💼</span>
                            <div>
                              <span className="ri-overline">EXPERIENCE</span>
                              <h3>Work Experience & Impact Bullets</h3>
                            </div>
                          </div>
                          <ul className="ri-suggestions-list">
                            {experienceImprovements.map((item, i) => (
                              <li key={`exp-${i}`}>
                                <span className="ri-sug-bullet">→</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Project Improvements */}
                      {projectImprovements.length > 0 && (
                        <div className="ri-deepdive-card">
                          <div className="ri-deepdive-heading">
                            <span className="ri-deepdive-icon">🚀</span>
                            <div>
                              <span className="ri-overline">PROJECTS</span>
                              <h3>Project Architecture & Evidence</h3>
                            </div>
                          </div>
                          <ul className="ri-suggestions-list">
                            {projectImprovements.map((item, i) => (
                              <li key={`proj-${i}`}>
                                <span className="ri-sug-bullet">→</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Skills Alignment */}
                      {skillsImprovements.length > 0 && (
                        <div className="ri-deepdive-card">
                          <div className="ri-deepdive-heading">
                            <span className="ri-deepdive-icon">⚙️</span>
                            <div>
                              <span className="ri-overline">SKILLS</span>
                              <h3>Skills Organization & Terminology</h3>
                            </div>
                          </div>
                          <ul className="ri-suggestions-list">
                            {skillsImprovements.map((item, i) => (
                              <li key={`sk-${i}`}>
                                <span className="ri-sug-bullet">→</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Required Skill Recommendations */}
                      {requiredSkillRecs.length > 0 && (
                        <div className="ri-deepdive-card ri-deepdive-required">
                          <div className="ri-deepdive-heading">
                            <span className="ri-deepdive-icon">🎯</span>
                            <div>
                              <span className="ri-overline">
                                REQUIRED SKILLS
                              </span>
                              <h3>Closing Required Skill Gaps</h3>
                            </div>
                          </div>
                          <ul className="ri-suggestions-list">
                            {requiredSkillRecs.map((item, i) => (
                              <li key={`req-rec-${i}`}>
                                <span className="ri-sug-bullet">!</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Preferred Skill Recommendations */}
                      {preferredSkillRecs.length > 0 && (
                        <div className="ri-deepdive-card">
                          <div className="ri-deepdive-heading">
                            <span className="ri-deepdive-icon">✨</span>
                            <div>
                              <span className="ri-overline">
                                PREFERRED SKILLS
                              </span>
                              <h3>Preferred Qualifications</h3>
                            </div>
                          </div>
                          <ul className="ri-suggestions-list">
                            {preferredSkillRecs.map((item, i) => (
                              <li key={`pref-rec-${i}`}>
                                <span className="ri-sug-bullet">✓</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </section>
                )}

                {/* Footer Notes & Navigation */}
                <div className="ri-bottom-cta">
                  <div className="ri-bottom-cta-text">
                    <strong>Next Steps</strong>
                    <p>
                      Apply these edits to your resume, re-upload to Hirely, and
                      run an updated ATS analysis to verify your score improvement.
                    </p>
                  </div>
                  <div className="ri-bottom-cta-buttons">
                    <Link
                      to={`/candidate/ats-analysis?job_id=${jobId}`}
                      className="ri-secondary-button"
                    >
                      View ATS Analyzer →
                    </Link>
                    <Link
                      to={`/candidate/jobs/${jobId}`}
                      className="primary-button ri-opportunity-btn"
                    >
                      Return to Opportunity
                    </Link>
                  </div>
                </div>

                <div className="ri-footer-note">
                  <span>AI-powered resume optimization assistant</span>
                  <span>
                    Recommendations are suggestions for your review. Always
                    ensure your resume represents truthful, verifiable work.
                  </span>
                </div>
              </div>
            )}
          </main>
        </div>
      </div>
    </section>
  )
}

export default ResumeImprovement
