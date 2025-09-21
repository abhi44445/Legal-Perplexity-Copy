import React from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { MessageSquare, Shield, Scale, Search } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  
  const menuCards = [
    {
      id: 'constitution',
      title: 'Constitution Chat',
      description: 'Ask questions about the Indian Constitution and get AI-powered legal insights with citations.',
      icon: MessageSquare,
      route: '/constitution',
      color: 'bg-blue-50',
      stats: '25,000+ queries answered'
    },
    {
      id: 'rights',
      title: 'Know Your Rights',
      description: 'Get constitutional guidance for real-world situations like bribery, threats, or harassment.',
      icon: Shield,
      route: '/know-your-rights',
      color: 'bg-green-50',
      stats: '8+ scenario types'
    },
    {
      id: 'cases',
      title: 'Case Outcome Prediction',
      description: 'Get AI-powered predictions for legal case outcomes based on historical data.',
      icon: Scale,
      route: '/cases',
      color: 'bg-purple-50',
      stats: '85% accuracy rate'
    },
    {
      id: 'research',
      title: 'Legal Research',
      description: 'Search through legal documents, precedents, and constitutional provisions.',
      icon: Search,
      route: '/research',
      color: 'bg-orange-50',
      stats: '10,000+ documents'
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: [0.4, 0.0, 0.2, 1] as const
      }
    }
  }

  return (
    <div className="min-h-screen bg-neo-white">
      {/* Hero Section */}
      <motion.div 
        className="relative overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <motion.h1 
              className="text-6xl md:text-8xl font-black text-neo-black mb-6 font-inter tracking-tight"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              Legal Perplexity
            </motion.h1>
            <motion.p 
              className="text-xl md:text-2xl text-neo-gray-500 mb-12 max-w-3xl mx-auto font-inter"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              Your AI-powered constitutional legal assistant. Ask questions, understand your rights, and get expert legal insights.
            </motion.p>
            
            {/* Search Bar */}
            <motion.div 
              className="max-w-2xl mx-auto mb-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <div className="flex gap-4">
                <Input 
                  placeholder="Ask a constitutional question..."
                  className="flex-1 h-14 text-lg"
                />
                <Button size="lg" className="h-14 px-8 text-lg">
                  Ask
                </Button>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Main Navigation Cards */}
      <motion.div 
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div 
          className="text-center mb-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <h2 className="text-4xl font-bold text-neo-black mb-4 font-inter">
            Choose Your Legal Journey
          </h2>
          <p className="text-lg text-neo-gray-500 font-inter">
            Select a category to explore constitutional law and your rights
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {menuCards.map((card) => {
            const IconComponent = card.icon
            return (
              <motion.div
                key={card.id}
                variants={cardVariants}
                whileHover={{ 
                  scale: 1.02,
                  transition: { duration: 0.2 }
                }}
                whileTap={{ scale: 0.98 }}
              >
                <Card className="h-full cursor-pointer group" onClick={() => navigate(card.route)}>
                  <CardHeader className="pb-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-4">
                        <div className="p-3 bg-neo-black rounded-none">
                          <IconComponent className="h-8 w-8 text-neo-white" />
                        </div>
                        <div>
                          <CardTitle className="text-2xl mb-2 group-hover:text-neo-gray-700 transition-colors">
                            {card.title}
                          </CardTitle>
                          <div className="text-sm font-bold text-neo-gray-500 bg-neo-gray-100 px-3 py-1 inline-block">
                            {card.stats}
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <CardDescription className="text-lg leading-relaxed mb-6">
                      {card.description}
                    </CardDescription>
                    <Button 
                      variant="outline" 
                      className="w-full group-hover:bg-neo-black group-hover:text-neo-white transition-all duration-200"
                      onClick={(e) => {
                        e.stopPropagation()
                        navigate(card.route)
                      }}
                    >
                      Get Started
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* Stats Section */}
      <motion.div 
        className="bg-neo-black text-neo-white py-20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 1.2 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-5xl font-black mb-4 font-inter">50k+</div>
              <div className="text-xl font-medium font-inter">Questions Answered</div>
            </div>
            <div>
              <div className="text-5xl font-black mb-4 font-inter">99.8%</div>
              <div className="text-xl font-medium font-inter">Citation Accuracy</div>
            </div>
            <div>
              <div className="text-5xl font-black mb-4 font-inter">24/7</div>
              <div className="text-xl font-medium font-inter">AI Assistant</div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default HomePage