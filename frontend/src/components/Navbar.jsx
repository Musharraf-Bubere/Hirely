import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

function Navbar() {
  const navigate = useNavigate()

  const { user, isAuthenticated, logout } = useAuth()

  function handleLogout() {
    logout()
    navigate('/', { replace: true })
  }

  return (
    <nav className="navbar">
      <div className="container navbar-content">
        <Link to="/" className="brand">
          Hirely
        </Link>

        <div className="nav-links">
          <Link to="/" className="nav-link">
            Home
          </Link>

          {!isAuthenticated && (
            <>
              <Link to="/login" className="nav-link">
                Login
              </Link>

              <Link to="/register" className="nav-button">
                Get Started
              </Link>
            </>
          )}

          {isAuthenticated && user?.role === 'candidate' && (
            <Link
              to="/candidate/dashboard"
              className="nav-button"
            >
              Dashboard
            </Link>
          )}

          {isAuthenticated && user?.role === 'recruiter' && (
            <Link
              to="/recruiter/dashboard"
              className="nav-button"
            >
              Dashboard
            </Link>
          )}

          {isAuthenticated && (
            <button
              type="button"
              className="nav-link nav-logout"
              onClick={handleLogout}
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar