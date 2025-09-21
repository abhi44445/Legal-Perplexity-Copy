import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import FormattedResponse from '../components/FormattedResponse'
import { motion } from 'framer-motion'
import { Send, User, Bot, ArrowLeft, BookOpen, CheckCircle, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { useConstitutionChat } from '@/hooks/useConstitutionChat'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  reasoning?: string
  citations?: Array<{
    type: string
    reference: string
    is_valid: boolean
  }>
  timestamp: Date
}

const ConstitutionChatPage: React.FC = () => {
  const navigate = useNavigate()
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [showReasoning, setShowReasoning] = useState<{ [key: string]: boolean }>({})
  
  // Use the API hook
  const { isLoading, error, askQuestion, clearError } = useConstitutionChat()

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const currentQuery = inputValue
    setInputValue('')
    clearError()

    try {
      const response = await askQuestion({
        query: currentQuery,
        user_type: 'general_public'
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        reasoning: response.reasoning,
        citations: response.citations,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error?.message || 'Please try again later.'}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleSuggestionClick = async (suggestion: string) => {
    setInputValue(suggestion)
    
    // Automatically send the suggestion
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: suggestion,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    clearError()

    try {
      const response = await askQuestion({
        query: suggestion,
        user_type: 'general_public'
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        reasoning: response.reasoning,
        citations: response.citations,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error?.message || 'Please try again later.'}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const toggleReasoning = (messageId: string) => {
    setShowReasoning(prev => ({
      ...prev,
      [messageId]: !prev[messageId]
    }))
  }

  return (
    <div className="min-h-screen bg-neo-white">
      {/* Header */}
      <motion.div 
        className="border-b-4 border-neo-black bg-neo-white"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" className="p-2" onClick={() => navigate('/')}>
                <ArrowLeft className="h-6 w-6" />
              </Button>
              <div className="flex items-center gap-3">
                <div className="p-2 bg-neo-black">
                  <BookOpen className="h-6 w-6 text-neo-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-neo-black font-inter">Constitution Chat</h1>
                  <p className="text-neo-gray-500 font-inter">Ask questions about the Indian Constitution</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Chat Area */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6 mb-24">
          {messages.length === 0 && (
            <motion.div 
              className="text-center py-16"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6 }}
            >
              <div className="text-6xl mb-6">⚖️</div>
              <h2 className="text-3xl font-bold text-neo-black mb-4 font-inter">
                Ask Your Constitutional Questions
              </h2>
              <p className="text-lg text-neo-gray-500 mb-8 max-w-2xl mx-auto font-inter">
                Get expert AI-powered insights about the Indian Constitution with proper citations and reasoning.
              </p>
              
              {/* Quick suggestions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                {[
                  "What is Article 21 about?",
                  "Explain fundamental rights",
                  "What are directive principles?",
                  "How does Article 370 work?"
                ].map((suggestion, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    className="text-left h-auto p-4"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    {suggestion}
                  </Button>
                ))}
              </div>
            </motion.div>
          )}

          {messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {message.type === 'assistant' && (
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-neo-black flex items-center justify-center">
                    <Bot className="h-5 w-5 text-neo-white" />
                  </div>
                </div>
              )}

              <div className={`max-w-3xl ${message.type === 'user' ? 'order-first' : ''}`}>
                <Card className={`${message.type === 'user' ? 'bg-neo-black text-neo-white border-neo-black' : ''}`}>
                  <CardContent className="p-6">
                    {message.type === 'assistant' ? (
                      <FormattedResponse content={message.content} />
                    ) : (
                      <div className="prose prose-lg max-w-none">
                        <p className={`font-inter leading-relaxed ${message.type === 'user' ? 'text-neo-white' : 'text-neo-black'}`}>
                          {message.content}
                        </p>
                      </div>
                    )}

                    {message.type === 'assistant' && message.reasoning && (
                      <div className="mt-4">
                        <Button
                          variant="ghost"
                          onClick={() => toggleReasoning(message.id)}
                          className="text-sm"
                        >
                          {showReasoning[message.id] ? 'Hide Reasoning' : 'Show Reasoning'}
                        </Button>
                        
                        {showReasoning[message.id] && (
                          <motion.div 
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            className="mt-3 p-4 bg-neo-gray-100 border-l-4 border-neo-black"
                          >
                            <h4 className="font-bold mb-2 font-inter">AI Reasoning:</h4>
                            <p className="text-sm text-neo-gray-700 font-inter">{message.reasoning}</p>
                          </motion.div>
                        )}
                      </div>
                    )}

                    {message.type === 'assistant' && message.citations && (
                      <div className="mt-4">
                        <h4 className="font-bold mb-2 text-sm font-inter">Citations:</h4>
                        <div className="flex flex-wrap gap-2">
                          {message.citations.map((citation, idx) => (
                            <div
                              key={idx}
                              className="flex items-center gap-2 px-3 py-1 bg-neo-white border-2 border-neo-black text-xs font-medium"
                            >
                              {citation.is_valid ? (
                                <CheckCircle className="h-3 w-3 text-green-600" />
                              ) : (
                                <AlertCircle className="h-3 w-3 text-red-600" />
                              )}
                              {citation.reference}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>

              {message.type === 'user' && (
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-neo-gray-200 flex items-center justify-center">
                    <User className="h-5 w-5 text-neo-black" />
                  </div>
                </div>
              )}
            </motion.div>
          ))}

          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex gap-4"
            >
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-neo-black flex items-center justify-center">
                  <Bot className="h-5 w-5 text-neo-white" />
                </div>
              </div>
              <Card className="max-w-3xl">
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 text-neo-gray-500">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-neo-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-neo-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-neo-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                    <span className="font-inter">AI is analyzing constitutional law... This may take up to 2 minutes.</span>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>

      {/* Input Area - Fixed at bottom */}
      <motion.div 
        className="fixed bottom-0 left-0 right-0 bg-neo-white border-t-4 border-neo-black"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.2 }}
      >
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex gap-4">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about the Constitution..."
              className="flex-1"
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              disabled={isLoading}
            />
            <Button 
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="px-6"
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default ConstitutionChatPage