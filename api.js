// API service for Sparko backend
const API_BASE_URL = 'https://0vhlizck0gvv.manus.space/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('sparko_token')
  }

  // Helper method to get headers
  getHeaders(includeAuth = true) {
    const headers = {
      'Content-Type': 'application/json',
    }
    
    if (includeAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }
    
    return headers
  }

  // Helper method to handle responses
  async handleResponse(response) {
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.error || data.message || 'API request failed')
    }
    
    return data
  }

  // Authentication APIs
  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: this.getHeaders(false),
      body: JSON.stringify(userData)
    })
    
    const data = await this.handleResponse(response)
    
    if (data.token) {
      this.token = data.token
      localStorage.setItem('sparko_token', data.token)
      localStorage.setItem('sparko_user', JSON.stringify(data.user))
    }
    
    return data
  }

  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: this.getHeaders(false),
      body: JSON.stringify(credentials)
    })
    
    const data = await this.handleResponse(response)
    
    if (data.token) {
      this.token = data.token
      localStorage.setItem('sparko_token', data.token)
      localStorage.setItem('sparko_user', JSON.stringify(data.user))
    }
    
    return data
  }

  async getProfile() {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  async updateProfile(profileData) {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(profileData)
    })
    
    const data = await this.handleResponse(response)
    
    if (data.user) {
      localStorage.setItem('sparko_user', JSON.stringify(data.user))
    }
    
    return data
  }

  // Multi-role profile APIs
  async getUserProfiles() {
    const response = await fetch(`${API_BASE_URL}/profile/profiles`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  async getProfileByRole(role) {
    const response = await fetch(`${API_BASE_URL}/profile/profiles/${role}`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  async updateProfileByRole(role, profileData) {
    const response = await fetch(`${API_BASE_URL}/profile/profiles/${role}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(profileData)
    })
    
    return this.handleResponse(response)
  }

  async switchRole(role) {
    const response = await fetch(`${API_BASE_URL}/profile/switch-role`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ role })
    })
    
    const data = await this.handleResponse(response)
    
    // Update local user data
    const currentUser = this.getCurrentUser()
    if (currentUser) {
      currentUser.current_role = role
      localStorage.setItem('sparko_user', JSON.stringify(currentUser))
    }
    
    return data
  }

  async checkProfileCompletion(role) {
    const response = await fetch(`${API_BASE_URL}/profile/check-completion/${role}`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  // Matching APIs
  async discoverProfiles() {
    const response = await fetch(`${API_BASE_URL}/matching/discover`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  async swipe(userId, action) {
    const response = await fetch(`${API_BASE_URL}/matching/swipe`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({
        user_id: userId,
        action: action
      })
    })
    
    return this.handleResponse(response)
  }

  async getMatches() {
    const response = await fetch(`${API_BASE_URL}/matching/matches`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  async resetSuperSparks() {
    const response = await fetch(`${API_BASE_URL}/matching/super-spark/reset`, {
      method: 'POST',
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  // Chat APIs
  async getMessages(matchId) {
    const response = await fetch(`${API_BASE_URL}/chat/matches/${matchId}/messages`, {
      headers: this.getHeaders()
    })
    
    return this.handleResponse(response)
  }

  async sendMessage(matchId, content) {
    const response = await fetch(`${API_BASE_URL}/chat/matches/${matchId}/messages`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ content })
    })
    
    return this.handleResponse(response)
  }

  // Premium APIs
  async purchaseSuperSpark(quantity = 1) {
    const response = await fetch(`${API_BASE_URL}/premium/purchase/super-spark`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ quantity })
    })
    
    return this.handleResponse(response)
  }

  async purchasePremium(plan = 'monthly') {
    const response = await fetch(`${API_BASE_URL}/premium/purchase/premium`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ plan })
    })
    
    return this.handleResponse(response)
  }

  async unlockChatEarly(matchId) {
    const response = await fetch(`${API_BASE_URL}/premium/features/unlock-chat-early`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ match_id: matchId })
    })
    
    return this.handleResponse(response)
  }

  async getFeedback(matchId) {
    const response = await fetch(`${API_BASE_URL}/premium/features/feedback`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ match_id: matchId })
    })
    
    return this.handleResponse(response)
  }

  async downloadLegalDocument(documentType) {
    const response = await fetch(`${API_BASE_URL}/premium/features/legal-documents`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ document_type: documentType })
    })
    
    return this.handleResponse(response)
  }

  // Utility methods
  logout() {
    this.token = null
    localStorage.removeItem('sparko_token')
    localStorage.removeItem('sparko_user')
  }

  isAuthenticated() {
    return !!this.token
  }

  getCurrentUser() {
    const userStr = localStorage.getItem('sparko_user')
    return userStr ? JSON.parse(userStr) : null
  }

  getCurrentRole() {
    const user = this.getCurrentUser()
    return user ? user.current_role || 'entrepreneur' : 'entrepreneur'
  }
}

export default new ApiService()

