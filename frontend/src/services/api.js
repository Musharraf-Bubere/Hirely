const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function apiRequest(endpoint, options = {}) {
  const {
    method = 'GET',
    body,
    headers = {},
    auth = false,
  } = options

  const requestHeaders = {
    ...headers,
  }

  if (!(body instanceof FormData)) {
    requestHeaders['Content-Type'] = 'application/json'
  }

  if (auth) {
    const token = localStorage.getItem('hirely_access_token')

    if (token) {
      requestHeaders.Authorization = `Bearer ${token}`
    }
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers: requestHeaders,
    body:
      body instanceof FormData
        ? body
        : body
          ? JSON.stringify(body)
          : undefined,
  })

  let data = null

  const contentType = response.headers.get('content-type')

  if (contentType?.includes('application/json')) {
    data = await response.json()
  } else {
    data = await response.text()
  }

  if (!response.ok) {
    const message =
      typeof data === 'object' && data?.detail
        ? data.detail
        : 'Something went wrong. Please try again.'

    throw new Error(message)
  }

  return data
}

export const api = {
  get: (endpoint, options = {}) =>
    apiRequest(endpoint, {
      ...options,
      method: 'GET',
    }),

  post: (endpoint, body, options = {}) =>
    apiRequest(endpoint, {
      ...options,
      method: 'POST',
      body,
    }),

  put: (endpoint, body, options = {}) =>
    apiRequest(endpoint, {
      ...options,
      method: 'PUT',
      body,
    }),

  patch: (endpoint, body, options = {}) =>
    apiRequest(endpoint, {
      ...options,
      method: 'PATCH',
      body,
    }),

  delete: (endpoint, options = {}) =>
    apiRequest(endpoint, {
      ...options,
      method: 'DELETE',
    }),

  upload: (endpoint, formData, options = {}) =>
    apiRequest(endpoint, {
      ...options,
      method: 'POST',
      body: formData,
    }),
}

export default api