import api from './api'

export async function getCandidateProfile() {
  return api.get('/candidate/profile', {
    auth: true,
  })
}

export async function createCandidateProfile(profileData) {
  return api.post('/candidate/profile', profileData, {
    auth: true,
  })
}

export async function updateCandidateProfile(profileData) {
  return api.patch('/candidate/profile', profileData, {
    auth: true,
  })
}