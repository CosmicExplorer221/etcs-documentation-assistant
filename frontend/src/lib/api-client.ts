import axios, { AxiosInstance } from 'axios'

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
    const response = await this.client.get('/documents/list')
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
