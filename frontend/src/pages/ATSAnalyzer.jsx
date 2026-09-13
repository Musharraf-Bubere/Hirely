import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

import { getJob } from '../services/jobs'
import { analyzeResumeATS } from '../services/atsAnalyzer'

import './ATSAnalyzer.css'

function formatPercentage(value) {
  if (
    typeof value !== 'number' ||
    !Number.isFinite(value)
  ) {
    return 0
  }

  return Math.round(
    Math.max(0, Math.min(1, value)) * 100,
  )
}

function getScoreLabel(score) {
  if (score >= 85) {
    return 'Excellent match'
  }

  if (score >= 70) {
    return 'Strong match'
  }

  if (score >= 55) {
    return 'Moderate match'
  }

  return 'Needs improvement'
}

function SkillPill({ skill, type = 'matched' }) {
  return (
    <span
      className={`ats-skill-pill ats-skill-pill-${type}`}
    >
      {type === 'matched' && (
        <span aria-hidden="true">✓</span>
      )}

      {type === 'missing' && (
        <span aria-hidden="true">!</span>
      )}

      {type === 'preferred' && (
        <span aria-hidden="true">✓</span>
      )}

      {skill}
    </span>
  )
}

function InsightList({
  items,
  emptyMessage,
  type,
}) {
  if (!Array.isArray(items) || items.length === 0) {
    return (
      <p className="ats-empty-insight">
        {emptyMessage}
      </p>
    )
  }

  return (
    <ul className={`ats-insight-list ats-insight-list-${type}`}>
      {items.map((item, index) => (
        <li key={`${type}-${index}`}>
          <span
            className="ats-insight-marker"
            aria-hidden="true"
          >
            {type === 'strengths'
              ? '✓'
              : type === 'improvement'
                ? '!'
                : '→'}
          </span>

          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}

function ATSAnalyzer() {
  const [searchParams] = useSearchParams()

  const jobId = searchParams.get('job_id')

  const [job, setJob] = useState(null)
  const [jobLoading, setJobLoading] = useState(true)
  const [jobError, setJobError] = useState('')

  const [analysis, setAnalysis] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisError, setAnalysisError] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadJob() {
      if (!jobId) {
        setJobLoading(false)
        setJobError(
          'No job was selected for ATS analysis.',
        )
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
            err.message ||
              'Unable to load the selected opportunity.',
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

  async function handleAnalyze() {
    if (!jobId) {
      setAnalysisError(
        'No job was selected for ATS analysis.',
      )
      return
    }

    try {
      setAnalyzing(true)
      setAnalysisError('')

      const result = await analyzeResumeATS(jobId)

      if (
        !result ||
        !result.ats_analysis ||
        typeof result.ats_analysis.ats_score !==
          'number'
      ) {
        setAnalysisError(
          'The ATS service returned an invalid analysis.',
        )
        return
      }

      setAnalysis(result.ats_analysis)
    } catch (err) {
      setAnalysisError(
        err.message ||
          'Unable to analyze your resume for this opportunity.',
      )
    } finally {
      setAnalyzing(false)
    }
  }

  if (jobLoading) {
    return (
      <section className="ats-page">
        <div className="ats-container">
          <div className="ats-loading">
            <div className="ats-loading-mark">
              ◎
            </div>

            <span className="ats-overline">
              AI RESUME ATS ANALYZER
            </span>

            <h1>
              Preparing your resume analysis...
            </h1>

            <p>
              Loading the opportunity details.
            </p>
          </div>
        </div>
      </section>
    )
  }

  if (jobError || !job) {
    return (
      <section className="ats-page">
        <div className="ats-container">
          <div className="ats-error-state">
            <div className="ats-error-icon">
              !
            </div>

            <span className="ats-overline">
              ATS ANALYZER
            </span>

            <h1>
              We couldn't open this opportunity.
            </h1>

            <p>
              {jobError ||
                'The selected opportunity is unavailable.'}
            </p>

            <Link
              to="/candidate/jobs"
              className="primary-button"
            >
              Browse opportunities
            </Link>
          </div>
        </div>
      </section>
    )
  }

  const atsScore = analysis?.ats_score ?? null

  const scoreBreakdown = analysis?.score_breakdown

  const requiredScore = formatPercentage(
    scoreBreakdown?.required_skill_score,
  )

  const preferredScore = formatPercentage(
    scoreBreakdown?.preferred_skill_score,
  )

  const semanticScore = formatPercentage(
    scoreBreakdown?.semantic_relevance_score,
  )

  const completenessScore = formatPercentage(
    scoreBreakdown?.resume_completeness_score,
  )

  const requiredMatched =
    Array.isArray(
      analysis?.required_skills_matched,
    )
      ? analysis.required_skills_matched
      : []

  const requiredMissing =
    Array.isArray(
      analysis?.required_skills_missing,
    )
      ? analysis.required_skills_missing
      : []

  const preferredMatched =
    Array.isArray(
      analysis?.preferred_skills_matched,
    )
      ? analysis.preferred_skills_matched
      : []

  const preferredMissing =
    Array.isArray(
      analysis?.preferred_skills_missing,
    )
      ? analysis.preferred_skills_missing
      : []

  return (
    <section className="ats-page">
      <div className="ats-container">
        <Link
          to={`/candidate/jobs/${jobId}`}
          className="ats-back"
        >
          <span aria-hidden="true">
            ←
          </span>

          Back to opportunity
        </Link>

        <header className="ats-hero">
          <div className="ats-hero-mark">
            ◎
          </div>

          <div>
            <span className="ats-overline">
              AI RESUME ATS ANALYZER
            </span>

            <h1>
              See how well your resume fits the role.
            </h1>

            <p>
              Hirely analyzes your current resume against
              this opportunity to identify your strongest
              signals, missing skills, and areas worth
              improving before you apply.
            </p>
          </div>
        </header>

        <div className="ats-layout">
          <aside className="ats-job-card">
            <span className="ats-card-label">
              TARGET OPPORTUNITY
            </span>

            <h2>{job.title}</h2>

            <div className="ats-job-details">
              <div>
                <span>LOCATION</span>

                <strong>
                  {job.location ||
                    'Not specified'}
                </strong>
              </div>

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
            </div>

            <div className="ats-job-description">
              <span className="ats-card-label">
                ROLE OVERVIEW
              </span>

              <p>
                {job.description}
              </p>
            </div>

            <div className="ats-method-note">
              <span aria-hidden="true">
                ✓
              </span>

              <p>
                Your score combines deterministic resume
                signals, semantic relevance, and AI-powered
                qualitative analysis.
              </p>
            </div>
          </aside>

          <main className="ats-workspace">
            {!analysis ? (
              <div className="ats-empty">
                <div className="ats-empty-icon">
                  ◎
                </div>

                <span className="ats-overline">
                  READY WHEN YOU ARE
                </span>

                <h2>
                  Analyze your current resume.
                </h2>

                <p>
                  Hirely will compare your active resume
                  with this opportunity and show you where
                  you already align and where you can
                  improve.
                </p>

                <button
                  type="button"
                  className="primary-button ats-analyze-button"
                  onClick={handleAnalyze}
                  disabled={analyzing}
                >
                  {analyzing
                    ? 'Analyzing your resume...'
                    : 'Analyze My Resume'}

                  {!analyzing && (
                    <span aria-hidden="true">
                      ✦
                    </span>
                  )}
                </button>

                {analysisError && (
                  <div className="ats-action-error">
                    <span>!</span>

                    {analysisError}
                  </div>
                )}
              </div>
            ) : (
              <div className="ats-results">
                <div className="ats-score-header">
                  <div>
                    <span className="ats-overline">
                      ATS ANALYSIS COMPLETE
                    </span>

                    <h2>
                      Your resume fit for this role.
                    </h2>
                  </div>

                  <button
                    type="button"
                    className="ats-secondary-button"
                    onClick={handleAnalyze}
                    disabled={analyzing}
                  >
                    <span aria-hidden="true">
                      ↻
                    </span>

                    {analyzing
                      ? 'Reanalyzing...'
                      : 'Reanalyze'}
                  </button>
                </div>

                {analysisError && (
                  <div className="ats-action-error">
                    <span>!</span>

                    {analysisError}
                  </div>
                )}

                <section className="ats-score-card">
                  <div className="ats-score-main">
                    <div className="ats-score-circle">
                      <strong>
                        {atsScore}
                      </strong>

                      <span>/ 100</span>
                    </div>

                    <div className="ats-score-copy">
                      <span className="ats-score-label">
                        ATS SCORE
                      </span>

                      <h3>
                        {getScoreLabel(atsScore)}
                      </h3>

                      <p>
                        This score reflects how strongly
                        your current resume represents your
                        fit for the selected opportunity.
                      </p>
                    </div>
                  </div>

                  <div className="ats-score-progress">
                    <div
                      className="ats-score-progress-fill"
                      style={{
                        width: `${Math.max(
                          0,
                          Math.min(100, atsScore),
                        )}%`,
                      }}
                    />
                  </div>
                </section>

                <section className="ats-breakdown-section">
                  <div className="ats-section-heading">
                    <div>
                      <span className="ats-overline">
                        SCORE BREAKDOWN
                      </span>

                      <h3>
                        What is driving your score?
                      </h3>
                    </div>
                  </div>

                  <div className="ats-breakdown-grid">
                    <div className="ats-breakdown-card">
                      <div className="ats-breakdown-top">
                        <span>
                          Required skills
                        </span>

                        <strong>
                          {requiredScore}%
                        </strong>
                      </div>

                      <div className="ats-breakdown-bar">
                        <div
                          style={{
                            width: `${requiredScore}%`,
                          }}
                        />
                      </div>

                      <small>
                        Weight: 45%
                      </small>
                    </div>

                    <div className="ats-breakdown-card">
                      <div className="ats-breakdown-top">
                        <span>
                          Preferred skills
                        </span>

                        <strong>
                          {preferredScore}%
                        </strong>
                      </div>

                      <div className="ats-breakdown-bar">
                        <div
                          style={{
                            width: `${preferredScore}%`,
                          }}
                        />
                      </div>

                      <small>
                        Weight: 15%
                      </small>
                    </div>

                    <div className="ats-breakdown-card">
                      <div className="ats-breakdown-top">
                        <span>
                          Semantic relevance
                        </span>

                        <strong>
                          {semanticScore}%
                        </strong>
                      </div>

                      <div className="ats-breakdown-bar">
                        <div
                          style={{
                            width: `${semanticScore}%`,
                          }}
                        />
                      </div>

                      <small>
                        Weight: 30%
                      </small>
                    </div>

                    <div className="ats-breakdown-card">
                      <div className="ats-breakdown-top">
                        <span>
                          Resume completeness
                        </span>

                        <strong>
                          {completenessScore}%
                        </strong>
                      </div>

                      <div className="ats-breakdown-bar">
                        <div
                          style={{
                            width: `${completenessScore}%`,
                          }}
                        />
                      </div>

                      <small>
                        Weight: 10%
                      </small>
                    </div>
                  </div>
                </section>

                <section className="ats-skills-section">
                  <div className="ats-section-heading">
                    <div>
                      <span className="ats-overline">
                        SKILL ALIGNMENT
                      </span>

                      <h3>
                        Where your resume matches the role.
                      </h3>
                    </div>
                  </div>

                  <div className="ats-skill-columns">
                    <div className="ats-skill-panel">
                      <div className="ats-panel-heading">
                        <span>
                          REQUIRED SKILLS
                        </span>

                        <strong>
                          {requiredMatched.length} matched
                        </strong>
                      </div>

                      <div className="ats-skill-list">
                        {requiredMatched.length > 0 ? (
                          requiredMatched.map(
                            (skill) => (
                              <SkillPill
                                key={`required-matched-${skill}`}
                                skill={skill}
                                type="matched"
                              />
                            ),
                          )
                        ) : (
                          <p className="ats-empty-insight">
                            No required skills were matched.
                          </p>
                        )}
                      </div>

                      {requiredMissing.length > 0 && (
                        <>
                          <div className="ats-panel-heading ats-panel-heading-spaced">
                            <span>
                              MISSING REQUIRED
                            </span>

                            <strong>
                              {requiredMissing.length}
                            </strong>
                          </div>

                          <div className="ats-skill-list">
                            {requiredMissing.map(
                              (skill) => (
                                <SkillPill
                                  key={`required-missing-${skill}`}
                                  skill={skill}
                                  type="missing"
                                />
                              ),
                            )}
                          </div>
                        </>
                      )}
                    </div>

                    <div className="ats-skill-panel">
                      <div className="ats-panel-heading">
                        <span>
                          PREFERRED SKILLS
                        </span>

                        <strong>
                          {preferredMatched.length} matched
                        </strong>
                      </div>

                      <div className="ats-skill-list">
                        {preferredMatched.length > 0 ? (
                          preferredMatched.map(
                            (skill) => (
                              <SkillPill
                                key={`preferred-matched-${skill}`}
                                skill={skill}
                                type="preferred"
                              />
                            ),
                          )
                        ) : (
                          <p className="ats-empty-insight">
                            No preferred skills were matched.
                          </p>
                        )}
                      </div>

                      {preferredMissing.length > 0 && (
                        <>
                          <div className="ats-panel-heading ats-panel-heading-spaced">
                            <span>
                              PREFERRED TO DEVELOP
                            </span>

                            <strong>
                              {preferredMissing.length}
                            </strong>
                          </div>

                          <div className="ats-skill-list">
                            {preferredMissing.map(
                              (skill) => (
                                <SkillPill
                                  key={`preferred-missing-${skill}`}
                                  skill={skill}
                                  type="missing"
                                />
                              ),
                            )}
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                </section>

                <section className="ats-insights-section">
                  <div className="ats-insight-card">
                    <div className="ats-insight-card-heading">
                      <span className="ats-insight-icon ats-insight-icon-strength">
                        ✓
                      </span>

                      <div>
                        <span className="ats-overline">
                          STRENGTHS
                        </span>

                        <h3>
                          What your resume does well.
                        </h3>
                      </div>
                    </div>

                    <InsightList
                      items={analysis.strengths}
                      emptyMessage="No specific strengths were identified."
                      type="strengths"
                    />
                  </div>

                  <div className="ats-insight-card">
                    <div className="ats-insight-card-heading">
                      <span className="ats-insight-icon ats-insight-icon-improvement">
                        !
                      </span>

                      <div>
                        <span className="ats-overline">
                          IMPROVEMENT AREAS
                        </span>

                        <h3>
                          What could strengthen your resume.
                        </h3>
                      </div>
                    </div>

                    <InsightList
                      items={analysis.improvement_areas}
                      emptyMessage="No major improvement areas were identified."
                      type="improvement"
                    />
                  </div>

                  <div className="ats-insight-card">
                    <div className="ats-insight-card-heading">
                      <span className="ats-insight-icon ats-insight-icon-suggestion">
                        →
                      </span>

                      <div>
                        <span className="ats-overline">
                          SUGGESTIONS
                        </span>

                        <h3>
                          Practical next steps.
                        </h3>
                      </div>
                    </div>

                    <InsightList
                      items={analysis.suggestions}
                      emptyMessage="No additional suggestions were provided."
                      type="suggestions"
                    />
                  </div>
                </section>

                <section className="ats-summary-card">
                  <span className="ats-overline">
                    AI SUMMARY
                  </span>

                  <h3>
                    What Hirely found overall.
                  </h3>

                  <p>
                    {analysis.summary}
                  </p>
                </section>

                <div className="ats-footer-note">
                  <span>
                    AI-assisted resume analysis
                  </span>

                  <span>
                    Review suggestions and make changes
                    that accurately reflect your experience.
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

export default ATSAnalyzer