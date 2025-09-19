// API service for communicating with the SYSE backend
const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  constructor() {
    this.apiKey = null;
  }

  setApiKey(apiKey) {
    this.apiKey = apiKey;
  }

  async generateScript(index) {
    if (!this.apiKey) {
      throw new Error('API key is required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/generate%20script?index=${index}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Validate response structure
      if (!data.scripts || !Array.isArray(data.scripts)) {
        throw new Error('Invalid response format: missing scripts array');
      }

      return data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Failed to connect to backend server. Please ensure the backend is running.');
      }
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: 'GET',
      });
      
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }
      
      const data = await response.json();
      return data.status === 'ok';
    } catch (error) {
      console.warn('Backend health check failed:', error);
      return false;
    }
  }
}

// Create singleton instance
const apiService = new ApiService();

export default apiService;