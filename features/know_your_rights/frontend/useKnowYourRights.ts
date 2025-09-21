/**
 * Custom hook for Know Your Rights API interactions
 */

import { useState, useCallback } from 'react'
import axios from 'axios'
import type { 
  KnowYourRightsRequest, 
  KnowYourRightsResponse, 
  UseKnowYourRightsState,
  ApiError,
  ValidationRequest
} from './types'

const API_BASE_URL = 'http://localhost:8000'

export const useKnowYourRights = () => {
  const [state, setState] = useState<UseKnowYourRightsState>({
    isLoading: false,
    error: null,
    response: null
  })

  const queryRights = useCallback(async (request: KnowYourRightsRequest): Promise<KnowYourRightsResponse> => {
    setState(prev => ({ ...prev, isLoading: true, error: null, response: null }))
    
    try {
      const response = await axios.post<KnowYourRightsResponse>(
        `${API_BASE_URL}/api/know-your-rights/query`,
        request,
        {
          timeout: 120000, // 2 minutes timeout for AI processing
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
      
      setState(prev => ({ ...prev, isLoading: false, response: response.data }))
      return response.data
    } catch (error) {
      const apiError = processApiError(error)
      setState(prev => ({ ...prev, isLoading: false, error: apiError }))
      throw apiError
    }
  }, [])

  const validateOutput = useCallback(async (validationRequest: ValidationRequest): Promise<void> => {
    try {
      await axios.post(
        `${API_BASE_URL}/api/know-your-rights/validate`,
        validationRequest,
        {
          timeout: 10000,
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
    } catch (error) {
      console.error('Validation failed:', error)
      throw processApiError(error)
    }
  }, [])

  const checkHealth = useCallback(async (): Promise<{ status: string; message: string }> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/know-your-rights/health`, {
        timeout: 10000
      })
      return response.data
    } catch (error) {
      throw processApiError(error)
    }
  }, [])

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  const reset = useCallback(() => {
    setState({
      isLoading: false,
      error: null,
      response: null
    })
  }, [])

  return {
    ...state,
    queryRights,
    validateOutput,
    checkHealth,
    clearError,
    reset
  }
}

// Helper function to process API errors consistently
function processApiError(error: any): ApiError {
  if (axios.isAxiosError(error)) {
    if (error.code === 'ECONNREFUSED') {
      return {
        message: 'Unable to connect to the Know Your Rights service. Please check if the server is running.',
        status: 503,
        detail: 'Connection refused'
      }
    }
    
    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      return {
        message: 'The AI is taking longer than expected to analyze your situation. Please try again with a simpler description.',
        status: 408,
        detail: 'Request timeout'
      }
    }
    
    if (error.response) {
      return {
        message: error.response.data?.detail || error.response.data?.message || `Server error (${error.response.status})`,
        status: error.response.status,
        detail: error.response.data?.detail
      }
    }
    
    return {
      message: error.message || 'Network error occurred',
      status: 0,
      detail: 'Network error'
    }
  }
  
  return {
    message: error?.message || 'An unexpected error occurred',
    status: 500,
    detail: 'Unknown error'
  }
}

// Export additional API utility functions
export const knowYourRightsApi = {
  async query(request: KnowYourRightsRequest): Promise<KnowYourRightsResponse> {
    const response = await axios.post<KnowYourRightsResponse>(
      `${API_BASE_URL}/api/know-your-rights/query`,
      request,
      {
        timeout: 120000,
        headers: { 'Content-Type': 'application/json' }
      }
    )
    return response.data
  },

  async validate(validationRequest: ValidationRequest): Promise<void> {
    await axios.post(
      `${API_BASE_URL}/api/know-your-rights/validate`,
      validationRequest,
      {
        timeout: 10000,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  },

  async health(): Promise<{ status: string; message: string }> {
    const response = await axios.get(`${API_BASE_URL}/api/know-your-rights/health`, {
      timeout: 10000
    })
    return response.data
  }
}

export default useKnowYourRights