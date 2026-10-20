import test, { describe, beforeEach } from 'node:test'
import assert from 'node:assert/strict'

// Create test environment globals before importing api module
class MockLocalStorage {
  constructor() {
    this.store = new Map()
  }
  getItem(key) {
    return this.store.has(key) ? this.store.get(key) : null
  }
  setItem(key, value) {
    this.store.set(key, String(value))
  }
  removeItem(key) {
    this.store.delete(key)
  }
  clear() {
    this.store.clear()
  }
}

class MockEventTarget {
  constructor() {
    this.listeners = new Map()
    this.dispatchedEvents = []
    this.location = {
      pathname: '/candidate/dashboard',
      href: 'http://localhost:5173/candidate/dashboard',
    }
  }

  addEventListener(type, listener) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, [])
    }
    this.listeners.get(type).push(listener)
  }

  removeEventListener(type, listener) {
    const list = this.listeners.get(type) || []
    this.listeners.set(type, list.filter(l => l !== listener))
  }

  dispatchEvent(event) {
    this.dispatchedEvents.push(event.type || event)
    const list = this.listeners.get(event.type || event) || []
    for (const listener of list) {
      listener(event)
    }
    return true
  }
}

const mockLocalStorage = new MockLocalStorage()
const mockWindow = new MockEventTarget()

globalThis.localStorage = mockLocalStorage
globalThis.window = mockWindow
globalThis.CustomEvent = class CustomEvent {
  constructor(type, options = {}) {
    this.type = type
    this.detail = options.detail || null
  }
}
globalThis.Event = class Event {
  constructor(type) {
    this.type = type
  }
}

// Dynamically import api module
const { default: api } = await import('./api.js')

describe('API Service — Session Expiration & Auth Interceptor', () => {
  beforeEach(() => {
    mockLocalStorage.clear()
    mockWindow.dispatchedEvents = []
    mockWindow.location.pathname = '/candidate/dashboard'
    mockWindow.location.href = 'http://localhost:5173/candidate/dashboard'
  })

  test('401 on protected endpoint clears token, dispatches event, and redirects to login', async () => {
    mockLocalStorage.setItem('hirely_access_token', 'valid-or-expired-jwt-token')

    globalThis.fetch = async () => ({
      ok: false,
      status: 401,
      headers: { get: () => 'application/json' },
      json: async () => ({ detail: 'Token has expired' }),
    })

    await assert.rejects(
      async () => {
        await api.get('/resumes', { auth: true })
      },
      (err) => {
        assert.equal(err.status, 401)
        assert.equal(err.message, 'Token has expired')
        return true
      }
    )

    // Token must be cleared
    assert.equal(mockLocalStorage.getItem('hirely_access_token'), null)
    // auth:session_expired event must be dispatched
    assert.ok(mockWindow.dispatchedEvents.includes('auth:session_expired'))
    // Must redirect to /login with session_expired query parameter
    assert.equal(mockWindow.location.href, '/login?session_expired=true')
  })

  test('401 on /auth/login does NOT clear token, does NOT dispatch session_expired, and does NOT redirect', async () => {
    mockLocalStorage.setItem('hirely_access_token', 'existing-token')

    globalThis.fetch = async () => ({
      ok: false,
      status: 401,
      headers: { get: () => 'application/json' },
      json: async () => ({ detail: 'Invalid email or password' }),
    })

    await assert.rejects(
      async () => {
        await api.post('/auth/login', { email: 'bad@example.com', password: 'wrong' })
      },
      (err) => {
        assert.equal(err.status, 401)
        assert.equal(err.message, 'Invalid email or password')
        return true
      }
    )

    // Token should remain intact
    assert.equal(mockLocalStorage.getItem('hirely_access_token'), 'existing-token')
    // No session_expired event
    assert.equal(mockWindow.dispatchedEvents.includes('auth:session_expired'), false)
    // No redirect triggered
    assert.equal(mockWindow.location.href, 'http://localhost:5173/candidate/dashboard')
  })

  test('401 on /auth/register does NOT clear state or redirect', async () => {
    mockLocalStorage.setItem('hirely_access_token', 'existing-token')

    globalThis.fetch = async () => ({
      ok: false,
      status: 401,
      headers: { get: () => 'application/json' },
      json: async () => ({ detail: 'Unauthorized registration' }),
    })

    await assert.rejects(
      async () => {
        await api.post('/auth/register', { email: 'test@example.com' })
      },
      (err) => {
        assert.equal(err.status, 401)
        return true
      }
    )

    assert.equal(mockLocalStorage.getItem('hirely_access_token'), 'existing-token')
    assert.equal(mockWindow.dispatchedEvents.includes('auth:session_expired'), false)
    assert.equal(mockWindow.location.href, 'http://localhost:5173/candidate/dashboard')
  })

  test('403 Forbidden does NOT log out or redirect', async () => {
    mockLocalStorage.setItem('hirely_access_token', 'valid-candidate-token')

    globalThis.fetch = async () => ({
      ok: false,
      status: 403,
      headers: { get: () => 'application/json' },
      json: async () => ({ detail: 'Recruiter role required' }),
    })

    await assert.rejects(
      async () => {
        await api.get('/recruiter/jobs', { auth: true })
      },
      (err) => {
        assert.equal(err.status, 403)
        assert.equal(err.message, 'Recruiter role required')
        return true
      }
    )

    // Token must NOT be removed on 403
    assert.equal(mockLocalStorage.getItem('hirely_access_token'), 'valid-candidate-token')
    assert.equal(mockWindow.dispatchedEvents.includes('auth:session_expired'), false)
    assert.equal(mockWindow.location.href, 'http://localhost:5173/candidate/dashboard')
  })

  test('Ordinary network error does NOT log out or redirect', async () => {
    mockLocalStorage.setItem('hirely_access_token', 'valid-candidate-token')

    globalThis.fetch = async () => {
      throw new TypeError('Failed to fetch')
    }

    await assert.rejects(
      async () => {
        await api.get('/jobs')
      },
      (err) => {
        assert.match(err.message, /Failed to fetch/)
        return true
      }
    )

    assert.equal(mockLocalStorage.getItem('hirely_access_token'), 'valid-candidate-token')
    assert.equal(mockWindow.dispatchedEvents.includes('auth:session_expired'), false)
    assert.equal(mockWindow.location.href, 'http://localhost:5173/candidate/dashboard')
  })

  test('401 while already on /login avoids redirect loop', async () => {
    mockWindow.location.pathname = '/login'
    mockWindow.location.href = 'http://localhost:5173/login?session_expired=true'

    globalThis.fetch = async () => ({
      ok: false,
      status: 401,
      headers: { get: () => 'application/json' },
      json: async () => ({ detail: 'Session expired' }),
    })

    await assert.rejects(
      async () => {
        await api.get('/auth/me', { auth: true })
      },
      (err) => {
        assert.equal(err.status, 401)
        return true
      }
    )

    // Should NOT re-assign href since pathname already starts with /login
    assert.equal(mockWindow.location.href, 'http://localhost:5173/login?session_expired=true')
  })
})
