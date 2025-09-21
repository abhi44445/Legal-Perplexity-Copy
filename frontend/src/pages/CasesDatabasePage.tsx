import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Scale, TrendingUp, FileText, AlertTriangle, CheckCircle, Clock, Users, Gavel } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

interface CaseOutcomePrediction {
  overall_probability: number
  favorable_outcome: number
  unfavorable_outcome: number
  neutral_outcome: number
  confidence_level: 'high' | 'medium' | 'low'
  key_factors: string[]
  similar_cases: SimilarCase[]
  recommendations: string[]
  estimated_duration: string
}

interface SimilarCase {
  id: string
  title: string
  court: string
  year: number
  outcome: 'favorable' | 'unfavorable' | 'neutral'
  similarity_score: number
  key_precedents: string[]
}

const mockSimilarCases: SimilarCase[] = [
  {
    id: '1',
    title: 'ABC Corp vs. State of Delhi',
    court: 'Delhi High Court',
    year: 2022,
    outcome: 'favorable',
    similarity_score: 85,
    key_precedents: ['Article 14', 'Natural Justice']
  },
  {
    id: '2', 
    title: 'XYZ Ltd vs. Municipal Corporation',
    court: 'Supreme Court',
    year: 2021,
    outcome: 'unfavorable',
    similarity_score: 78,
    key_precedents: ['Administrative Law', 'Due Process']
  },
  {
    id: '3',
    title: 'Citizens Forum vs. Government',
    court: 'Bombay High Court', 
    year: 2023,
    outcome: 'neutral',
    similarity_score: 72,
    key_precedents: ['Public Interest', 'Fundamental Rights']
  }
]

const caseTypes = [
  'Constitutional Law',
  'Administrative Law', 
  'Civil Rights',
  'Commercial Dispute',
  'Criminal Law',
  'Family Law',
  'Property Law',
  'Tax Law',
  'Labor Law',
  'Environmental Law'
]

const CasesDatabasePage: React.FC = () => {
  const navigate = useNavigate()
  const [caseTitle, setCaseTitle] = useState('')
  const [caseType, setCaseType] = useState('')
  const [caseDescription, setCaseDescription] = useState('')
  const [prediction, setPrediction] = useState<CaseOutcomePrediction | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const analyzeCaseOutcome = async () => {
    if (!caseTitle.trim() || !caseDescription.trim()) return

    setIsAnalyzing(true)
    
    // Simulate AI analysis delay
    await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 1000))

    // Mock prediction based on input content
    const mockPrediction: CaseOutcomePrediction = {
      overall_probability: Math.round(60 + Math.random() * 30),
      favorable_outcome: Math.round(50 + Math.random() * 40),
      unfavorable_outcome: Math.round(20 + Math.random() * 30),
      neutral_outcome: Math.round(10 + Math.random() * 20),
      confidence_level: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low',
      key_factors: [
        'Strong precedent in similar constitutional matters',
        'Clear violation of fundamental rights established',
        'Government response time and administrative factors',
        'Court jurisdiction and case complexity',
        'Quality of legal representation and evidence'
      ],
      similar_cases: mockSimilarCases,
      recommendations: [
        'Strengthen constitutional arguments with recent precedents',
        'Focus on fundamental rights violations in pleadings',
        'Prepare comprehensive evidence documentation',
        'Consider alternative dispute resolution mechanisms',
        'Ensure proper procedural compliance throughout'
      ],
      estimated_duration: Math.random() > 0.5 ? '12-18 months' : '6-12 months'
    }

    setPrediction(mockPrediction)
    setIsAnalyzing(false)
  }

  const getOutcomeColor = (outcome: string) => {
    switch (outcome) {
      case 'favorable': return 'text-green-600 bg-green-100'
      case 'unfavorable': return 'text-red-600 bg-red-100'  
      case 'neutral': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'high': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
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
                  <Scale className="h-6 w-6 text-neo-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-neo-black font-inter">Case Outcome Prediction</h1>
                  <p className="text-neo-gray-500 font-inter">AI-powered legal case analysis and outcome prediction</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Case Input Form */}
          <motion.div 
            className="lg:col-span-1"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Case Details
                </CardTitle>
                <CardDescription>
                  Enter your case information for AI-powered outcome analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Case Title */}
                <div>
                  <label className="text-sm font-medium text-neo-black block mb-2">Case Title</label>
                  <Input
                    placeholder="e.g., Citizen vs. Municipal Corporation"
                    value={caseTitle}
                    onChange={(e) => setCaseTitle(e.target.value)}
                  />
                </div>

                {/* Case Type */}
                <div>
                  <label className="text-sm font-medium text-neo-black block mb-2">Case Type</label>
                  <select 
                    className="w-full px-3 py-2 border-3 border-neo-black bg-neo-white text-neo-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neo-black"
                    value={caseType}
                    onChange={(e) => setCaseType(e.target.value)}
                  >
                    <option value="">Select case type...</option>
                    {caseTypes.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>

                {/* Case Description */}
                <div>
                  <label className="text-sm font-medium text-neo-black block mb-2">Case Description</label>
                  <textarea
                    placeholder="Describe the key facts, legal issues, and circumstances of your case..."
                    className="w-full px-3 py-2 border-3 border-neo-black bg-neo-white text-neo-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neo-black resize-none"
                    rows={6}
                    value={caseDescription}
                    onChange={(e) => setCaseDescription(e.target.value)}
                  />
                </div>

                {/* Analyze Button */}
                <Button 
                  onClick={analyzeCaseOutcome}
                  disabled={!caseTitle.trim() || !caseDescription.trim() || isAnalyzing}
                  className="w-full"
                >
                  {isAnalyzing ? (
                    <>
                      <Clock className="h-4 w-4 mr-2 animate-spin" />
                      Analyzing Case...
                    </>
                  ) : (
                    <>
                      <TrendingUp className="h-4 w-4 mr-2" />
                      Predict Outcome
                    </>
                  )}
                </Button>

                {/* Disclaimer */}
                <div className="p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded-r">
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-sm font-medium text-yellow-800">Disclaimer</p>
                      <p className="text-xs text-yellow-700 mt-1">
                        This is an AI prediction tool for informational purposes only. 
                        Consult qualified legal professionals for actual legal advice.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Prediction Results */}
          <motion.div 
            className="lg:col-span-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            {!prediction && !isAnalyzing && (
              <Card className="text-center py-16">
                <CardContent>
                  <Scale className="h-16 w-16 text-neo-gray-400 mx-auto mb-6" />
                  <h3 className="text-2xl font-bold text-neo-black mb-4">Legal Case Analysis</h3>
                  <p className="text-lg text-neo-gray-500 mb-6 max-w-2xl mx-auto">
                    Enter your case details to get AI-powered predictions on likely outcomes, 
                    similar cases, and strategic recommendations.
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                    <div className="text-center">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                        <TrendingUp className="h-6 w-6 text-blue-600" />
                      </div>
                      <h4 className="font-semibold text-neo-black">Outcome Prediction</h4>
                      <p className="text-sm text-neo-gray-500">Statistical analysis</p>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                        <FileText className="h-6 w-6 text-green-600" />
                      </div>
                      <h4 className="font-semibold text-neo-black">Similar Cases</h4>
                      <p className="text-sm text-neo-gray-500">Precedent analysis</p>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                        <Gavel className="h-6 w-6 text-purple-600" />
                      </div>
                      <h4 className="font-semibold text-neo-black">Recommendations</h4>
                      <p className="text-sm text-neo-gray-500">Strategic advice</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {isAnalyzing && (
              <Card className="text-center py-16">
                <CardContent>
                  <div className="flex items-center justify-center mb-6">
                    <div className="animate-spin rounded-full h-16 w-16 border-4 border-neo-black border-t-transparent"></div>
                  </div>
                  <h3 className="text-2xl font-bold text-neo-black mb-4">Analyzing Your Case</h3>
                  <p className="text-lg text-neo-gray-500 mb-4">
                    Our AI is analyzing legal precedents, case patterns, and outcome probabilities...
                  </p>
                  <div className="flex items-center justify-center gap-2">
                    <div className="w-2 h-2 bg-neo-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-neo-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-neo-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </CardContent>
              </Card>
            )}

            {prediction && (
              <div className="space-y-6">
                {/* Outcome Probabilities */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-blue-600" />
                      Outcome Prediction
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                      <div className="text-center p-4 bg-green-50 rounded border-2 border-green-200">
                        <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-green-600">{prediction.favorable_outcome}%</div>
                        <div className="text-sm text-green-700">Favorable</div>
                      </div>
                      <div className="text-center p-4 bg-red-50 rounded border-2 border-red-200">
                        <AlertTriangle className="h-8 w-8 text-red-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-red-600">{prediction.unfavorable_outcome}%</div>
                        <div className="text-sm text-red-700">Unfavorable</div>
                      </div>
                      <div className="text-center p-4 bg-yellow-50 rounded border-2 border-yellow-200">
                        <Clock className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-yellow-600">{prediction.neutral_outcome}%</div>
                        <div className="text-sm text-yellow-700">Neutral</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between p-4 bg-neo-gray-100 rounded">
                      <div>
                        <div className="font-semibold text-neo-black">Overall Success Probability</div>
                        <div className="text-sm text-neo-gray-600">Based on historical case data</div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-neo-black">{prediction.overall_probability}%</div>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getConfidenceColor(prediction.confidence_level)}`}>
                          {prediction.confidence_level.toUpperCase()} CONFIDENCE
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Key Factors */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="h-5 w-5 text-purple-600" />
                      Key Factors Affecting Outcome
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {prediction.key_factors.map((factor, index) => (
                        <li key={index} className="flex items-start gap-3">
                          <div className="w-2 h-2 bg-purple-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-sm text-neo-black">{factor}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                {/* Similar Cases */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-green-600" />
                      Similar Cases & Precedents
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {prediction.similar_cases.map((similarCase) => (
                        <div key={similarCase.id} className="p-4 border-2 border-neo-gray-200 rounded">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h4 className="font-semibold text-neo-black">{similarCase.title}</h4>
                              <p className="text-sm text-neo-gray-600">{similarCase.court} • {similarCase.year}</p>
                            </div>
                            <div className="text-right">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${getOutcomeColor(similarCase.outcome)}`}>
                                {similarCase.outcome.toUpperCase()}
                              </span>
                              <div className="text-sm text-neo-gray-600 mt-1">{similarCase.similarity_score}% similar</div>
                            </div>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {similarCase.key_precedents.map((precedent, idx) => (
                              <span key={idx} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                                {precedent}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Recommendations */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Gavel className="h-5 w-5 text-orange-600" />
                      Strategic Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {prediction.recommendations.map((recommendation, index) => (
                        <li key={index} className="flex items-start gap-3">
                          <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-neo-black">{recommendation}</span>
                        </li>
                      ))}
                    </ul>
                    
                    <div className="mt-6 p-4 bg-blue-50 border-l-4 border-blue-400 rounded-r">
                      <div className="flex items-center gap-2 mb-2">
                        <Clock className="h-5 w-5 text-blue-600" />
                        <span className="font-semibold text-blue-800">Estimated Duration</span>
                      </div>
                      <p className="text-blue-700">{prediction.estimated_duration}</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default CasesDatabasePage