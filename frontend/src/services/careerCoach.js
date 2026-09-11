import api from './api'

export async function askCareerCoach(message) {
  return api.post(
    '/candidate/career-coach',
    { message },
    {
      auth: true,
    },
  )
}