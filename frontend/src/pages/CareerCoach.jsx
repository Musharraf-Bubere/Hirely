import { useState } from 'react'

import { askCareerCoach } from '../services/careerCoach'

import './CareerCoach.css'

const exampleQuestions = [
  'What skills should I improve to become an AI Engineer?',
  'How can I make my profile stronger for AI roles?',
  'What should I learn next based on my current skills?',
]

function CareerCoach() {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()

    const trimmedMessage = message.trim()

    if (!trimmedMessage || loading) {
      return
    }

    setLoading(true)
    setError('')

    try {
      const data = await askCareerCoach(trimmedMessage)

      setResponse(data)
    } catch (err) {
      setError(
        err.message ||
          'Career Coach is temporarily unavailable. Please try again.',
      )
    } finally {
      setLoading(false)
    }
  }

  function handleExampleClick(question) {
    setMessage(question)
    setError('')
  }

  return (
    <section className="career-coach-page">
      <div className="career-coach-container">
        <header className="career-coach-hero">
          <div>
            <span className="career-coach-overline">
              AI CAREER COACH
            </span>

            <h1>
              Build your next career move
              <span className="career-coach-accent">.</span>
            </h1>

            <p>
              Get personalized career guidance based on your
              Hirely profile, skills, resume, and application
              journey.
            </p>
          </div>

          <div className="career-coach-hero-badge">
            <span className="career-coach-badge-icon">✦</span>
            <span>Personalized AI guidance</span>
          </div>
        </header>

        <div className="career-coach-main-grid">
          <section className="career-coach-ask-card">
            <div className="career-coach-card-heading">
              <div>
                <span className="career-coach-section-label">
                  ASK ANYTHING
                </span>

                <h2>What would you like help with?</h2>
              </div>

              <div className="career-coach-card-icon">
                ✦
              </div>
            </div>

            <form
              className="career-coach-form"
              onSubmit={handleSubmit}
            >
              <label
                htmlFor="career-coach-message"
                className="career-coach-label"
              >
                Your question
              </label>

              <textarea
                id="career-coach-message"
                className="career-coach-textarea"
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
                placeholder="For example: What skills should I improve to become an AI Engineer?"
                maxLength={4000}
                rows={7}
                disabled={loading}
              />

              <div className="career-coach-form-footer">
                <span className="career-coach-character-count">
                  {message.length}/4000
                </span>

                <button
                  type="submit"
                  className="primary-button career-coach-submit"
                  disabled={!message.trim() || loading}
                >
                  {loading ? (
                    <>
                      <span className="career-coach-spinner" />
                      Thinking...
                    </>
                  ) : (
                    <>
                      Ask Career Coach
                      <span>→</span>
                    </>
                  )}
                </button>
              </div>
            </form>

            {error && (
              <div className="career-coach-error" role="alert">
                <span className="career-coach-error-icon">
                  !
                </span>

                <div>
                  <strong>Unable to get guidance</strong>
                  <p>{error}</p>
                </div>
              </div>
            )}

            <div className="career-coach-examples">
              <span>Try asking:</span>

              <div className="career-coach-example-list">
                {exampleQuestions.map((question) => (
                  <button
                    key={question}
                    type="button"
                    className="career-coach-example"
                    onClick={() =>
                      handleExampleClick(question)
                    }
                    disabled={loading}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </section>

          <aside className="career-coach-capabilities">
            <div className="career-coach-capabilities-glow" />

            <span className="career-coach-section-label">
              CAREER COMPANION
            </span>

            <h2>
              Guidance built around
              <span> your journey.</span>
            </h2>

            <p>
              Career Coach uses the information already available
              in your Hirely profile to provide more relevant
              recommendations.
            </p>

            <div className="career-coach-capability-list">
              <div className="career-coach-capability">
                <span className="career-coach-capability-icon">
                  ↗
                </span>

                <div>
                  <strong>Career direction</strong>
                  <p>
                    Explore realistic next steps for your target
                    role.
                  </p>
                </div>
              </div>

              <div className="career-coach-capability">
                <span className="career-coach-capability-icon">
                  ◇
                </span>

                <div>
                  <strong>Skill gaps</strong>
                  <p>
                    Identify skills that can strengthen your
                    profile.
                  </p>
                </div>
              </div>

              <div className="career-coach-capability">
                <span className="career-coach-capability-icon">
                  +
                </span>

                <div>
                  <strong>Learning priorities</strong>
                  <p>
                    Turn career goals into practical learning
                    steps.
                  </p>
                </div>
              </div>

              <div className="career-coach-capability">
                <span className="career-coach-capability-icon">
                  ✓
                </span>

                <div>
                  <strong>Job readiness</strong>
                  <p>
                    Get advice on becoming stronger for your
                    target roles.
                  </p>
                </div>
              </div>
            </div>
          </aside>
        </div>

        {response && (
          <section className="career-coach-response">
            <div className="career-coach-response-header">
              <div>
                <span className="career-coach-section-label">
                  AI GUIDANCE
                </span>

                <h2>Your personalized guidance</h2>
              </div>

              <span className="career-coach-response-status">
                <span />
                Generated for your profile
              </span>
            </div>

            <div className="career-coach-answer">
              <h3>Answer</h3>
              <p>{response.answer}</p>
            </div>

            <div className="career-coach-insights-grid">
              <InsightSection
                title="Recommendations"
                items={response.recommendations}
                icon="↗"
              />

              <InsightSection
                title="Skills to improve"
                items={response.skills_to_improve}
                icon="◇"
              />

              <InsightSection
                title="Next steps"
                items={response.next_steps}
                icon="✓"
              />
            </div>
          </section>
        )}
      </div>
    </section>
  )
}

function InsightSection({ title, items, icon }) {
  return (
    <div className="career-coach-insight">
      <div className="career-coach-insight-heading">
        <span>{icon}</span>
        <h3>{title}</h3>
      </div>

      {items?.length ? (
        <ul>
          {items.map((item, index) => (
            <li key={`${title}-${index}`}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="career-coach-no-insights">
          No specific items were identified.
        </p>
      )}
    </div>
  )
}

export default CareerCoach