import { BrowserRouter, Route, Routes } from 'react-router-dom'

import MainLayout from './layouts/MainLayout'
import ProtectedRoute from './components/ProtectedRoute'

import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import CandidateDashboard from './pages/CandidateDashboard'
import CandidateProfile from './pages/CandidateProfile'
import CandidateResume from './pages/CandidateResume'

import { AuthProvider } from './context/AuthContext'

import './App.css'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route
              path="/"
              element={<Home />}
            />

            <Route
              path="/login"
              element={<Login />}
            />

            <Route
              path="/register"
              element={<Register />}
            />

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['candidate']}
                />
              }
            >
              <Route
                path="/candidate/dashboard"
                element={<CandidateDashboard />}
              />

              <Route
                path="/candidate/profile"
                element={<CandidateProfile />}
              />

              <Route
                path="/candidate/resumes"
                element={<CandidateResume />}
              />
            </Route>

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['recruiter']}
                />
              }
            >
              <Route
                path="/recruiter/dashboard"
                element={
                  <main className="placeholder-page">
                    <h1>
                      Recruiter Dashboard
                    </h1>

                    <p>
                      Recruiter dashboard coming next.
                    </p>
                  </main>
                }
              />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App