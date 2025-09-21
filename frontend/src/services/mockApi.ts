/**
 * Mock API service for frontend development when backend is unavailable
 * This provides realistic responses for testing UI components
 */

import type { ConstitutionChatRequest, ConstitutionChatResponse } from './api'

// Mock delay to simulate network latency
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

// Mock constitutional responses
const mockConstitutionResponses: Record<string, ConstitutionChatResponse> = {
  "article 21": {
    answer: "**Article 21 - Protection of Life and Personal Liberty**\n\nArticle 21 of the Indian Constitution states: \"No person shall be deprived of his life or personal liberty except according to procedure established by law.\"\n\n**Key Aspects:**\n\n1. **Scope of Life**: The Supreme Court has interpreted 'life' not merely as biological existence but as a meaningful life with dignity.\n\n2. **Personal Liberty**: This encompasses freedom of movement, profession, residence, and other fundamental aspects of human existence.\n\n3. **Procedure Established by Law**: Any deprivation must follow due process of law, ensuring fair and just procedures.\n\n**Landmark Cases:**\n* **Maneka Gandhi v. Union of India (1978)**: Expanded the scope of Article 21 to include the right to travel abroad.\n* **Francis Coralie Mullin v. Administrator, Union Territory of Delhi (1981)**: Established that life includes dignity and all aspects that make life meaningful.\n\n**Modern Interpretations:**\nThe right to life has been expanded to include:\n* Right to livelihood\n* Right to clean environment\n* Right to healthcare\n* Right to education\n* Right to shelter",
    reasoning: "This response synthesizes Article 21's text with judicial interpretations from landmark cases. The Supreme Court has consistently expanded Article 21's scope beyond mere survival to encompass dignified living. I've included specific case law that established key precedents and modern applications that courts have recognized under this fundamental right.",
    citations: [
      {
        type: "Constitutional Article",
        reference: "Article 21, Constitution of India",
        is_valid: true
      },
      {
        type: "Supreme Court Case",
        reference: "Maneka Gandhi v. Union of India (1978) 1 SCC 248",
        is_valid: true
      },
      {
        type: "Supreme Court Case", 
        reference: "Francis Coralie Mullin v. Administrator, UT of Delhi (1981) 1 SCC 608",
        is_valid: true
      }
    ],
    citation_validation: {
      citation_accuracy: 0.95,
      total_citations: 3,
      verified_citations: 3
    },
    response_time: 2.3,
    confidence_score: 0.92,
    user_type: "general_public"
  },
  "fundamental rights": {
    answer: "**Fundamental Rights in the Indian Constitution**\n\nFundamental Rights are basic human rights guaranteed to all citizens by the Constitution. They are enshrined in Part III (Articles 12-35) and are justiciable, meaning courts can enforce them.\n\n**The Six Categories:**\n\n1. **Right to Equality (Articles 14-18)**\n   * Equality before law and equal protection of laws\n   * Prohibition of discrimination\n   * Equality of opportunity in public employment\n   * Abolition of untouchability and titles\n\n2. **Right to Freedom (Articles 19-22)**\n   * Freedom of speech and expression\n   * Freedom of assembly, association, movement\n   * Freedom of profession, occupation, trade\n   * Protection against arbitrary arrest\n\n3. **Right against Exploitation (Articles 23-24)**\n   * Prohibition of human trafficking and forced labor\n   * Prohibition of child labor in hazardous work\n\n4. **Right to Freedom of Religion (Articles 25-28)**\n   * Freedom of conscience and religion\n   * Freedom to manage religious affairs\n   * Protection from religious instruction in state institutions\n\n5. **Cultural and Educational Rights (Articles 29-30)**\n   * Protection of language, script, and culture\n   * Right to establish and administer educational institutions\n\n6. **Right to Constitutional Remedies (Article 32)**\n   * Right to directly approach Supreme Court\n   * Power to issue writs (habeas corpus, mandamus, prohibition, certiorari, quo-warranto)",
    reasoning: "This comprehensive overview covers all six categories of fundamental rights with their constitutional basis. The structure follows the Constitution's organization in Part III, providing both the theoretical framework and practical applications. I've emphasized Article 32 as the 'heart and soul' of the Constitution as described by Dr. B.R. Ambedkar.",
    citations: [
      {
        type: "Constitutional Part",
        reference: "Part III, Articles 12-35, Constitution of India",
        is_valid: true
      },
      {
        type: "Constitutional Article",
        reference: "Article 32, Constitution of India",
        is_valid: true
      }
    ],
    citation_validation: {
      citation_accuracy: 0.98,
      total_citations: 2,
      verified_citations: 2
    },
    response_time: 1.8,
    confidence_score: 0.96,
    user_type: "general_public"
  },
  "directive principles": {
    answer: "**Directive Principles of State Policy (DPSP)**\n\nDirective Principles are guidelines for the state in governance and law-making, enshrined in Part IV (Articles 36-51) of the Constitution.\n\n**Key Characteristics:**\n* **Non-justiciable**: Cannot be enforced in courts\n* **Moral and political obligations**: Guide state policy\n* **Positive obligations**: Require state action\n* **Welfare state vision**: Promote social and economic democracy\n\n**Categories of DPSP:**\n\n1. **Economic and Social Principles (Articles 38-47)**\n   * Promote welfare and minimize inequalities\n   * Right to work, education, and public assistance\n   * Living wage and humane working conditions\n   * Prohibition of intoxicating drinks and drugs\n\n2. **Gandhian Principles (Articles 40, 43, 46, 47, 48)**\n   * Village panchayats and local self-government\n   * Cottage industries and rural development\n   * Protection of weaker sections\n   * Protection of animals and environment\n\n3. **Liberal-Intellectual Principles (Articles 44, 45, 48, 49, 50, 51)**\n   * Uniform Civil Code\n   * Free and compulsory education\n   * Protection of monuments and cultural heritage\n   * Separation of judiciary from executive\n   * International peace and cooperation\n\n**Relationship with Fundamental Rights:**\n* **Complementary**: DPSP and Fundamental Rights together ensure comprehensive development\n* **Balancing**: Courts balance both when they conflict\n* **Progressive implementation**: DPSP guide long-term policy goals",
    reasoning: "This analysis covers the comprehensive framework of DPSP, their classification, and relationship with fundamental rights. The tripartite classification (economic-social, Gandhian, liberal-intellectual) helps understand the diverse influences on the Constitution. I've emphasized their non-justiciable nature while highlighting their importance in policy-making.",
    citations: [
      {
        type: "Constitutional Part",
        reference: "Part IV, Articles 36-51, Constitution of India",
        is_valid: true
      },
      {
        type: "Constitutional Article",
        reference: "Article 38, Constitution of India",
        is_valid: true
      }
    ],
    citation_validation: {
      citation_accuracy: 0.94,
      total_citations: 2,
      verified_citations: 2
    },
    response_time: 2.1,
    confidence_score: 0.89,
    user_type: "general_public"
  }
}

export const mockApiService = {
  constitutionChat: {
    askQuestion: async (request: ConstitutionChatRequest): Promise<ConstitutionChatResponse> => {
      await delay(1500 + Math.random() * 1000) // Simulate 1.5-2.5s response time
      
      const query = request.query.toLowerCase()
      
      // Try to find a matching response
      for (const [key, response] of Object.entries(mockConstitutionResponses)) {
        if (query.includes(key)) {
          return {
            ...response,
            user_type: request.user_type || 'general_public'
          }
        }
      }
      
      // Default response for unmatched queries
      return {
        answer: `**Constitutional Analysis: "${request.query}"**\n\nThank you for your constitutional question. While I don't have a specific pre-written response for this query, I can help you understand constitutional principles.\n\n**General Guidance:**\n* All constitutional questions should be analyzed within the framework of fundamental rights, directive principles, and constitutional values\n* The Supreme Court is the final interpreter of constitutional provisions\n* Constitutional law evolves through judicial precedents and amendments\n\n**Suggestion:** Try asking about specific articles, fundamental rights, or landmark constitutional cases for more detailed responses.`,
        reasoning: "This is a general response for queries not covered by specific mock data. In a real system, the AI would analyze the query using constitutional databases and legal precedents.",
        citations: [
          {
            type: "Constitutional Framework",
            reference: "Constitution of India, 1950",
            is_valid: true
          }
        ],
        citation_validation: {
          citation_accuracy: 0.85,
          total_citations: 1,
          verified_citations: 1
        },
        response_time: 1.2,
        confidence_score: 0.75,
        user_type: request.user_type || 'general_public'
      }
    },

    getSuggestions: async (userType = 'general_public') => {
      await delay(300)
      
      const suggestions = {
        general_public: [
          { title: "Right to Education", query: "What are my rights to education under the Constitution?" },
          { title: "Freedom of Speech", query: "What does freedom of speech and expression mean for me?" },
          { title: "Right to Privacy", query: "Is privacy a fundamental right in India?" },
          { title: "Equal Protection", query: "How does Article 14 protect me from discrimination?" },
          { title: "Life and Liberty", query: "What is Article 21 about?" }
        ],
        lawyer: [
          { title: "Article 14 Interpretation", query: "Explain the scope and limitations of Article 14 equality before law" },
          { title: "Emergency Provisions", query: "Analyze the constitutional provisions for emergency and their judicial review" },
          { title: "Fundamental Rights vs DPSP", query: "Compare fundamental rights and directive principles in constitutional jurisprudence" },
          { title: "Amendment Procedure", query: "Explain Article 368 and the constitutional amendment process" },
          { title: "Federal Structure", query: "Analyze the federal structure of Indian Constitution" }
        ],
        law_student: [
          { title: "Basic Structure Doctrine", query: "What is the basic structure doctrine and its significance?" },
          { title: "Separation of Powers", query: "Explain separation of powers in the Indian Constitution" },
          { title: "Judicial Review", query: "What is judicial review and its scope in India?" },
          { title: "Fundamental Duties", query: "Explain fundamental duties under Article 51A" },
          { title: "Constitutional Remedies", query: "What are constitutional remedies under Article 32?" }
        ]
      }
      
      return {
        suggestions: suggestions[userType as keyof typeof suggestions] || suggestions.general_public,
        user_type: userType
      }
    },

    getHistory: async () => {
      await delay(200)
      return {
        history: [],
        total_queries: 0
      }
    }
  }
}