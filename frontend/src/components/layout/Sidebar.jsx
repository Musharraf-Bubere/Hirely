import { NavLink } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const candidateNavigation = [
  {
    label: 'Workspace',
    items: [
      { label: 'Overview', path: '/candidate/dashboard', icon: '⌂' },
      { label: 'Find Jobs', path: '/candidate/jobs', icon: '⌕' },
      { label: 'Applications', path: '/candidate/applications', icon: '✓' },
    ],
  },
  {
    label: 'Career',
    items: [
      { label: 'Profile', path: '/candidate/profile', icon: '◎' },
      { label: 'Resume', path: '/candidate/resumes', icon: '▤' },
    ],
  },
  {
    label: 'AI Tools',
    items: [
      {
        label: 'Career Coach',
        path: '/candidate/career-coach',
        icon: '✦',
      },
      {
        label: 'Cover Letter',
        path: '/candidate/cover-letter',
        icon: '✎',
      },
    ],
  },
]

const recruiterNavigation = [
  {
    label: 'Workspace',
    items: [
      { label: 'Overview', path: '/recruiter/dashboard', icon: '⌂' },
      { label: 'Jobs', path: '/recruiter/jobs', icon: '▣' },
      { label: 'Candidates', path: '/recruiter/candidates', icon: '◎' },
      {
        label: 'Applications',
        path: '/recruiter/applications',
        icon: '✓',
      },
    ],
  },
  {
    label: 'Hiring',
    items: [
      {
        label: 'Create Job',
        path: '/recruiter/jobs/create',
        icon: '+',
      },
      {
        label: 'AI Matching',
        path: '/recruiter/matching',
        icon: '✦',
      },
    ],
  },
  {
    label: 'Company',
    items: [
      {
        label: 'Company Profile',
        path: '/recruiter/profile',
        icon: '◉',
      },
    ],
  },
]

function Sidebar({ mobileOpen, onClose }) {
  const { user } = useAuth()

  const navigation =
    user?.role === 'recruiter'
      ? recruiterNavigation
      : candidateNavigation

  const roleLabel =
    user?.role === 'recruiter'
      ? 'Recruiter Workspace'
      : 'Candidate Workspace'

  return (
    <>
      {mobileOpen && (
        <button
          type="button"
          className="sidebar-overlay"
          aria-label="Close navigation"
          onClick={onClose}
        />
      )}

      <aside
        className={`app-sidebar ${
          mobileOpen ? 'app-sidebar-open' : ''
        }`}
      >
        <div className="sidebar-brand">
          <NavLink to="/" className="sidebar-logo">
            <span className="brand-mark">✦</span>
            <span>Hirely</span>
          </NavLink>

          <button
            type="button"
            className="sidebar-close"
            onClick={onClose}
            aria-label="Close navigation"
          >
            ×
          </button>
        </div>

        <div className="sidebar-workspace">
          <span className="sidebar-workspace-dot" />
          <span>{roleLabel}</span>
        </div>

        <nav className="sidebar-navigation">
          {navigation.map((section) => (
            <div
              className="sidebar-section"
              key={section.label}
            >
              <p className="sidebar-section-label">
                {section.label}
              </p>

              <div className="sidebar-items">
                {section.items.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    onClick={onClose}
                    className={({ isActive }) =>
                      `sidebar-link ${
                        isActive ? 'sidebar-link-active' : ''
                      }`
                    }
                  >
                    <span className="sidebar-link-icon">
                      {item.icon}
                    </span>

                    <span>{item.label}</span>
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <NavLink
            to={
              user?.role === 'recruiter'
                ? '/recruiter/profile'
                : '/candidate/profile'
            }
            onClick={onClose}
            className="sidebar-account"
          >
            <span className="sidebar-avatar">
              {user?.email?.charAt(0).toUpperCase() || 'U'}
            </span>

            <span className="sidebar-account-info">
              <strong>{user?.email || 'User'}</strong>
              <small>
                {user?.role === 'recruiter'
                  ? 'Recruiter'
                  : 'Candidate'}
              </small>
            </span>

            <span className="sidebar-account-arrow">→</span>
          </NavLink>
        </div>
      </aside>
    </>
  )
}

export default Sidebar