import api from './api'

export async function getRecruiterJobs() {
  return api.get('/recruiter/jobs', {
    auth: true,
  })
}

export async function getRecruiterApplications() {
  return api.get('/applications/recruiter', {
    auth: true,
  })
}

export async function createJob(jobData) {
  return api.post('/jobs', jobData, {
    auth: true,
  })
}