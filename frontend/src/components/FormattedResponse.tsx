import React from 'react'
import { CheckCircle, BookOpen, Scale, Users, Shield } from 'lucide-react'

interface FormattedResponseProps {
  content: string
  className?: string
}

const FormattedResponse: React.FC<FormattedResponseProps> = ({ content, className = '' }) => {
  // Function to parse and structure the content
  const parseContent = (text: string) => {
    // Split into sections based on numbered points and headings
    const sections = text.split(/(\d+\.\s*\*\*[^*]+\*\*:?)/).filter(Boolean)
    
    const parsed = []
    let currentSection = ''
    
    for (let i = 0; i < sections.length; i++) {
      if (sections[i].match(/^\d+\.\s*\*\*[^*]+\*\*:?/)) {
        // This is a numbered heading
        if (currentSection) {
          parsed.push({ type: 'content', text: currentSection })
        }
        parsed.push({ type: 'heading', text: sections[i] })
        currentSection = ''
      } else {
        currentSection += sections[i]
      }
    }
    
    if (currentSection) {
      parsed.push({ type: 'content', text: currentSection })
    }
    
    return parsed
  }

  // Function to format individual content blocks
  const formatContent = (text: string) => {
    // Handle bullet points
    const lines = text.split('\n').map(line => line.trim()).filter(Boolean)
    
    return lines.map((line, index) => {
      // Check for various patterns
      if (line.startsWith('* **Art.') || line.startsWith('* **Article')) {
        // Article references
        return (
          <div key={index} className="ml-4 mb-2 flex items-start gap-2">
            <Scale className="h-4 w-4 text-blue-600 mt-1 flex-shrink-0" />
            <span className="text-sm" dangerouslySetInnerHTML={{ __html: formatMarkdown(line.substring(2)) }} />
          </div>
        )
      } else if (line.startsWith('* **')) {
        // Bold bullet points
        return (
          <div key={index} className="ml-4 mb-2 flex items-start gap-2">
            <div className="w-2 h-2 bg-neo-black rounded-full mt-2 flex-shrink-0" />
            <span className="text-sm" dangerouslySetInnerHTML={{ __html: formatMarkdown(line.substring(2)) }} />
          </div>
        )
      } else if (line.startsWith('*')) {
        // Regular bullet points
        return (
          <div key={index} className="ml-6 mb-1 flex items-start gap-2">
            <div className="w-1 h-1 bg-neo-gray-400 rounded-full mt-2 flex-shrink-0" />
            <span className="text-sm text-neo-gray-700" dangerouslySetInnerHTML={{ __html: formatMarkdown(line.substring(1)) }} />
          </div>
        )
      } else if (line.includes('**Conclusion:**') || line.includes('**Key Distinction:**')) {
        // Conclusion sections
        return (
          <div key={index} className="mt-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r">
            <div className="flex items-start gap-2">
              <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <span className="font-medium" dangerouslySetInnerHTML={{ __html: formatMarkdown(line) }} />
            </div>
          </div>
        )
      } else {
        // Regular paragraphs
        return (
          <p key={index} className="mb-3 text-sm leading-relaxed" dangerouslySetInnerHTML={{ __html: formatMarkdown(line) }} />
        )
      }
    })
  }

  // Function to format markdown-like syntax
  const formatMarkdown = (text: string) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-neo-black">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
      .replace(/(Article \d+[A-Z]?)/g, '<span class="bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded text-xs font-medium">$1</span>')
      .replace(/(Part [IVX]+)/g, '<span class="bg-green-100 text-green-800 px-1.5 py-0.5 rounded text-xs font-medium">$1</span>')
      .replace(/(Section \d+)/g, '<span class="bg-purple-100 text-purple-800 px-1.5 py-0.5 rounded text-xs font-medium">$1</span>')
  }

  // Function to get icon for section type
  const getSectionIcon = (heading: string) => {
    if (heading.includes('Rights') || heading.includes('Freedom')) {
      return <Shield className="h-5 w-5 text-blue-600" />
    } else if (heading.includes('Equality')) {
      return <Scale className="h-5 w-5 text-green-600" />
    } else if (heading.includes('Cultural') || heading.includes('Educational')) {
      return <Users className="h-5 w-5 text-purple-600" />
    } else {
      return <BookOpen className="h-5 w-5 text-orange-600" />
    }
  }

  const parsedContent = parseContent(content)

  return (
    <div className={`prose prose-sm max-w-none ${className}`}>
      {parsedContent.map((section, index) => {
        if (section.type === 'heading') {
          const cleanHeading = section.text.replace(/^\d+\.\s*/, '').replace(/\*\*/g, '')
          return (
            <div key={index} className="mb-4">
              <div className="flex items-center gap-3 mb-3 p-3 bg-neo-gray-100 border-l-4 border-neo-black rounded-r">
                {getSectionIcon(cleanHeading)}
                <h3 className="font-bold text-lg text-neo-black m-0" dangerouslySetInnerHTML={{ __html: formatMarkdown(cleanHeading) }} />
              </div>
            </div>
          )
        } else {
          return (
            <div key={index} className="mb-4">
              {formatContent(section.text)}
            </div>
          )
        }
      })}
    </div>
  )
}

export default FormattedResponse