import { useState } from 'react'
import { Outlet } from 'react-router-dom'

import Sidebar from './Sidebar'
import Topbar from './Topbar'

function AppShell() {
  const [mobileOpen, setMobileOpen] = useState(false)

  function closeMobileSidebar() {
    setMobileOpen(false)
  }

  return (
    <div className="app-shell authenticated-shell">
      <Sidebar
        mobileOpen={mobileOpen}
        onClose={closeMobileSidebar}
      />

      <div className="workspace">
        <Topbar
          onMenuClick={() => setMobileOpen(true)}
        />

        <main className="workspace-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppShell