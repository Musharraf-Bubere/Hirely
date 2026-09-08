import { useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

function getPageTitle(pathname, role) {
  if (pathname.includes('/profile')) {
    return role === 'recruiter'
      ? 'Company Profile'
      : 'Profile'
  }

  if (pathname.includes('/resumes')) {
    return 'Resume Center'
  }

  if (pathname.includes('/applications')) {
    return 'Applications'
  }

  if (pathname.includes('/career-coach')) {
    return 'AI Career Coach'
  }

  if (pathname.includes('/cover-letter')) {
    return 'Cover Letter'
  }

  if (pathname.includes('/jobs/create')) {
    return 'Create Job'
  }

  if (pathname.includes('/jobs/')) {
    return 'Job Details'
  }

  if (pathname.includes('/jobs')) {
    return role === 'recruiter'
      ? 'Jobs'
      : 'Find Jobs'
  }

  if (pathname.includes('/candidates')) {
    return 'Candidates'
  }

  if (pathname.includes('/matching')) {
    return 'AI Matching'
  }

  return 'Overview'
}

function Topbar({ onMenuClick }) {
  const location = useLocation()
  const { user } = useAuth()

  const title = getPageTitle(
    location.pathname,
    user?.role,
  )

  const initial =
    user?.email?.charAt(0).toUpperCase() || 'U'

  return (
    <header className="app-topbar">
      <div className="topbar-left">
        <button
          type="button"
          className="mobile-menu-button"
          onClick={onMenuClick}
          aria-label="Open navigation"
        >
          <span />
          <span />
          <span />
        </button>

        <div className="topbar-heading">
          <span className="topbar-context">
            Hirely
          </span>

          <h1>{title}</h1>
        </div>
      </div>

      <div className="topbar-right">
        <button
          type="button"
          className="topbar-icon-button"
          aria-label="Notifications"
        >
          <span className="notification-icon">♢</span>
          <span className="notification-dot" />
        </button>

        <div className="topbar-divider" />

        <div className="topbar-user">
          <span className="topbar-avatar">
            {initial}
          </span>

          <div className="topbar-user-info">
            <strong>
              {user?.email || 'Hirely User'}
            </strong>

            <span>
              {user?.role === 'recruiter'
                ? 'Recruiter'
                : 'Candidate'}
            </span>
          </div>

          <span className="topbar-chevron">⌄</span>
        </div>
      </div>
    </header>
  )
}

export default Topbar