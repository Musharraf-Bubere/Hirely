import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import {
  createCandidateProfile,
  getCandidateProfile,
  updateCandidateProfile,
} from '../services/candidate'

function CandidateProfile() {
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    headline: '',
    bio: '',
    location: '',
  })

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [profileExists, setProfileExists] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    async function loadProfile() {
      try {
        const profile = await getCandidateProfile()

        setFormData({
          first_name: profile.first_name || '',
          last_name: profile.last_name || '',
          headline: profile.headline || '',
          bio: profile.bio || '',
          location: profile.location || '',
        })

        setProfileExists(true)
      } catch (err) {
        if (!err.message.toLowerCase().includes('not found')) {
          setError(err.message)
        }
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [])

  function handleChange(event) {
    const { name, value } = event.target

    setFormData((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setSuccess('')
    setSaving(true)

    try {
      const profile = profileExists
        ? await updateCandidateProfile(formData)
        : await createCandidateProfile(formData)

      setFormData({
        first_name: profile.first_name || '',
        last_name: profile.last_name || '',
        headline: profile.headline || '',
        bio: profile.bio || '',
        location: profile.location || '',
      })

      setProfileExists(true)

      setSuccess(
        profileExists
          ? 'Profile updated successfully.'
          : 'Profile created successfully.'
      )

      setTimeout(() => {
        navigate('/candidate/dashboard')
      }, 700)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <main className="loading-page">
        <p>Loading profile...</p>
      </main>
    )
  }

  return (
    <section className="profile-section">
      <div className="profile-container">
        <div className="page-header">
          <div>
            <span className="eyebrow">
              CANDIDATE PROFILE
            </span>

            <h1>
              {profileExists
                ? 'Update your profile'
                : 'Create your profile'}
            </h1>

            <p>
              Build your professional profile so Hirely can
              understand your background and match you with
              relevant opportunities.
            </p>
          </div>

          <Link
            to="/candidate/dashboard"
            className="secondary-button"
          >
            Back to Dashboard
          </Link>
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {success && (
          <div className="success-message" role="status">
            {success}
          </div>
        )}

        <form
          className="profile-form"
          onSubmit={handleSubmit}
        >
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">
                First Name
              </label>

              <input
                id="first_name"
                name="first_name"
                type="text"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="First name"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="last_name">
                Last Name
              </label>

              <input
                id="last_name"
                name="last_name"
                type="text"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Last name"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="headline">
              Professional Headline
            </label>

            <input
              id="headline"
              name="headline"
              type="text"
              value={formData.headline}
              onChange={handleChange}
              placeholder="e.g. Data Scientist | Machine Learning Engineer"
            />
          </div>

          <div className="form-group">
            <label htmlFor="location">
              Location
            </label>

            <input
              id="location"
              name="location"
              type="text"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g. Mumbai, India"
            />
          </div>

          <div className="form-group">
            <label htmlFor="bio">
              Professional Bio
            </label>

            <textarea
              id="bio"
              name="bio"
              value={formData.bio}
              onChange={handleChange}
              placeholder="Tell recruiters about your professional background..."
              rows="6"
            />
          </div>

          <div className="profile-form-actions">
            <Link
              to="/candidate/dashboard"
              className="secondary-button"
            >
              Cancel
            </Link>

            <button
              type="submit"
              className="primary-button"
              disabled={saving}
            >
              {saving
                ? 'Saving...'
                : profileExists
                  ? 'Update Profile'
                  : 'Create Profile'}
            </button>
          </div>
        </form>
      </div>
    </section>
  )
}

export default CandidateProfile