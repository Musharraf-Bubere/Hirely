import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

function Login() {
  const navigate = useNavigate()
  const location = useLocation()

  const { login } = useAuth()

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

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
    setLoading(true)

    try {
      const user = await login(formData)

      if (user.role === 'candidate') {
        navigate('/candidate/dashboard', { replace: true })
      } else if (user.role === 'recruiter') {
        navigate('/recruiter/dashboard', { replace: true })
      } else {
        navigate('/', { replace: true })
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const from = location.state?.from

  return (
    <section className="auth-section">
      <div className="auth-card">
        <div className="auth-header">
          <span className="eyebrow">WELCOME BACK</span>

          <h1>Sign in to Hirely</h1>

          <p>
            Access your candidate or recruiter account.
          </p>
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>

            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              required
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>

            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="primary-button full-width"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="auth-footer-text">
          Don't have an account?{' '}
          <Link to="/register">Create one</Link>
        </p>

        {from && (
          <p className="auth-redirect-message">
            Please sign in to continue.
          </p>
        )}
      </div>
    </section>
  )
}

export default Login