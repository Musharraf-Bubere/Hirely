import { createContext, useContext, useEffect, useState } from 'react'

import {
  getAccessToken,
  getCurrentUser,
  loginUser,
  logoutUser,
  registerUser,
} from '../services/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadUser() {
      const token = getAccessToken()

      if (!token) {
        setLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)
      } catch (err) {
        // Only clear authentication state if the backend explicitly rejected the token (401).
        // Transient network errors or 5xx server issues should not wipe saved credentials.
        if (err?.status === 401) {
          logoutUser()
          setUser(null)
        }
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [])

  useEffect(() => {
    function handleSessionExpired() {
      logoutUser()
      setUser(null)
    }

    if (typeof window !== 'undefined') {
      window.addEventListener('auth:session_expired', handleSessionExpired)
      return () => {
        window.removeEventListener('auth:session_expired', handleSessionExpired)
      }
    }
  }, [])

  async function login(credentials) {
    await loginUser(credentials)

    const currentUser = await getCurrentUser()

    setUser(currentUser)

    return currentUser
  }

  async function register(data) {
    return registerUser(data)
  }

  function logout() {
    logoutUser()
    setUser(null)
  }

  const value = {
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }

  return context
}
