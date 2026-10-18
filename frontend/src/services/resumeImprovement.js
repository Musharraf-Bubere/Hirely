import api from './api'

export async function getResumeImprovement(jobId) {
  return api.post(
    '/candidate/resume-improvement',
    { job_id: jobId },
    {
      auth: true,
    },
  )
}

export const generateResumeImprovement = getResumeImprovement

export default {
  getResumeImprovement,
  generateResumeImprovement,
}
