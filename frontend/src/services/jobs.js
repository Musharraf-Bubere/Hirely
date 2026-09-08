import api from './api'

export async function getJobs() {
  return api.get('/jobs')
}

export async function getJob(jobId) {
  return api.get(`/jobs/${jobId}`)
}

export async function applyToJob(jobId) {
  return api.post(`/jobs/${jobId}/apply`, null, { auth: true })
}

export async function matchCandidateToJob(jobId) {
  return api.post(`/jobs/${jobId}/match`, null, { auth: true })
}