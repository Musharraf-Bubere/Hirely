import api from './api'

export async function generateCoverLetter(jobId) {
  return api.post(
    '/candidate/cover-letter',
    { job_id: jobId },
    {
      auth: true,
    },
  )
}