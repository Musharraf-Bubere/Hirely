import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import {
  addJobSkill,
  createJob,
} from '../services/recruiter'

import './Recruiter.css'

const INITIAL_FORM = {
  title: '',
  description: '',
  location: '',
  employment_type: '',
  experience_level: '',
  salary_min: '',
  salary_max: '',
}

export default function CreateJob() {
  const navigate = useNavigate()

  const [form, setForm] = useState(INITIAL_FORM)

  const [requiredSkills, setRequiredSkills] = useState([])
  const [preferredSkills, setPreferredSkills] = useState([])

  const [requiredSkillInput, setRequiredSkillInput] = useState('')
  const [preferredSkillInput, setPreferredSkillInput] = useState('')

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function handleChange(event) {
    const { name, value } = event.target

    setForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function normalizeSkill(skill) {
    return skill.trim().replace(/\s+/g, ' ')
  }

  function addSkill(
    input,
    setInput,
    setSkills,
    existingSkills,
    otherSkills,
  ) {
    const skill = normalizeSkill(input)

    if (!skill) {
      return
    }

    const normalizedSkill = skill.toLowerCase()

    const alreadyExists =
      existingSkills.some(
        (item) => item.toLowerCase() === normalizedSkill,
      ) ||
      otherSkills.some(
        (item) => item.toLowerCase() === normalizedSkill,
      )

    if (alreadyExists) {
      setError(`"${skill}" has already been added.`)
      return
    }

    setSkills((current) => [...current, skill])
    setInput('')
    setError('')
  }

  function removeSkill(skill, setSkills) {
    setSkills((current) =>
      current.filter((item) => item !== skill),
    )
  }

  function handleRequiredSkillKeyDown(event) {
    if (event.key === 'Enter') {
      event.preventDefault()

      addSkill(
        requiredSkillInput,
        setRequiredSkillInput,
        setRequiredSkills,
        requiredSkills,
        preferredSkills,
      )
    }
  }

  function handlePreferredSkillKeyDown(event) {
    if (event.key === 'Enter') {
      event.preventDefault()

      addSkill(
        preferredSkillInput,
        setPreferredSkillInput,
        setPreferredSkills,
        preferredSkills,
        requiredSkills,
      )
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')

    if (!form.title.trim()) {
      setError('Job title is required.')
      return
    }

    if (!form.description.trim()) {
      setError('Job description is required.')
      return
    }

    if (!form.employment_type.trim()) {
      setError('Employment type is required.')
      return
    }

    if (
      form.salary_min &&
      form.salary_max &&
      Number(form.salary_min) > Number(form.salary_max)
    ) {
      setError(
        'Minimum salary cannot be greater than maximum salary.',
      )
      return
    }

    setLoading(true)

    try {
      const payload = {
        title: form.title.trim(),
        description: form.description.trim(),
        location: form.location.trim() || null,
        employment_type: form.employment_type.trim(),
        experience_level:
          form.experience_level.trim() || null,
        salary_min: form.salary_min
          ? Number(form.salary_min)
          : null,
        salary_max: form.salary_max
          ? Number(form.salary_max)
          : null,
      }

      const createdJob = await createJob(payload)

      if (!createdJob?.id) {
        throw new Error(
          'Job was created but no job ID was returned.',
        )
      }

      for (const skill of requiredSkills) {
        await addJobSkill(createdJob.id, {
          name: skill,
          is_required: true,
        })
      }

      for (const skill of preferredSkills) {
        await addJobSkill(createdJob.id, {
          name: skill,
          is_required: false,
        })
      }

      navigate(`/recruiter/jobs/${createdJob.id}`)
    } catch (requestError) {
      setError(
        requestError?.message ||
          'Unable to create the job. Please try again.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="recruiter-page recruiter-create-page">
      <section className="recruiter-create-header">
        <Link
          to="/recruiter/jobs"
          className="recruiter-back-link"
        >
          ← Back to Jobs
        </Link>

        <div>
          <span className="recruiter-section-eyebrow">
            Recruiter workspace
          </span>

          <h1>Create a new job</h1>

          <p>
            Define the opportunity and the skills Hirely should use
            when finding the strongest candidates.
          </p>
        </div>
      </section>

      <form
        className="recruiter-create-form"
        onSubmit={handleSubmit}
      >
        <section className="recruiter-form-section">
          <div className="recruiter-form-section-header">
            <div className="recruiter-form-section-number">
              01
            </div>

            <div>
              <span className="recruiter-section-eyebrow">
                Job information
              </span>

              <h2>Tell candidates about the opportunity</h2>

              <p>
                Provide the core details recruiters and candidates
                need to understand this role.
              </p>
            </div>
          </div>

          <div className="recruiter-form-grid">
            <div className="recruiter-form-field recruiter-form-field-full">
              <label htmlFor="title">
                Job title <span>*</span>
              </label>

              <input
                id="title"
                name="title"
                type="text"
                value={form.title}
                onChange={handleChange}
                placeholder="e.g. Senior Machine Learning Engineer"
                required
              />
            </div>

            <div className="recruiter-form-field recruiter-form-field-full">
              <label htmlFor="description">
                Job description <span>*</span>
              </label>

              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Describe the role, responsibilities, technical requirements, and what the candidate will work on..."
                rows="8"
                required
              />
            </div>

            <div className="recruiter-form-field">
              <label htmlFor="location">
                Location
              </label>

              <input
                id="location"
                name="location"
                type="text"
                value={form.location}
                onChange={handleChange}
                placeholder="e.g. Mumbai / Remote"
              />
            </div>

            <div className="recruiter-form-field">
              <label htmlFor="employment_type">
                Employment type <span>*</span>
              </label>

              <select
                id="employment_type"
                name="employment_type"
                value={form.employment_type}
                onChange={handleChange}
                required
              >
                <option value="">
                  Select employment type
                </option>

                <option value="full_time">
                  Full Time
                </option>

                <option value="part_time">
                  Part Time
                </option>

                <option value="contract">
                  Contract
                </option>

                <option value="internship">
                  Internship
                </option>

                <option value="freelance">
                  Freelance
                </option>
              </select>
            </div>

            <div className="recruiter-form-field">
              <label htmlFor="experience_level">
                Experience level
              </label>

              <select
                id="experience_level"
                name="experience_level"
                value={form.experience_level}
                onChange={handleChange}
              >
                <option value="">
                  Select experience level
                </option>

                <option value="entry">
                  Entry Level
                </option>

                <option value="junior">
                  Junior
                </option>

                <option value="mid">
                  Mid Level
                </option>

                <option value="senior">
                  Senior
                </option>

                <option value="lead">
                  Lead
                </option>
              </select>
            </div>

            <div className="recruiter-form-field">
              <label htmlFor="salary_min">
                Minimum salary
              </label>

              <input
                id="salary_min"
                name="salary_min"
                type="number"
                min="0"
                value={form.salary_min}
                onChange={handleChange}
                placeholder="e.g. 600000"
              />
            </div>

            <div className="recruiter-form-field">
              <label htmlFor="salary_max">
                Maximum salary
              </label>

              <input
                id="salary_max"
                name="salary_max"
                type="number"
                min="0"
                value={form.salary_max}
                onChange={handleChange}
                placeholder="e.g. 1200000"
              />
            </div>
          </div>
        </section>

        <section className="recruiter-form-section">
          <div className="recruiter-form-section-header">
            <div className="recruiter-form-section-number">
              02
            </div>

            <div>
              <span className="recruiter-section-eyebrow">
                AI matching criteria
              </span>

              <h2>Define the skills that matter</h2>

              <p>
                Hirely uses these skills when calculating candidate
                compatibility and ranking applicants.
              </p>
            </div>
          </div>

          <div className="recruiter-skills-grid">
            <div className="recruiter-skill-editor required">
              <div className="recruiter-skill-editor-header">
                <div>
                  <span className="recruiter-skill-label required">
                    Required
                  </span>

                  <h3>Must-have skills</h3>
                </div>

                <span className="recruiter-skill-count">
                  {requiredSkills.length}
                </span>
              </div>

              <p className="recruiter-skill-help">
                Skills a candidate should have to be considered a
                strong match.
              </p>

              <div className="recruiter-skill-input-row">
                <input
                  type="text"
                  value={requiredSkillInput}
                  onChange={(event) =>
                    setRequiredSkillInput(event.target.value)
                  }
                  onKeyDown={handleRequiredSkillKeyDown}
                  placeholder="e.g. Python"
                />

                <button
                  type="button"
                  onClick={() =>
                    addSkill(
                      requiredSkillInput,
                      setRequiredSkillInput,
                      setRequiredSkills,
                      requiredSkills,
                      preferredSkills,
                    )
                  }
                >
                  Add
                </button>
              </div>

              <div className="recruiter-skill-chips">
                {requiredSkills.length === 0 ? (
                  <span className="recruiter-skill-empty">
                    No required skills added yet.
                  </span>
                ) : (
                  requiredSkills.map((skill) => (
                    <span
                      className="recruiter-skill-chip required"
                      key={skill}
                    >
                      {skill}

                      <button
                        type="button"
                        aria-label={`Remove ${skill}`}
                        onClick={() =>
                          removeSkill(
                            skill,
                            setRequiredSkills,
                          )
                        }
                      >
                        ×
                      </button>
                    </span>
                  ))
                )}
              </div>
            </div>

            <div className="recruiter-skill-editor preferred">
              <div className="recruiter-skill-editor-header">
                <div>
                  <span className="recruiter-skill-label preferred">
                    Preferred
                  </span>

                  <h3>Nice-to-have skills</h3>
                </div>

                <span className="recruiter-skill-count">
                  {preferredSkills.length}
                </span>
              </div>

              <p className="recruiter-skill-help">
                Additional skills that can improve a candidate's
                ranking.
              </p>

              <div className="recruiter-skill-input-row">
                <input
                  type="text"
                  value={preferredSkillInput}
                  onChange={(event) =>
                    setPreferredSkillInput(event.target.value)
                  }
                  onKeyDown={handlePreferredSkillKeyDown}
                  placeholder="e.g. Docker"
                />

                <button
                  type="button"
                  onClick={() =>
                    addSkill(
                      preferredSkillInput,
                      setPreferredSkillInput,
                      setPreferredSkills,
                      preferredSkills,
                      requiredSkills,
                    )
                  }
                >
                  Add
                </button>
              </div>

              <div className="recruiter-skill-chips">
                {preferredSkills.length === 0 ? (
                  <span className="recruiter-skill-empty">
                    No preferred skills added yet.
                  </span>
                ) : (
                  preferredSkills.map((skill) => (
                    <span
                      className="recruiter-skill-chip preferred"
                      key={skill}
                    >
                      {skill}

                      <button
                        type="button"
                        aria-label={`Remove ${skill}`}
                        onClick={() =>
                          removeSkill(
                            skill,
                            setPreferredSkills,
                          )
                        }
                      >
                        ×
                      </button>
                    </span>
                  ))
                )}
              </div>
            </div>
          </div>
        </section>

        {error && (
          <div className="recruiter-form-error">
            <span>!</span>
            <p>{error}</p>
          </div>
        )}

        <div className="recruiter-form-actions">
          <Link
            to="/recruiter/jobs"
            className="recruiter-cancel-button"
          >
            Cancel
          </Link>

          <button
            type="submit"
            className="recruiter-primary-button"
            disabled={loading}
          >
            {loading
              ? 'Creating job...'
              : 'Create Job →'}
          </button>
        </div>
      </form>
    </main>
  )
}