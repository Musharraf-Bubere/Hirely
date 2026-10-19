import { useEffect, useState, useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'

import { getRecruiterJobs } from '../services/recruiter'
import { analyzeJobDescription } from '../services/jobDescriptionAnalyzer'

import './JobDescriptionAnalyzer.css'

function getScoreLabel(score) {
  if (score >= 85) return 'Exceptional Quality'
  if (score >= 70) return 'Solid Description'
  if (score >= 50) return 'Needs Polish'
  return 'Requires Significant Revision'
}

function getScoreColorClass(score) {
  if (score >= 85) return 'score-excellent'
  if (score >= 70) return 'score-good'
  if (score >= 50) return 'score-warning'
  return 'score-poor'
}

function getPriorityBadgeClass(priority) {
  switch (priority?.toLowerCase()) {
    case 'high':
      return 'priority-badge-high'
    case 'medium':
      return 'priority-badge-medium'
    case 'low':
      return 'priority-badge-low'
    default:
      return 'priority-badge-neutral'
  }
}

function getCategoryBadgeClass(category) {
  switch (category?.toLowerCase()) {
    case 'clarity':
      return 'category-badge-clarity'
    case 'completeness':
      return 'category-badge-completeness'
    case 'requirements':
      return 'category-badge-requirements'
    case 'skills':
      return 'category-badge-skills'
    case 'tone':
      return 'category-badge-tone'
    case 'structure':
      return 'category-badge-structure'
    default:
      return 'category-badge-default'
  }
}

export default function JobDescriptionAnalyzer() {
  const { jobId } = useParams()

  const [job, setJob] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState('')
  const [copiedDraft, setCopiedDraft] = useState(false)
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [activeTab, setActiveTab] = useState('overview')

  // Load Job info and perform initial analysis
  useEffect(() => {
    let isMounted = true

    async function initialize() {
      setLoading(true)
      setError('')

      try {
        const jobs = await getRecruiterJobs()
        const found = (Array.isArray(jobs) ? jobs : []).find(
          (j) => String(j.id) === String(jobId),
        )

        if (!found) {
          if (isMounted) {
            setError('Job not found or you do not have permission to view this job.')
            setLoading(false)
          }
          return
        }

        if (isMounted) {
          setJob(found)
        }

        if (!found.description || !found.description.trim()) {
          if (isMounted) {
            setError('This job currently has an empty description. Please add a description before analyzing.')
            setLoading(false)
          }
          return
        }

        // Run analysis
        const res = await analyzeJobDescription(jobId)
        if (isMounted) {
          setAnalysis(res.analysis)
        }
      } catch (err) {
        if (isMounted) {
          setError(
            err?.message ||
              'Unable to analyze this job description. Please ensure the backend is available.',
          )
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    initialize()

    return () => {
      isMounted = false
    }
  }, [jobId])

  // Handle re-analyze trigger
  async function handleReanalyze() {
    setAnalyzing(true)
    setError('')
    try {
      const res = await analyzeJobDescription(jobId)
      setAnalysis(res.analysis)
    } catch (err) {
      setError(
        err?.message ||
          'Failed to re-analyze the job description. Please try again.',
      )
    } finally {
      setAnalyzing(false)
    }
  }

  // Handle copy draft
  async function handleCopyDraft() {
    if (!analysis?.improved_description) return
    try {
      await navigator.clipboard.writeText(analysis.improved_description)
      setCopiedDraft(true)
      setTimeout(() => setCopiedDraft(false), 2500)
    } catch {
      // Fallback
      setCopiedDraft(false)
    }
  }

  // Filter issues by priority
  const filteredIssues = useMemo(() => {
    if (!analysis?.issues) return []
    if (priorityFilter === 'all') return analysis.issues
    return analysis.issues.filter(
      (issue) => issue.priority.toLowerCase() === priorityFilter.toLowerCase(),
    )
  }, [analysis, priorityFilter])

  // Issue counts
  const issueCounts = useMemo(() => {
    const counts = { all: 0, high: 0, medium: 0, low: 0 }
    if (!analysis?.issues) return counts
    counts.all = analysis.issues.length
    for (const issue of analysis.issues) {
      const p = issue.priority.toLowerCase()
      if (counts[p] !== undefined) {
        counts[p]++
      }
    }
    return counts
  }, [analysis])

  if (loading) {
    return (
      <main className="jda-page">
        <div className="jda-container">
          <div className="jda-skeleton-hero">
            <div className="jda-skeleton-icon" />
            <div className="jda-skeleton-text-group">
              <div className="jda-skeleton-line short" />
              <div className="jda-skeleton-line title" />
              <div className="jda-skeleton-line medium" />
            </div>
          </div>
          <div className="jda-skeleton-cards">
            <div className="jda-skeleton-card" />
            <div className="jda-skeleton-card" />
          </div>
          <div className="jda-loading-status">
            <div className="jda-spinner" />
            <p>Analyzing job description with Gemini AI...</p>
            <span>Evaluating clarity, completeness, skills alignment, and drafting suggestions</span>
          </div>
        </div>
      </main>
    )
  }

  if (error && !analysis) {
    return (
      <main className="jda-page">
        <div className="jda-container">
          <div className="jda-error-card">
            <div className="jda-error-icon">!</div>
            <h2>Unable to Complete Analysis</h2>
            <p>{error}</p>
            <div className="jda-error-actions">
              <Link to={`/recruiter/jobs/${jobId}`} className="jda-btn jda-btn-secondary">
                ← Back to Job
              </Link>
              <button
                type="button"
                onClick={handleReanalyze}
                disabled={analyzing}
                className="jda-btn jda-btn-primary"
              >
                {analyzing ? 'Analyzing...' : 'Retry Analysis'}
              </button>
            </div>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="jda-page">
      <div className="jda-container">
        {/* Navigation Bar */}
        <nav className="jda-nav-bar">
          <Link to={`/recruiter/jobs/${jobId}`} className="jda-back-link">
            ← Back to Job Detail
          </Link>
          <div className="jda-nav-actions">
            <button
              type="button"
              onClick={handleReanalyze}
              disabled={analyzing}
              className="jda-btn jda-btn-secondary jda-btn-sm"
              title="Run a fresh analysis with Gemini AI"
            >
              {analyzing ? 'Analyzing...' : '↻ Re-analyze'}
            </button>
          </div>
        </nav>

        {/* Header Hero */}
        <header className="jda-hero">
          <div className="jda-hero-icon">✦</div>
          <div className="jda-hero-info">
            <span className="jda-eyebrow">Recruiter AI • Job Intelligence</span>
            <h1 className="jda-title">Job Description Analyzer</h1>
            <p className="jda-subtitle">
              Advisory quality audit and structural refinement for{' '}
              <strong>{job?.title || 'this position'}</strong>
            </p>
          </div>
        </header>

        {/* Advisory Banner */}
        <div className="jda-advisory-banner">
          <span className="jda-advisory-badge">Advisory Only</span>
          <p>
            {analysis?.disclaimer ||
              'This evaluation and improved draft are AI-generated suggestions. Hirely does not automatically modify or republish your job description.'}
          </p>
        </div>

        {/* Error notification if re-analysis failed */}
        {error && analysis && (
          <div className="jda-inline-error">
            <span>Notice:</span> {error}
          </div>
        )}

        {/* Score & Assessment Card */}
        <section className="jda-score-card">
          <div className="jda-score-left">
            <div className={`jda-score-badge ${getScoreColorClass(analysis?.quality_score)}`}>
              <span className="jda-score-number">{analysis?.quality_score ?? 0}</span>
              <span className="jda-score-max">/100</span>
            </div>
            <div className="jda-score-meta">
              <span className="jda-score-label">{getScoreLabel(analysis?.quality_score)}</span>
              <span className="jda-score-note">Heuristic Quality Rating</span>
            </div>
          </div>

          <div className="jda-score-right">
            <h3 className="jda-assessment-heading">Overall Assessment</h3>
            <p className="jda-assessment-text">{analysis?.overall_assessment}</p>
          </div>
        </section>

        {/* Tab Navigation */}
        <div className="jda-tabs">
          <button
            type="button"
            className={`jda-tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview & Strengths
          </button>
          <button
            type="button"
            className={`jda-tab-btn ${activeTab === 'issues' ? 'active' : ''}`}
            onClick={() => setActiveTab('issues')}
          >
            Issues & Gaps ({analysis?.issues?.length || 0})
          </button>
          <button
            type="button"
            className={`jda-tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
            onClick={() => setActiveTab('skills')}
          >
            Skills Alignment
          </button>
          <button
            type="button"
            className={`jda-tab-btn ${activeTab === 'draft' ? 'active' : ''}`}
            onClick={() => setActiveTab('draft')}
          >
            Advisory Draft
          </button>
        </div>

        {/* TAB 1: OVERVIEW & STRENGTHS */}
        {activeTab === 'overview' && (
          <div className="jda-tab-content">
            <div className="jda-grid-two">
              {/* Strengths */}
              <article className="jda-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon positive">✓</span>
                  <h2>Key Strengths</h2>
                </div>
                <div className="jda-card-body">
                  {analysis?.strengths && analysis.strengths.length > 0 ? (
                    <ul className="jda-list jda-strengths-list">
                      {analysis.strengths.map((str, idx) => (
                        <li key={`strength-${idx}`}>{str}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="jda-empty-note">No particular strengths highlighted.</p>
                  )}
                </div>
              </article>

              {/* Actionable Recommendations */}
              <article className="jda-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon action">⚡</span>
                  <h2>Improvement Recommendations</h2>
                </div>
                <div className="jda-card-body">
                  {analysis?.improvement_recommendations &&
                  analysis.improvement_recommendations.length > 0 ? (
                    <ul className="jda-list jda-action-list">
                      {analysis.improvement_recommendations.map((rec, idx) => (
                        <li key={`rec-${idx}`}>{rec}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="jda-empty-note">No specific recommendations provided.</p>
                  )}
                </div>
              </article>
            </div>

            {/* Missing Info Callout */}
            {analysis?.missing_information && analysis.missing_information.length > 0 && (
              <div className="jda-card jda-missing-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon warning">!</span>
                  <h2>Critical Missing Details</h2>
                </div>
                <p className="jda-missing-intro">
                  The following key details are missing from your job description. Adding these will
                  significantly enhance candidate qualification transparency and searchability:
                </p>
                <div className="jda-tags-wrapper">
                  {analysis.missing_information.map((item, idx) => (
                    <span key={`missing-${idx}`} className="jda-missing-tag">
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 2: ISSUES & GAPS */}
        {activeTab === 'issues' && (
          <div className="jda-tab-content">
            <div className="jda-filter-bar">
              <span className="jda-filter-label">Filter by Priority:</span>
              <div className="jda-filter-chips">
                <button
                  type="button"
                  className={`jda-chip ${priorityFilter === 'all' ? 'active' : ''}`}
                  onClick={() => setPriorityFilter('all')}
                >
                  All ({issueCounts.all})
                </button>
                <button
                  type="button"
                  className={`jda-chip high ${priorityFilter === 'high' ? 'active' : ''}`}
                  onClick={() => setPriorityFilter('high')}
                >
                  High ({issueCounts.high})
                </button>
                <button
                  type="button"
                  className={`jda-chip medium ${priorityFilter === 'medium' ? 'active' : ''}`}
                  onClick={() => setPriorityFilter('medium')}
                >
                  Medium ({issueCounts.medium})
                </button>
                <button
                  type="button"
                  className={`jda-chip low ${priorityFilter === 'low' ? 'active' : ''}`}
                  onClick={() => setPriorityFilter('low')}
                >
                  Low ({issueCounts.low})
                </button>
              </div>
            </div>

            {filteredIssues.length > 0 ? (
              <div className="jda-issues-list">
                {filteredIssues.map((issue, idx) => (
                  <article key={`issue-${idx}`} className="jda-issue-card">
                    <div className="jda-issue-header">
                      <div className="jda-issue-badges">
                        <span className={`jda-priority-badge ${getPriorityBadgeClass(issue.priority)}`}>
                          {issue.priority?.toUpperCase()} PRIORITY
                        </span>
                        <span className={`jda-category-badge ${getCategoryBadgeClass(issue.category)}`}>
                          {issue.category}
                        </span>
                      </div>
                      <h3 className="jda-issue-title">{issue.title}</h3>
                    </div>

                    <div className="jda-issue-body">
                      <div className="jda-issue-section">
                        <span className="jda-issue-section-label">Explanation:</span>
                        <p>{issue.explanation}</p>
                      </div>

                      <div className="jda-issue-section suggested-action">
                        <span className="jda-issue-section-label">Recommended Action:</span>
                        <p>{issue.suggested_action}</p>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="jda-empty-card">
                <p>No issues found matching the selected filter.</p>
              </div>
            )}
          </div>
        )}

        {/* TAB 3: SKILLS ALIGNMENT */}
        {activeTab === 'skills' && (
          <div className="jda-tab-content">
            <div className="jda-grid-two">
              {/* Required Skills Evaluation */}
              <article className="jda-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon required">★</span>
                  <h2>Required Skills Evaluation</h2>
                </div>
                <div className="jda-card-body">
                  <p className="jda-narrative">
                    {analysis?.skills_analysis?.required_skills_evaluation ||
                      'No evaluation available for required skills.'}
                  </p>
                </div>
              </article>

              {/* Preferred Skills Evaluation */}
              <article className="jda-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon preferred">☆</span>
                  <h2>Preferred Skills Evaluation</h2>
                </div>
                <div className="jda-card-body">
                  <p className="jda-narrative">
                    {analysis?.skills_analysis?.preferred_skills_evaluation ||
                      'No evaluation available for preferred skills.'}
                  </p>
                </div>
              </article>
            </div>

            <div className="jda-grid-two jda-mt-4">
              {/* Unmentioned Tagged Skills */}
              <article className="jda-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon warning">!</span>
                  <h2>Unmentioned Job Skills</h2>
                </div>
                <div className="jda-card-body">
                  <p className="jda-skills-help">
                    These skills are linked to this job in Hirely, but are not clearly referenced in
                    the job description body:
                  </p>
                  {analysis?.skills_analysis?.unmentioned_skills_in_description &&
                  analysis.skills_analysis.unmentioned_skills_in_description.length > 0 ? (
                    <div className="jda-tags-wrapper">
                      {analysis.skills_analysis.unmentioned_skills_in_description.map((sk, idx) => (
                        <span key={`unmentioned-${idx}`} className="jda-unmentioned-tag">
                          {sk}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="jda-all-mentioned-note">
                      ✓ All tagged skills are referenced in the text description.
                    </p>
                  )}
                </div>
              </article>

              {/* Suggested Skills to Add */}
              <article className="jda-card">
                <div className="jda-card-header">
                  <span className="jda-card-icon action">💡</span>
                  <h2>Suggested Skills to Add</h2>
                </div>
                <div className="jda-card-body">
                  <p className="jda-skills-help">
                    Recommended industry-standard skills that could strengthen candidate matching:
                  </p>
                  {analysis?.skills_analysis?.suggested_skills_to_add &&
                  analysis.skills_analysis.suggested_skills_to_add.length > 0 ? (
                    <div className="jda-tags-wrapper">
                      {analysis.skills_analysis.suggested_skills_to_add.map((sk, idx) => (
                        <span key={`suggested-${idx}`} className="jda-suggested-tag">
                          + {sk}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="jda-empty-note">No additional skills suggested at this time.</p>
                  )}
                </div>
              </article>
            </div>
          </div>
        )}

        {/* TAB 4: ADVISORY DRAFT */}
        {activeTab === 'draft' && (
          <div className="jda-tab-content">
            <article className="jda-card jda-draft-card">
              <div className="jda-draft-header">
                <div>
                  <span className="jda-eyebrow">Advisory Template</span>
                  <h2>Improved Job Description Draft</h2>
                  <p className="jda-draft-subtext">
                    This revised draft clarifies structure and scope without fabricating specific
                    compensation, perks, or proprietary details. Explicit placeholders like{' '}
                    <code>[Insert ...]</code> mark fields requiring your input.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={handleCopyDraft}
                  className="jda-btn jda-btn-primary"
                  title="Copy improved draft to clipboard"
                >
                  {copiedDraft ? 'Copied to Clipboard! ✓' : '📋 Copy Draft'}
                </button>
              </div>

              <div className="jda-draft-content">
                <pre className="jda-draft-pre">{analysis?.improved_description}</pre>
              </div>

              <div className="jda-draft-footer">
                <p>
                  💡 <strong>How to apply:</strong> Copy this draft, navigate to your job
                  management view, replace the bracketed placeholders with your actual details, and
                  save. Hirely does not mutate your job posting automatically.
                </p>
              </div>
            </article>
          </div>
        )}
      </div>
    </main>
  )
}
