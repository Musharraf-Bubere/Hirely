import api from './api'

export async function getRecruiterJobs() {
  return api.get('/recruiter/jobs', { auth: true })
}

export async function getRecruiterApplications() {
  return api.get('/applications/recruiter', { auth: true })
}

export async function createJob(jobData) {
  return api.post('/jobs', jobData, { auth: true })
}

export async function addJobSkill(jobId, skillData) {
  return api.post(`/jobs/${jobId}/skills`, skillData, { auth: true })
}

export async function getJobSkills(jobId) {
  return api.get(`/jobs/${jobId}/skills`, { auth: true })
}

export async function removeJobSkill(jobId, skillId) {
  return api.delete(`/jobs/${jobId}/skills/${skillId}`, { auth: true })
}

export async function matchCandidatesToJob(jobId) {
  return api.post(`/jobs/${jobId}/candidates/match`, null, {
    auth: true,
  })
}

export async function explainCandidatesForJob(
  jobId,
  explanationLimit = 5,
) {
  return api.post(
    `/jobs/${jobId}/candidates/match/explain?explanation_limit=${explanationLimit}`,
    null,
    { auth: true },
  )
}

export async function updateApplicationStatus(
  applicationId,
  status,
) {
  return api.patch(
    `/applications/${applicationId}/status`,
    { status },
    { auth: true },
  )
}