import { useState, useCallback } from 'react'
import { apiService } from '@/services/api'
import type { ConstitutionChatRequest, ConstitutionChatResponse, ApiError } from '@/services/api'

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
      const response = await apiService.constitutionChat.askQuestion(request)
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
      const suggestions = await apiService.constitutionChat.getSuggestions(userType)
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