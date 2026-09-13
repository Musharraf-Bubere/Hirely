import api from './api'

export async function analyzeResumeATS(jobId) {
  return api.post(
    '/candidate/ats-analysis',
    { job_id: jobId },
    {
      auth: true,
    },
  )
}