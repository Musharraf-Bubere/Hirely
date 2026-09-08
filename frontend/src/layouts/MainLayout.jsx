import { Outlet } from 'react-router-dom'

import Navbar from '../components/Navbar'

function MainLayout() {
  return (
    <div className="public-shell">
      <Navbar />

      <main className="public-main">
        <Outlet />
      </main>

      <footer className="public-footer">
        <div className="public-footer-inner">
          <div className="footer-brand">
            <span className="brand-mark">✦</span>
            <strong>Hirely</strong>
          </div>

          <p>
            Intelligent hiring. Better opportunities.
          </p>

          <span>
            © 2026 Hirely
          </span>
        </div>
      </footer>
    </div>
  )
}

export default MainLayout