import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import ResumeCard from '../components/ResumeCard'
import {
  activateResume,
  getResumes,
  parseResume,
  uploadResume,
} from '../services/resume'

function CandidateResume() {
  const fileInputRef = useRef(null)

  const [resumes, setResumes] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)

  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [activatingId, setActivatingId] = useState(null)
  const [parsingId, setParsingId] = useState(null)

  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function loadResumes() {
    try {
      setError('')

      const data = await getResumes()

      setResumes(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResumes()
  }, [])

  function handleFileChange(event) {
    const file = event.target.files?.[0] || null

    setSelectedFile(file)
    setError('')
    setSuccess('')
  }

  async function handleUpload(event) {
    event.preventDefault()

    if (!selectedFile) {
      setError('Please select a PDF or DOCX resume.')
      return
    }

    setError('')
    setSuccess('')
    setUploading(true)

    try {
      await uploadResume(selectedFile)

      setSelectedFile(null)

      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }

      await loadResumes()

      setSuccess(
        'Resume uploaded successfully.',
      )
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  async function handleParse(resumeId) {
    setError('')
    setSuccess('')
    setParsingId(resumeId)

    try {
      await parseResume(resumeId)

      await loadResumes()

      setSuccess(
        'Resume parsed successfully and candidate skills were synchronized.',
      )
    } catch (err) {
      setError(err.message)

      await loadResumes()
    } finally {
      setParsingId(null)
    }
  }

  async function handleActivate(resumeId) {
    setError('')
    setSuccess('')
    setActivatingId(resumeId)

    try {
      await activateResume(resumeId)

      await loadResumes()

      setSuccess('Active resume updated successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setActivatingId(null)
    }
  }

  return (
    <section className="resume-section">
      <div className="container resume-container">
        <div className="page-header">
          <div>
            <span className="eyebrow">
              RESUME MANAGEMENT
            </span>

            <h1>Your Resumes</h1>

            <p>
              Upload, parse, and manage your resumes.
              Hirely uses parsed resume information to
              power candidate skills and AI-powered job
              matching.
            </p>
          </div>

          <Link
            to="/candidate/dashboard"
            className="secondary-button"
          >
            Back to Dashboard
          </Link>
        </div>

        {error && (
          <div
            className="error-message"
            role="alert"
          >
            {error}
          </div>
        )}

        {success && (
          <div
            className="success-message"
            role="status"
          >
            {success}
          </div>
        )}

        <div className="resume-upload-card">
          <div>
            <span className="card-label">
              UPLOAD RESUME
            </span>

            <h2>Add a new resume</h2>

            <p>
              Supported formats: PDF and DOCX.
              Maximum file size: 10 MB.
            </p>
          </div>

          <form
            className="resume-upload-form"
            onSubmit={handleUpload}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              onChange={handleFileChange}
            />

            {selectedFile && (
              <p className="selected-file">
                Selected: {selectedFile.name}
              </p>
            )}

            <button
              type="submit"
              className="primary-button"
              disabled={
                uploading || !selectedFile
              }
            >
              {uploading
                ? 'Uploading...'
                : 'Upload Resume'}
            </button>
          </form>
        </div>

        <div className="resume-list-section">
          <div className="section-heading">
            <div>
              <span className="card-label">
                YOUR FILES
              </span>

              <h2>Resume Versions</h2>
            </div>

            <span className="resume-count">
              {resumes.length} resume
              {resumes.length === 1 ? '' : 's'}
            </span>
          </div>

          {loading ? (
            <div className="dashboard-card loading-card">
              <p>Loading resumes...</p>
            </div>
          ) : resumes.length === 0 ? (
            <div className="dashboard-card empty-state">
              <h3>No resumes yet</h3>

              <p>
                Upload your first resume to start
                building your Hirely candidate profile.
              </p>
            </div>
          ) : (
            <div className="resume-list">
              {resumes.map((resume) => (
                <ResumeCard
                  key={resume.id}
                  resume={resume}
                  onActivate={handleActivate}
                  onParse={handleParse}
                  activating={
                    activatingId === resume.id
                  }
                  parsing={
                    parsingId === resume.id
                  }
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default CandidateResume