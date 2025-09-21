import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Shield, Search, Filter, BookOpen, Scale, Users, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

interface Right {
  id: string
  title: string
  category: string
  description: string
  articles: string[]
  keyPoints: string[]
  limitations: string[]
  importance: 'high' | 'medium' | 'low'
}

const mockRights: Right[] = [
  {
    id: '1',
    title: 'Right to Equality',
    category: 'Fundamental Rights',
    description: 'Ensures equal treatment before law and prohibits discrimination on grounds of religion, race, caste, sex, or place of birth.',
    articles: ['Article 14', 'Article 15', 'Article 16', 'Article 17', 'Article 18'],
    keyPoints: [
      'Equality before law and equal protection of laws',
      'Prohibition of discrimination on certain grounds',
      'Equality of opportunity in public employment',
      'Abolition of untouchability',
      'Abolition of titles except military and academic'
    ],
    limitations: [
      'Special provisions for women, children, and backward classes are allowed',
      'Reservation in employment and education is permitted',
      'Military and academic distinctions are exceptions'
    ],
    importance: 'high'
  },
  {
    id: '2',
    title: 'Right to Freedom',
    category: 'Fundamental Rights',
    description: 'Guarantees various freedoms including speech, expression, assembly, association, movement, and profession.',
    articles: ['Article 19', 'Article 20', 'Article 21', 'Article 22'],
    keyPoints: [
      'Freedom of speech and expression',
      'Freedom to assemble peacefully',
      'Freedom to form associations and unions',
      'Freedom of movement throughout India',
      'Freedom to practice any profession or trade',
      'Protection of life and personal liberty'
    ],
    limitations: [
      'Restrictions in interest of sovereignty, security, public order',
      'Reasonable restrictions on freedom of speech',
      'Emergency provisions can suspend certain freedoms'
    ],
    importance: 'high'
  },
  {
    id: '3',
    title: 'Right against Exploitation',
    category: 'Fundamental Rights',
    description: 'Prohibits human trafficking, forced labor, and employment of children in hazardous work.',
    articles: ['Article 23', 'Article 24'],
    keyPoints: [
      'Prohibition of traffic in human beings and forced labor',
      'Prohibition of employment of children below 14 years in factories',
      'Right against exploitation in any form',
      'Protection of children from hazardous work'
    ],
    limitations: [
      'State can impose compulsory service for public purposes',
      'Military service and national service are exceptions'
    ],
    importance: 'high'
  },
  {
    id: '4',
    title: 'Right to Freedom of Religion',
    category: 'Fundamental Rights',
    description: 'Guarantees freedom of conscience, religion, and the right to manage religious affairs.',
    articles: ['Article 25', 'Article 26', 'Article 27', 'Article 28'],
    keyPoints: [
      'Freedom of conscience and religion',
      'Freedom to manage religious affairs',
      'Freedom from payment of taxes for promotion of any religion',
      'Freedom from religious instruction in state educational institutions'
    ],
    limitations: [
      'Subject to public order, morality, and health',
      'State can regulate secular activities associated with religion',
      'Anti-conversion laws in some states'
    ],
    importance: 'medium'
  },
  {
    id: '5',
    title: 'Cultural and Educational Rights',
    category: 'Fundamental Rights',
    description: 'Protects the rights of minorities to conserve their culture and establish educational institutions.',
    articles: ['Article 29', 'Article 30'],
    keyPoints: [
      'Right to conserve distinct language, script, and culture',
      'Right to establish and administer educational institutions',
      'Protection against discrimination in state-aided institutions',
      'Minority rights protection'
    ],
    limitations: [
      'Subject to general law and regulations',
      'Must comply with conditions for state aid',
      'Cannot violate national integration'
    ],
    importance: 'medium'
  },
  {
    id: '6',
    title: 'Right to Constitutional Remedies',
    category: 'Fundamental Rights',
    description: 'Provides the right to directly approach the Supreme Court for enforcement of fundamental rights.',
    articles: ['Article 32'],
    keyPoints: [
      'Right to directly approach Supreme Court',
      'Power of courts to issue writs',
      'Habeas corpus, mandamus, prohibition, certiorari, quo-warranto',
      'Guaranteed enforcement of fundamental rights'
    ],
    limitations: [
      'Can be suspended during emergency',
      'Subject to parliamentary modification',
      'Courts may refuse writs in certain cases'
    ],
    importance: 'high'
  }
]

const categories = ['All', 'Fundamental Rights', 'Directive Principles', 'Constitutional Provisions']
const importanceFilters = ['All', 'High', 'Medium', 'Low']

const RightsExplorerPage: React.FC = () => {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [selectedImportance, setSelectedImportance] = useState('All')
  const [filteredRights, setFilteredRights] = useState<Right[]>(mockRights)
  const [selectedRight, setSelectedRight] = useState<Right | null>(null)

  // Filter rights based on search and filters
  useEffect(() => {
    let filtered = mockRights

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(right =>
        right.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        right.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        right.keyPoints.some(point => point.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    }

    // Apply category filter
    if (selectedCategory !== 'All') {
      filtered = filtered.filter(right => right.category === selectedCategory)
    }

    // Apply importance filter
    if (selectedImportance !== 'All') {
      filtered = filtered.filter(right => right.importance === selectedImportance.toLowerCase())
    }

    setFilteredRights(filtered)
  }, [searchQuery, selectedCategory, selectedImportance])

  const getImportanceColor = (importance: string) => {
    switch (importance) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Fundamental Rights': return <Shield className="h-5 w-5 text-blue-600" />
      case 'Directive Principles': return <BookOpen className="h-5 w-5 text-green-600" />
      case 'Constitutional Provisions': return <Scale className="h-5 w-5 text-purple-600" />
      default: return <Users className="h-5 w-5 text-gray-600" />
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
                  <Shield className="h-6 w-6 text-neo-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-neo-black font-inter">Rights Explorer</h1>
                  <p className="text-neo-gray-500 font-inter">Explore your constitutional rights and freedoms</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Filters Sidebar */}
          <motion.div 
            className="lg:col-span-1"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Filter className="h-5 w-5" />
                  Filters
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Search */}
                <div>
                  <label className="text-sm font-medium text-neo-black block mb-2">Search Rights</label>
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-neo-gray-500" />
                    <Input
                      placeholder="Search rights..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                {/* Category Filter */}
                <div>
                  <label className="text-sm font-medium text-neo-black block mb-2">Category</label>
                  <div className="space-y-2">
                    {categories.map((category) => (
                      <Button
                        key={category}
                        variant={selectedCategory === category ? "default" : "outline"}
                        className="w-full justify-start"
                        onClick={() => setSelectedCategory(category)}
                      >
                        {category}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Importance Filter */}
                <div>
                  <label className="text-sm font-medium text-neo-black block mb-2">Importance</label>
                  <div className="space-y-2">
                    {importanceFilters.map((importance) => (
                      <Button
                        key={importance}
                        variant={selectedImportance === importance ? "default" : "outline"}
                        className="w-full justify-start"
                        onClick={() => setSelectedImportance(importance)}
                      >
                        {importance}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Results Count */}
                <div className="pt-4 border-t">
                  <p className="text-sm text-neo-gray-500">
                    Showing {filteredRights.length} of {mockRights.length} rights
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Rights List */}
          <motion.div 
            className="lg:col-span-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <div className="space-y-6">
              {filteredRights.length === 0 ? (
                <Card className="text-center py-12">
                  <CardContent>
                    <AlertCircle className="h-12 w-12 text-neo-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-neo-black mb-2">No rights found</h3>
                    <p className="text-neo-gray-500">Try adjusting your search or filters</p>
                  </CardContent>
                </Card>
              ) : (
                filteredRights.map((right, index) => (
                  <motion.div
                    key={right.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                  >
                    <Card 
                      className="cursor-pointer hover:shadow-neo-hover transition-all duration-200"
                      onClick={() => setSelectedRight(selectedRight?.id === right.id ? null : right)}
                    >
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3">
                            {getCategoryIcon(right.category)}
                            <div>
                              <CardTitle className="text-xl mb-2">{right.title}</CardTitle>
                              <div className="flex items-center gap-2 mb-2">
                                <span className={`px-2 py-1 rounded text-xs font-medium ${getImportanceColor(right.importance)}`}>
                                  {right.importance.toUpperCase()}
                                </span>
                                <span className="text-sm text-neo-gray-500">{right.category}</span>
                              </div>
                              <CardDescription className="text-base">
                                {right.description}
                              </CardDescription>
                            </div>
                          </div>
                        </div>
                      </CardHeader>

                      {selectedRight?.id === right.id && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                        >
                          <CardContent className="pt-0">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                              <div>
                                <h4 className="font-semibold text-neo-black mb-3">Constitutional Articles</h4>
                                <div className="flex flex-wrap gap-2 mb-4">
                                  {right.articles.map((article) => (
                                    <span 
                                      key={article}
                                      className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm font-medium"
                                    >
                                      {article}
                                    </span>
                                  ))}
                                </div>

                                <h4 className="font-semibold text-neo-black mb-3">Key Points</h4>
                                <ul className="space-y-2">
                                  {right.keyPoints.map((point, idx) => (
                                    <li key={idx} className="flex items-start gap-2 text-sm">
                                      <div className="w-2 h-2 bg-neo-black rounded-full mt-2 flex-shrink-0" />
                                      {point}
                                    </li>
                                  ))}
                                </ul>
                              </div>

                              <div>
                                <h4 className="font-semibold text-neo-black mb-3">Limitations & Exceptions</h4>
                                <ul className="space-y-2">
                                  {right.limitations.map((limitation, idx) => (
                                    <li key={idx} className="flex items-start gap-2 text-sm">
                                      <AlertCircle className="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
                                      {limitation}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </CardContent>
                        </motion.div>
                      )}
                    </Card>
                  </motion.div>
                ))
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default RightsExplorerPage