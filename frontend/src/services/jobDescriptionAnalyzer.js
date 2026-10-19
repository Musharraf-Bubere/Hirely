import api from './api'

export async function analyzeJobDescription(jobId) {
  return api.post(`/recruiter/jobs/${jobId}/description-analysis`, null, {
    auth: true,
  })
}

export default {
  analyzeJobDescription,
}
