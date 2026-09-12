import { useEffect, useState } from 'react'
import {
  Link,
  useSearchParams,
} from 'react-router-dom'

import { getJob } from '../services/jobs'
import { generateCoverLetter } from '../services/coverLetter'

import './CoverLetter.css'

function CoverLetter() {
  const [searchParams] = useSearchParams()

  const jobId = searchParams.get('job_id')

  const [job, setJob] = useState(null)
  const [jobLoading, setJobLoading] = useState(true)
  const [jobError, setJobError] = useState('')

  const [coverLetter, setCoverLetter] = useState('')
  const [generating, setGenerating] = useState(false)
  const [generateError, setGenerateError] = useState('')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    let ignore = false

    async function loadJob() {
      if (!jobId) {
        setJobLoading(false)
        setJobError(
          'No job was selected for the cover letter.',
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

  async function handleGenerate() {
    if (!jobId) {
      setGenerateError(
        'No job was selected for the cover letter.',
      )
      return
    }

    try {
      setGenerating(true)
      setGenerateError('')
      setCopied(false)

      const result = await generateCoverLetter(jobId)

      if (
        !result ||
        typeof result.cover_letter !== 'string' ||
        !result.cover_letter.trim()
      ) {
        setGenerateError(
          'The AI service returned an empty cover letter.',
        )
        return
      }

      setCoverLetter(result.cover_letter)
    } catch (err) {
      setGenerateError(
        err.message ||
          'Unable to generate your cover letter.',
      )
    } finally {
      setGenerating(false)
    }
  }

  async function handleCopy() {
    if (!coverLetter) {
      return
    }

    try {
      await navigator.clipboard.writeText(
        coverLetter,
      )

      setCopied(true)

      window.setTimeout(() => {
        setCopied(false)
      }, 2000)
    } catch {
      setGenerateError(
        'Unable to copy the cover letter. Please copy it manually.',
      )
    }
  }

  function handleRegenerate() {
    handleGenerate()
  }

  if (jobLoading) {
    return (
      <section className="cover-letter-page">
        <div className="cover-letter-container">
          <div className="cover-letter-loading">
            <div className="cover-letter-loading-mark">
              ✦
            </div>

            <span className="cover-letter-overline">
              AI COVER LETTER
            </span>

            <h1>
              Preparing your application workspace...
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
      <section className="cover-letter-page">
        <div className="cover-letter-container">
          <div className="cover-letter-error-state">
            <div className="cover-letter-error-icon">
              !
            </div>

            <span className="cover-letter-overline">
              COVER LETTER
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

  return (
    <section className="cover-letter-page">
      <div className="cover-letter-container">
        <Link
          to={`/candidate/jobs/${jobId}`}
          className="cover-letter-back"
        >
          <span aria-hidden="true">
            ←
          </span>

          Back to opportunity
        </Link>

        <header className="cover-letter-hero">
          <div className="cover-letter-hero-mark">
            ✦
          </div>

          <div>
            <span className="cover-letter-overline">
              AI APPLICATION ASSISTANT
            </span>

            <h1>
              Build a cover letter that fits the role.
            </h1>

            <p>
              Hirely uses your profile and resume
              alongside this opportunity to create a
              tailored, recruiter-friendly cover letter.
            </p>
          </div>
        </header>

        <div className="cover-letter-layout">
          <aside className="cover-letter-job-card">
            <span className="cover-letter-card-label">
              TARGET OPPORTUNITY
            </span>

            <h2>
              {job.title}
            </h2>

            <div className="cover-letter-job-details">
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

            <div className="cover-letter-job-description">
              <span className="cover-letter-card-label">
                ROLE OVERVIEW
              </span>

              <p>
                {job.description}
              </p>
            </div>

            <div className="cover-letter-ai-note">
              <span aria-hidden="true">
                ✓
              </span>

              <p>
                Your letter is generated using
                information already available in your
                Hirely profile and resume.
              </p>
            </div>
          </aside>

          <main className="cover-letter-workspace">
            {!coverLetter ? (
              <div className="cover-letter-empty">
                <div className="cover-letter-empty-icon">
                  ✎
                </div>

                <span className="cover-letter-overline">
                  READY WHEN YOU ARE
                </span>

                <h2>
                  Generate your tailored cover letter.
                </h2>

                <p>
                  Hirely will create a professional
                  cover letter specifically for this
                  opportunity using your available
                  candidate information.
                </p>

                <button
                  type="button"
                  className="primary-button cover-letter-generate-button"
                  onClick={handleGenerate}
                  disabled={generating}
                >
                  {generating
                    ? 'Writing your cover letter...'
                    : 'Generate Cover Letter'}

                  {!generating && (
                    <span aria-hidden="true">
                      ✦
                    </span>
                  )}
                </button>

                {generateError && (
                  <div className="cover-letter-action-error">
                    <span>!</span>

                    {generateError}
                  </div>
                )}
              </div>
            ) : (
              <div className="cover-letter-result">
                <div className="cover-letter-result-header">
                  <div>
                    <span className="cover-letter-overline">
                      GENERATED COVER LETTER
                    </span>

                    <h2>
                      Your application draft
                    </h2>
                  </div>

                  <div className="cover-letter-result-actions">
                    <button
                      type="button"
                      className="cover-letter-secondary-button"
                      onClick={handleCopy}
                    >
                      <span aria-hidden="true">
                        {copied ? '✓' : '⧉'}
                      </span>

                      {copied ? 'Copied' : 'Copy'}
                    </button>

                    <button
                      type="button"
                      className="cover-letter-secondary-button"
                      onClick={handleRegenerate}
                      disabled={generating}
                    >
                      <span aria-hidden="true">
                        ↻
                      </span>

                      {generating
                        ? 'Regenerating...'
                        : 'Regenerate'}
                    </button>
                  </div>
                </div>

                {generateError && (
                  <div className="cover-letter-action-error">
                    <span>!</span>

                    {generateError}
                  </div>
                )}

                <article className="cover-letter-document">
                  {coverLetter
                    .split('\n')
                    .map((paragraph, index) => {
                      const trimmedParagraph =
                        paragraph.trim()

                      if (!trimmedParagraph) {
                        return (
                          <div
                            key={`space-${index}`}
                            className="cover-letter-document-space"
                          />
                        )
                      }

                      return (
                        <p key={index}>
                          {trimmedParagraph}
                        </p>
                      )
                    })}
                </article>

                <div className="cover-letter-result-footer">
                  <span>
                    AI-generated draft
                  </span>

                  <span>
                    Review and personalize before sending.
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

export default CoverLetter