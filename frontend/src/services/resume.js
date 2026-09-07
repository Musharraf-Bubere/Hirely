import api from './api'

export async function uploadResume(file) {
  const formData = new FormData()

  formData.append('resume', file)

  return api.upload('/resumes', formData, {
    auth: true,
  })
}

export async function getResumes() {
  return api.get('/resumes', {
    auth: true,
  })
}

export async function activateResume(resumeId) {
  return api.patch(
    `/resumes/${resumeId}/activate`,
    null,
    {
      auth: true,
    },
  )
}

export async function parseResume(resumeId) {
  return api.post(
    `/resumes/${resumeId}/parse`,
    null,
    {
      auth: true,
    },
  )
}