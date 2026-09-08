import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Navbar() {
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuth()

  function handleLogout() {
    logout()
    navigate('/', { replace: true })
  }

  function getDashboardPath() {
    if (user?.role === 'recruiter') {
      return '/recruiter/dashboard'
    }

    return '/candidate/dashboard'
  }

  return (
    <header className="public-navbar">
      <div className="public-navbar-inner">
        <Link to="/" className="brand">
          <span className="brand-mark">✦</span>
          <span>Hirely</span>
        </Link>

        <nav className="public-nav-links">
          <Link to="/jobs" className="public-nav-link">
            Find Jobs
          </Link>

          <a href="#how-it-works" className="public-nav-link">
            How It Works
          </a>

          <a href="#for-recruiters" className="public-nav-link">
            For Recruiters
          </a>
        </nav>

        <div className="public-nav-actions">
          {!isAuthenticated ? (
            <>
              <Link to="/login" className="public-sign-in">
                Sign In
              </Link>

              <Link to="/register" className="public-nav-cta">
                Get Started
                <span>→</span>
              </Link>
            </>
          ) : (
            <>
              <Link
                to={getDashboardPath()}
                className="public-sign-in"
              >
                Dashboard
              </Link>

              <button
                type="button"
                className="public-nav-cta"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

export default Navbar