import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { createJob } from '../services/recruiter'

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
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function handleChange(event) {
    const { name, value } = event.target

    setForm((current) => ({
      ...current,
      [name]: value,
    }))
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

      navigate(
        createdJob?.id
          ? `/recruiter/jobs/${createdJob.id}`
          : '/recruiter/jobs',
      )
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
          ← Back to jobs
        </Link>

        <span className="recruiter-eyebrow">
          Hiring workspace
        </span>

        <h1>Create a new job</h1>

        <p>
          Define the opportunity clearly so Hirely can help
          you identify the strongest candidates.
        </p>
      </section>

      <form
        className="recruiter-job-form"
        onSubmit={handleSubmit}
      >
        <section className="recruiter-form-card">
          <div className="recruiter-form-heading">
            <div>
              <span className="recruiter-section-eyebrow">
                Job information
              </span>

              <h2>Opportunity details</h2>
            </div>
          </div>

          <div className="recruiter-form-grid">
            <div className="recruiter-form-field full">
              <label htmlFor="title">
                Job title <span>*</span>
              </label>

              <input
                id="title"
                name="title"
                type="text"
                value={form.title}
                onChange={handleChange}
                placeholder="e.g. Senior Python Backend Developer"
                required
              />
            </div>

            <div className="recruiter-form-field full">
              <label htmlFor="description">
                Job description <span>*</span>
              </label>

              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Describe the role, responsibilities, requirements, and what success looks like..."
                rows="9"
                required
              />

              <span className="recruiter-field-help">
                A detailed description gives the AI matching
                engine better context.
              </span>
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
                <option value="full_time">Full Time</option>
                <option value="part_time">Part Time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
                <option value="freelance">Freelance</option>
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
                <option value="entry">Entry Level</option>
                <option value="junior">Junior</option>
                <option value="mid">Mid Level</option>
                <option value="senior">Senior</option>
                <option value="lead">Lead</option>
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
            {loading ? 'Creating job...' : 'Create Job →'}
          </button>
        </div>
      </form>
    </main>
  )
}