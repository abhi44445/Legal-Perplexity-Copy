import { useState, useCallback } from 'react'
import { apiService } from '@/services/api'
import { mockApiService } from '@/services/mockApi'
import type { ConstitutionChatRequest, ConstitutionChatResponse, ApiError } from '@/services/api'

// Flag to use mock API when backend is unavailable
const USE_MOCK_API = true

export interface UseConstitutionChatState {
  isLoading: boolean
  error: ApiError | null
  response: ConstitutionChatResponse | null
}

export const useConstitutionChat = () => {
  const [state, setState] = useState<UseConstitutionChatState>({
    isLoading: false,
    error: null,
    response: null
  })

  const askQuestion = useCallback(async (request: ConstitutionChatRequest) => {
    setState(prev => ({ ...prev, isLoading: true, error: null, response: null }))
    
    try {
      const response = USE_MOCK_API 
        ? await mockApiService.constitutionChat.askQuestion(request)
        : await apiService.constitutionChat.askQuestion(request)
      setState(prev => ({ ...prev, isLoading: false, response }))
      return response
    } catch (error) {
      const apiError = error as ApiError
      setState(prev => ({ ...prev, isLoading: false, error: apiError }))
      throw apiError
    }
  }, [])

  const getSuggestions = useCallback(async (userType = 'general_public') => {
    try {
      const suggestions = USE_MOCK_API
        ? await mockApiService.constitutionChat.getSuggestions(userType)
        : await apiService.constitutionChat.getSuggestions(userType)
      return suggestions
    } catch (error) {
      console.error('Failed to get suggestions:', error)
      throw error as ApiError
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
    askQuestion,
    getSuggestions,
    clearError,
    reset
  }
}