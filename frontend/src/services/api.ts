import axios from 'axios'
import type { AxiosResponse, AxiosError } from 'axios'

// Types for API responses
export interface ConstitutionChatRequest {
  query: string
  user_type?: string
}

export interface ConstitutionChatResponse {
  answer: string
  reasoning: string
  citations: Array<{
    type: string
    reference: string
    is_valid: boolean
  }>
  citation_validation: Record<string, any>
  response_time: number
  confidence_score?: number
  user_type: string
}

export interface ApiError {
  message: string
  status: number
  detail?: string
}

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 120000, // 2 minutes timeout for AI responses (was 30 seconds)
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging and auth
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error: AxiosError) => {
    console.error('❌ Response Error:', error)
    
    const apiError: ApiError = {
      message: 'An error occurred',
      status: error.response?.status || 500,
      detail: error.message
    }

    if (error.response?.status === 404) {
      apiError.message = 'Resource not found'
    } else if (error.response?.status === 500) {
      apiError.message = 'Internal server error'
    } else if (error.response?.status === 503) {
      apiError.message = 'Service temporarily unavailable'
    } else if (error.code === 'ECONNREFUSED') {
      apiError.message = 'Unable to connect to server'
    } else if (error.code === 'ECONNABORTED') {
      apiError.message = 'The AI is taking longer than expected to process your question. Please try a simpler question or try again later.'
    } else if (error.message?.includes('timeout')) {
      apiError.message = 'The AI response is taking longer than expected. Please wait or try again with a simpler question.'
    }

    return Promise.reject(apiError)
  }
)

// API service functions
export const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      throw error as ApiError
    }
  },

  // Constitution Chat
  constitutionChat: {
    askQuestion: async (request: ConstitutionChatRequest): Promise<ConstitutionChatResponse> => {
      try {
        const response = await api.post('/api/chat/constitution', request)
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    getSuggestions: async (user_type = 'general_public') => {
      try {
        const response = await api.get(`/api/chat/suggestions?user_type=${user_type}`)
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    getHistory: async () => {
      try {
        const response = await api.get('/api/chat/history')
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    }
  },

  // Rights
  rights: {
    getCategories: async () => {
      try {
        const response = await api.get('/api/rights/categories')
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    search: async (query: string, category?: string) => {
      try {
        const response = await api.post('/api/rights/search', { query, category })
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    }
  },

  // Cases
  cases: {
    predictOutcome: async (caseDetails: any) => {
      try {
        const response = await api.post('/api/cases/predict', caseDetails)
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    findSimilar: async (caseSummary: string, caseType?: string) => {
      try {
        const response = await api.post('/api/cases/similar', { 
          case_summary: caseSummary, 
          case_type: caseType 
        })
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    }
  },

  // Research
  research: {
    search: async (query: string, filters?: any) => {
      try {
        const response = await api.post('/api/research/search', { query, ...filters })
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    getDocument: async (documentId: string) => {
      try {
        const response = await api.get(`/api/research/document/${documentId}`)
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    summarize: async (text: string, summaryType = 'brief') => {
      try {
        const response = await api.post('/api/research/summarize', { 
          text, 
          summary_type: summaryType 
        })
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    }
  },

  // Know Your Rights
  knowYourRights: {
    query: async (request: { scenario: string; text: string; language?: string; user_id?: string }) => {
      try {
        const response = await api.post('/api/know-your-rights/query', {
          ...request,
          language: request.language || 'en'
        })
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    validate: async (validationRequest: { output_id: string; expected: any; score: number; notes: string }) => {
      try {
        const response = await api.post('/api/know-your-rights/validate', validationRequest)
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    },

    healthCheck: async () => {
      try {
        const response = await api.get('/api/know-your-rights/health')
        return response.data
      } catch (error) {
        throw error as ApiError
      }
    }
  }
}

export default api