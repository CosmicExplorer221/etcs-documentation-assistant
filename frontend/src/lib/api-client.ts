import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    })

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor to handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            const refreshToken = this.getRefreshToken()
            if (refreshToken) {
              const response = await this.client.post('/auth/refresh', {
                refresh_token: refreshToken,
              })

              const { access_token, refresh_token } = response.data
              this.setTokens(access_token, refresh_token)

              // Retry original request
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${access_token}`
              }
              return this.client(originalRequest)
            }
          } catch (refreshError) {
            this.clearTokens()
            if (typeof window !== 'undefined') {
              window.location.href = '/login'
            }
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  private getAccessToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('access_token')
  }

  private getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('refresh_token')
  }

  private setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === 'undefined') return
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
  }

  private clearTokens(): void {
    if (typeof window === 'undefined') return
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  // Auth methods
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', { email, password })
    const { access_token, refresh_token, user } = response.data
    this.setTokens(access_token, refresh_token)
    return { user, accessToken: access_token }
  }

  async register(email: string, password: string, full_name: string) {
    const response = await this.client.post('/auth/register', {
      email,
      password,
      full_name,
    })
    return response.data
  }

  async logout() {
    this.clearTokens()
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me')
    return response.data
  }

  // Chat methods
  async sendMessage(conversationId: string | null, message: string, style: string) {
    const response = await this.client.post('/chat/message', {
      conversation_id: conversationId,
      message,
      style,
    })
    return response.data
  }

  async getConversations() {
    const response = await this.client.get('/chat/conversations')
    return response.data
  }

  async getConversation(conversationId: string) {
    const response = await this.client.get(`/chat/conversations/${conversationId}`)
    return response.data
  }

  async deleteConversation(conversationId: string) {
    await this.client.delete(`/chat/conversations/${conversationId}`)
  }

  // Document methods
  async getDocuments() {
    const response = await this.client.get('/documents')
    return response.data
  }

  async uploadDocument(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await this.client.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  }

  // Bookmarks
  async getBookmarks() {
    const response = await this.client.get('/bookmarks')
    return response.data
  }

  async createBookmark(data: {
    conversation_id: string
    message_id: string
    note?: string
  }) {
    const response = await this.client.post('/bookmarks', data)
    return response.data
  }

  async deleteBookmark(bookmarkId: string) {
    await this.client.delete(`/bookmarks/${bookmarkId}`)
  }

  // Search
  async searchDocuments(query: string, filters?: Record<string, any>) {
    const response = await this.client.post('/search', { query, filters })
    return response.data
  }
}

export const apiClient = new ApiClient()
