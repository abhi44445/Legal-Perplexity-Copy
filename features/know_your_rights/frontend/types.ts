/**
 * TypeScript interfaces for Know Your Rights feature
 */

export type ScenarioType = "bribe" | "threat" | "harassment" | "online_harassment" | "workplace" | "other"

export type UrgencyLevel = "low" | "medium" | "high" | "emergency"

export type ActionType = "collect_evidence" | "call_police" | "legal_aid" | "block_report" | "contact_authorities" | "document_incident"

export interface Citation {
  type: "constitution" | "statute" | "case" | "other"
  reference: string
  link?: string
}

export interface SourceDocument {
  id: string
  score: number
  snippet: string
  metadata?: Record<string, any>
}

export interface KnowYourRightsRequest {
  user_id?: string
  scenario: ScenarioType
  text: string
  language: string
}

export interface KnowYourRightsResponse {
  legal_advice: string
  citations: Citation[]
  recommended_actions: ActionType[]
  urgency: UrgencyLevel
  follow_up_questions: string[]
  disclaimer: string
  source_docs: SourceDocument[]
}

export interface ValidationRequest {
  output_id: string
  expected: Record<string, any>
  score: number
  notes: string
}

export interface ApiError {
  message: string
  status: number
  detail?: string
}

export interface UseKnowYourRightsState {
  isLoading: boolean
  error: ApiError | null
  response: KnowYourRightsResponse | null
}

// Scenario configuration
export interface ScenarioConfig {
  id: ScenarioType
  label: string
  description: string
  icon: string
  examples: string[]
  placeholder: string
}

export const SCENARIO_CONFIGS: ScenarioConfig[] = [
  {
    id: "bribe",
    label: "Bribery & Corruption",
    description: "Officials demanding money or favors",
    icon: "💰",
    examples: [
      "Police asking for money to avoid ticket",
      "Government office demanding bribe for service"
    ],
    placeholder: "Describe the bribery situation you experienced..."
  },
  {
    id: "threat",
    label: "Threats & Intimidation",
    description: "Someone threatening you or your family",
    icon: "⚠️",
    examples: [
      "Neighbor threatening physical harm",
      "Landlord threatening illegal eviction"
    ],
    placeholder: "Describe the threats made against you..."
  },
  {
    id: "harassment",
    label: "Harassment",
    description: "Persistent unwanted behavior",
    icon: "🚫",
    examples: [
      "Workplace harassment by supervisor",
      "Harassment by neighbors or others"
    ],
    placeholder: "Describe the harassment you're experiencing..."
  },
  {
    id: "online_harassment",
    label: "Online Harassment",
    description: "Digital harassment, cyberbullying, or privacy violations",
    icon: "📱",
    examples: [
      "Social media harassment or doxxing",
      "Inappropriate sharing of personal information"
    ],
    placeholder: "Describe the online harassment or cyber incident..."
  },
  {
    id: "workplace",
    label: "Workplace Issues",
    description: "Employment-related problems and discrimination",
    icon: "💼",
    examples: [
      "Discrimination based on caste/religion",
      "Unfair termination or workplace conditions"
    ],
    placeholder: "Describe your workplace situation..."
  },
  {
    id: "other",
    label: "Other Rights Issues",
    description: "General constitutional rights concerns",
    icon: "⚖️",
    examples: [
      "Discrimination in public services",
      "Violation of fundamental rights"
    ],
    placeholder: "Describe your rights-related concern..."
  }
]

// Action configurations for UI display
export interface ActionConfig {
  id: ActionType
  label: string
  description: string
  icon: string
  type: "primary" | "secondary" | "emergency"
}

export const ACTION_CONFIGS: ActionConfig[] = [
  {
    id: "call_police",
    label: "Call Police",
    description: "Contact law enforcement immediately",
    icon: "🚨",
    type: "emergency"
  },
  {
    id: "contact_authorities",
    label: "Contact Authorities",
    description: "Report to relevant government authorities",
    icon: "🏛️",
    type: "primary"
  },
  {
    id: "legal_aid",
    label: "Get Legal Aid",
    description: "Consult with a lawyer or legal aid organization",
    icon: "⚖️",
    type: "primary"
  },
  {
    id: "document_incident",
    label: "Document Everything",
    description: "Record all details, dates, and evidence",
    icon: "📝",
    type: "secondary"
  },
  {
    id: "collect_evidence",
    label: "Collect Evidence",
    description: "Gather photos, recordings, or witness statements",
    icon: "📸",
    type: "secondary"
  },
  {
    id: "block_report",
    label: "Block & Report",
    description: "Block the person and report to platform/authorities",
    icon: "🛡️",
    type: "secondary"
  }
]

// Urgency level configurations
export interface UrgencyConfig {
  level: UrgencyLevel
  label: string
  description: string
  color: string
  bgColor: string
  icon: string
}

export const URGENCY_CONFIGS: UrgencyConfig[] = [
  {
    level: "low",
    label: "Low Priority",
    description: "Take action when convenient",
    color: "text-green-700",
    bgColor: "bg-green-100",
    icon: "ℹ️"
  },
  {
    level: "medium",
    label: "Medium Priority", 
    description: "Address within a few days",
    color: "text-yellow-700",
    bgColor: "bg-yellow-100",
    icon: "⚠️"
  },
  {
    level: "high",
    label: "High Priority",
    description: "Take immediate action",
    color: "text-orange-700",
    bgColor: "bg-orange-100",
    icon: "🔥"
  },
  {
    level: "emergency",
    label: "Emergency",
    description: "Seek immediate help",
    color: "text-red-700",
    bgColor: "bg-red-100",
    icon: "🚨"
  }
]