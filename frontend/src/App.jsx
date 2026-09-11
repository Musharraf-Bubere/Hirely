import { BrowserRouter, Route, Routes } from 'react-router-dom'

import MainLayout from './layouts/MainLayout'
import AppShell from './components/layout/AppShell'
import ProtectedRoute from './components/ProtectedRoute'

import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Jobs from './pages/Jobs'
import JobDetail from './pages/JobDetail'
import Applications from './pages/Applications'
import CandidateDashboard from './pages/CandidateDashboard'
import CandidateProfile from './pages/CandidateProfile'
import CandidateResume from './pages/CandidateResume'
import CareerCoach from './pages/CareerCoach'

import RecruiterDashboard from './pages/RecruiterDashboard'
import RecruiterJobs from './pages/RecruiterJobs'
import CreateJob from './pages/CreateJob'
import RecruiterJobDetail from './pages/RecruiterJobDetail'
import RecruiterCandidates from './pages/RecruiterCandidates'

import { AuthProvider } from './context/AuthContext'

import './App.css'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* =====================================================
              Public Routes
          ===================================================== */}

          <Route element={<MainLayout />}>
            <Route path="/" element={<Home />} />

            <Route path="/login" element={<Login />} />

            <Route path="/register" element={<Register />} />

            <Route path="/jobs" element={<Jobs />} />

            <Route
              path="/jobs/:jobId"
              element={<JobDetail />}
            />
          </Route>

          {/* =====================================================
              Candidate Routes
          ===================================================== */}

          <Route
            element={
              <ProtectedRoute allowedRoles={['candidate']} />
            }
          >
            <Route element={<AppShell />}>
              <Route
                path="/candidate/dashboard"
                element={<CandidateDashboard />}
              />

              <Route
                path="/candidate/jobs"
                element={<Jobs />}
              />

              <Route
                path="/candidate/jobs/:jobId"
                element={<JobDetail />}
              />

              <Route
                path="/candidate/applications"
                element={<Applications />}
              />

              <Route
                path="/candidate/profile"
                element={<CandidateProfile />}
              />

              <Route
                path="/candidate/resumes"
                element={<CandidateResume />}
              />

              <Route
                path="/candidate/career-coach"
                element={<CareerCoach />}
              />
            </Route>
          </Route>

          {/* =====================================================
              Recruiter Routes
          ===================================================== */}

          <Route
            element={
              <ProtectedRoute allowedRoles={['recruiter']}
              />
            }
          >
            <Route element={<AppShell />}>

              {/* Recruiter Dashboard */}
              <Route
                path="/recruiter/dashboard"
                element={<RecruiterDashboard />}
              />

              {/* Recruiter Jobs */}
              <Route
                path="/recruiter/jobs"
                element={<RecruiterJobs />}
              />

              {/* Create Job */}
              <Route
                path="/recruiter/jobs/create"
                element={<CreateJob />}
              />

              {/* Recruiter Job Detail */}
              <Route
                path="/recruiter/jobs/:jobId"
                element={<RecruiterJobDetail />}
              />

              {/* AI Candidate Matching */}
              <Route
                path="/recruiter/jobs/:jobId/candidates"
                element={<RecruiterCandidates />}
              />

            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App