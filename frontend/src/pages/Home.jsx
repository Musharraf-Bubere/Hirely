import { Link } from 'react-router-dom'

function Home() {
  return (
    <section className="hero-section">
      <div className="container hero-content">
        <div className="hero-text">
          <span className="eyebrow">AI-POWERED RECRUITMENT</span>

          <h1>
            Find the right talent.
            <br />
            <span>Build the right future.</span>
          </h1>

          <p>
            Hirely connects candidates with the right opportunities using
            intelligent resume analysis, semantic job matching, candidate
            ranking, and AI-powered insights.
          </p>

          <div className="hero-actions">
            <Link to="/register" className="primary-button">
              Get Started
            </Link>

            <Link to="/login" className="secondary-button">
              Sign In
            </Link>
          </div>
        </div>

        <div className="hero-card">
          <div className="hero-card-header">
            <span>AI Match Score</span>
            <span className="match-score">92%</span>
          </div>

          <div className="match-profile">
            <div className="avatar">JD</div>

            <div>
              <h3>Software Engineer</h3>
              <p>Strong match for your requirements</p>
            </div>
          </div>

          <div className="skill-list">
            <span>Python</span>
            <span>FastAPI</span>
            <span>Machine Learning</span>
            <span>SQL</span>
          </div>

          <div className="match-bar">
            <div className="match-bar-fill"></div>
          </div>

          <p className="match-description">
            Skills, experience, and semantic profile similarity indicate a
            strong match.
          </p>
        </div>
      </div>
    </section>
  )
}

export default Home