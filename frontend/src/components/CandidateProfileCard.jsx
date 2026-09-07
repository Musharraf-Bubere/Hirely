import { Link } from 'react-router-dom'

function CandidateProfileCard({ profile }) {
  const fullName = `${profile.first_name} ${profile.last_name}`

  return (
    <div className="dashboard-card profile-card">
      <div className="card-header">
        <div>
          <span className="card-label">PROFILE</span>
          <h2>Your Profile</h2>
        </div>

        <Link to="/candidate/profile" className="card-action">
          Edit
        </Link>
      </div>

      <div className="profile-summary">
        <div className="profile-avatar">
          {profile.first_name?.charAt(0).toUpperCase()}
          {profile.last_name?.charAt(0).toUpperCase()}
        </div>

        <div className="profile-info">
          <h3>{fullName}</h3>

          <p>
            {profile.headline || 'Add a professional headline'}
          </p>

          {profile.location && (
            <span>{profile.location}</span>
          )}
        </div>
      </div>

      {profile.bio && (
        <p className="profile-bio">
          {profile.bio}
        </p>
      )}
    </div>
  )
}

export default CandidateProfileCard