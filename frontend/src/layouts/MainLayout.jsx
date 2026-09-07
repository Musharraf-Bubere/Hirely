import { Outlet } from 'react-router-dom'

import Navbar from '../components/Navbar'

function MainLayout() {
  return (
    <div className="app-shell">
      <Navbar />

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="footer">
        <div className="container">
          <p>© 2026 Hirely. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default MainLayout