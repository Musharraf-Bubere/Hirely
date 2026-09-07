import api from './api'

const ACCESS_TOKEN_KEY = 'hirely_access_token'

export async function registerUser({ email, password, role }) {
  return api.post('/auth/register', {
    email,
    password,
    role,
  })
}

export async function loginUser({ email, password }) {
  const data = await api.post('/auth/login', {
    email,
    password,
  })

  localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token)

  return data
}

export async function getCurrentUser() {
  return api.get('/auth/me', {
    auth: true,
  })
}

export function logoutUser() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function isAuthenticated() {
  return Boolean(getAccessToken())
}