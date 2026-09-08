import api from './api'

export async function getMyApplications() {
  return api.get('/applications/me', { auth: true })
}