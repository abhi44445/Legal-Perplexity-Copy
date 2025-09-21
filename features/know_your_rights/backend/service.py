"""
Know Your Rights Service Layer
==============================

Core business logic for Know Your Rights feature.
Handles input validation, RAG integration, and response processing.
"""

import re
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

# Import existing RAG components
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from constitution_chat.core.constitution_rag import ConstitutionRAG
from constitution_chat.core.constitution_db import ConstitutionDatabase

logger = logging.getLogger(__name__)

@dataclass
class RightsQueryResult:
    """Result of a Know Your Rights query."""
    legal_advice: str
    citations: List[Dict[str, str]]
    recommended_actions: List[str]
    urgency: str
    follow_up_questions: List[str]
    disclaimer: str
    source_docs: List[Dict[str, Any]]
    confidence_score: float

class KnowYourRightsService:
    """
    Service class for Know Your Rights functionality.
    Reuses existing RAG pipeline with specialized prompts and processing.
    """
    
    def __init__(self, rag_instance: Optional[ConstitutionRAG] = None):
        """Initialize the service with existing RAG components."""
        self.rag = rag_instance or ConstitutionRAG()
        self.disclaimer = "This is informational only and not legal advice. Consult a qualified lawyer for legal advice."
        
        # Scenario-specific prompt templates
        self.scenario_prompts = {
            "bribe": self._create_bribe_prompt(),
            "threat": self._create_threat_prompt(), 
            "harassment": self._create_harassment_prompt(),
            "online_harassment": self._create_online_harassment_prompt(),
            "workplace": self._create_workplace_prompt(),
            "other": self._create_general_prompt()
        }
        
    def process_query(self, scenario: str, user_text: str, user_id: Optional[str] = None) -> RightsQueryResult:
        """
        Process a Know Your Rights query using existing RAG system.
        
        Args:
            scenario: Type of rights violation
            user_text: User's description of the situation
            user_id: Optional user identifier
            
        Returns:
            RightsQueryResult with comprehensive guidance
        """
        try:
            # Input validation and sanitization
            sanitized_text = self._sanitize_input(user_text)
            
            # Build specialized query using scenario context
            enhanced_query = self._build_enhanced_query(scenario, sanitized_text)
            
            # Use existing retrieval function
            context_docs = self.rag.retrieve_relevant_context(enhanced_query)
            
            # Check retrieval confidence
            if not context_docs:
                return self._generate_low_confidence_response(scenario, sanitized_text)
            
            # Generate response using existing model
            rag_result = self.rag.ask_constitutional_question(enhanced_query, user_type="general_public")
            
            if rag_result['status'] != 'success':
                logger.error(f"RAG generation failed: {rag_result.get('error', 'Unknown error')}")
                return self._generate_fallback_response(scenario, sanitized_text)
            
            # Process response into Know Your Rights format
            result = self._process_rag_response(
                rag_result, 
                context_docs, 
                scenario, 
                sanitized_text
            )
            
            # Log successful processing (with PII redaction)
            logger.info(f"Successfully processed {scenario} query - confidence: {result.confidence_score:.2f}")
            logger.debug(f"Generated {len(result.citations)} citations, urgency: {result.urgency}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing Know Your Rights query: {str(e)}")
            return self._generate_error_response(scenario, str(e))
    
    def _sanitize_input(self, text: str) -> str:
        """Sanitize and validate user input."""
        # Basic length validation
        if len(text.strip()) < 10:
            raise ValueError("Description too short - please provide more details")
        
        if len(text) > 2000:
            text = text[:2000] + "..."
            logger.warning("Input text truncated to 2000 characters")
        
        # Block potential system commands or injections
        dangerous_patterns = [
            r'<script.*?</script>',
            r'javascript:',
            r'exec\(',
            r'eval\(',
            r'system\(',
            r'rm\s+-rf',
            r'DELETE\s+FROM'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning("Potentially dangerous input detected and sanitized")
                text = re.sub(pattern, '[CONTENT_REMOVED]', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _build_enhanced_query(self, scenario: str, user_text: str) -> str:
        """Build enhanced query using scenario-specific prompt template."""
        prompt_template = self.scenario_prompts.get(scenario, self.scenario_prompts["other"])
        
        return prompt_template.format(
            user_situation=user_text,
            scenario=scenario
        )
    
    def _process_rag_response(self, rag_result: Dict, context_docs: List, scenario: str, user_text: str) -> RightsQueryResult:
        """Process RAG result into Know Your Rights format."""
        
        answer = rag_result.get('answer', '')
        reasoning = rag_result.get('reasoning', '')
        
        # Extract structured information
        citations = self._extract_citations(answer, context_docs)
        urgency = self._determine_urgency(scenario, user_text, answer)
        recommended_actions = self._generate_recommended_actions(scenario, urgency, answer)
        follow_up_questions = self._generate_follow_up_questions(scenario, user_text, answer)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(rag_result, context_docs, citations)
        
        # Process source documents
        source_docs = [
            {
                "id": f"constitutional_doc_{i}",
                "score": getattr(doc, 'score', 0.9 - (i * 0.1)),
                "snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": getattr(doc, 'metadata', {})
            }
            for i, doc in enumerate(context_docs[:5])
        ]
        
        return RightsQueryResult(
            legal_advice=answer,
            citations=citations,
            recommended_actions=recommended_actions,
            urgency=urgency,
            follow_up_questions=follow_up_questions,
            disclaimer=self.disclaimer,
            source_docs=source_docs,
            confidence_score=confidence_score
        )
    
    def _extract_citations(self, answer: str, context_docs: List) -> List[Dict[str, str]]:
        """Extract constitutional and legal citations from response."""
        citations = []
        
        # Constitutional articles
        article_pattern = r'Article\s+(\d+(?:[A-Z]?)?(?:\([^)]+\))?)'
        articles = re.findall(article_pattern, answer, re.IGNORECASE)
        for article in set(articles):  # Remove duplicates
            citations.append({
                "type": "constitution",
                "reference": f"Article {article}",
                "link": None
            })
        
        # Statutory provisions
        statutory_patterns = [
            (r'Section\s+(\d+)\s*(?:of\s*)?(?:the\s*)?Indian\s*Penal\s*Code|IPC', "statute", "Section {} IPC"),
            (r'Section\s+(\d+)\s*(?:of\s*)?(?:the\s*)?(?:IT\s*Act|Information\s*Technology\s*Act)', "statute", "Section {} IT Act"),
            (r'Section\s+(\d+)\s*(?:of\s*)?(?:the\s*)?(?:Criminal\s*Procedure\s*Code|CrPC)', "statute", "Section {} CrPC")
        ]
        
        for pattern, citation_type, reference_format in statutory_patterns:
            matches = re.findall(pattern, answer, re.IGNORECASE)
            for match in set(matches):
                citations.append({
                    "type": citation_type,
                    "reference": reference_format.format(match),
                    "link": None
                })
        
        # Case law references (basic pattern)
        case_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+v\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        cases = re.findall(case_pattern, answer)
        for plaintiff, defendant in cases[:2]:  # Limit to 2 cases
            citations.append({
                "type": "case",
                "reference": f"{plaintiff} v. {defendant}",
                "link": None
            })
        
        # Ensure at least one constitutional citation
        if not any(c["type"] == "constitution" for c in citations):
            citations.insert(0, {
                "type": "constitution",
                "reference": "Fundamental Rights (Part III)",
                "link": None
            })
        
        return citations[:5]  # Limit to 5 most relevant
    
    def _determine_urgency(self, scenario: str, user_text: str, answer: str) -> str:
        """Determine urgency level using multiple factors."""
        
        text_combined = (user_text + " " + answer).lower()
        
        # Emergency indicators
        emergency_keywords = [
            "immediate danger", "life threat", "violence", "emergency", 
            "urgent medical", "call police immediately", "911", "100"
        ]
        
        # High priority indicators  
        high_keywords = [
            "threat", "intimidation", "harassment", "fear for safety", 
            "physical harm", "stalking", "blackmail", "extortion"
        ]
        
        # Medium priority indicators
        medium_keywords = [
            "bribe", "corruption", "ongoing harassment", "workplace discrimination",
            "repeated incidents", "pattern of behavior"
        ]
        
        if any(keyword in text_combined for keyword in emergency_keywords):
            return "emergency"
        elif scenario == "threat" or any(keyword in text_combined for keyword in high_keywords):
            return "high"
        elif any(keyword in text_combined for keyword in medium_keywords):
            return "medium"
        else:
            return "low"
    
    def _generate_recommended_actions(self, scenario: str, urgency: str, answer: str) -> List[str]:
        """Generate context-aware recommended actions."""
        
        actions = []
        
        # Universal actions
        actions.extend(["document_incident", "collect_evidence"])
        
        # Scenario-specific actions
        scenario_actions = {
            "bribe": ["contact_authorities", "call_police"],
            "threat": ["call_police", "legal_aid"],
            "harassment": ["legal_aid", "contact_authorities"],
            "online_harassment": ["block_report", "contact_authorities"],
            "workplace": ["legal_aid", "contact_authorities"],
            "other": ["legal_aid"]
        }
        
        actions.extend(scenario_actions.get(scenario, ["legal_aid"]))
        
        # Urgency-based modifications
        if urgency == "emergency":
            actions.insert(0, "call_police")
        elif urgency == "high" and "call_police" not in actions:
            actions.insert(1, "call_police")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_actions = []
        for action in actions:
            if action not in seen:
                unique_actions.append(action)
                seen.add(action)
        
        return unique_actions[:6]  # Limit to 6 actions
    
    def _generate_follow_up_questions(self, scenario: str, user_text: str, answer: str) -> List[str]:
        """Generate relevant follow-up questions based on context."""
        
        questions = []
        
        # Universal questions
        if "evidence" not in user_text.lower():
            questions.append("Do you have any evidence or documentation of this incident?")
        
        if "report" not in user_text.lower():
            questions.append("Have you reported this matter to any authorities?")
        
        # Scenario-specific questions
        scenario_questions = {
            "bribe": [
                "What amount was demanded and by whom?",
                "Was this demand made verbally or in writing?",
                "Are there any witnesses to this incident?"
            ],
            "threat": [
                "What specific threats were made against you?",
                "Do you feel you are in immediate physical danger?",
                "Have these threats been communicated in writing or digitally?"
            ],
            "harassment": [
                "How long has this harassment been ongoing?",
                "Have there been witnesses to these incidents?",
                "What steps have you already taken to address this?"
            ],
            "online_harassment": [
                "What platform or medium was used for the harassment?",
                "Have you saved screenshots or other digital evidence?",
                "Have you reported this to the platform administrators?"
            ],
            "workplace": [
                "Is there an HR department or internal grievance mechanism?",
                "Have you documented these workplace issues previously?",
                "Are other colleagues experiencing similar treatment?"
            ],
            "other": [
                "Can you provide more specific details about your situation?",
                "When did this incident or pattern begin?"
            ]
        }
        
        questions.extend(scenario_questions.get(scenario, scenario_questions["other"]))
        
        return questions[:4]  # Limit to 4 most relevant questions
    
    def _calculate_confidence(self, rag_result: Dict, context_docs: List, citations: List) -> float:
        """Calculate confidence score based on multiple factors."""
        
        confidence = 0.5  # Base confidence
        
        # Factor 1: Number of relevant documents retrieved
        if len(context_docs) >= 3:
            confidence += 0.2
        elif len(context_docs) >= 1:
            confidence += 0.1
        
        # Factor 2: Number of citations extracted
        if len(citations) >= 2:
            confidence += 0.15
        elif len(citations) >= 1:
            confidence += 0.1
        
        # Factor 3: Response length (indicator of comprehensiveness)
        answer_length = len(rag_result.get('answer', ''))
        if answer_length > 500:
            confidence += 0.1
        elif answer_length > 200:
            confidence += 0.05
        
        # Factor 4: Presence of reasoning
        if rag_result.get('reasoning'):
            confidence += 0.05
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _generate_low_confidence_response(self, scenario: str, user_text: str) -> RightsQueryResult:
        """Generate response when retrieval confidence is low."""
        
        cautious_advice = f"""I understand you're facing a {scenario}-related situation. While I don't have sufficient specific constitutional information to provide detailed guidance, I can offer some general direction:

For this type of situation, you should consider:
1. Consulting with a qualified lawyer who specializes in constitutional and criminal law
2. Contacting relevant authorities if you believe laws have been violated
3. Documenting all evidence and details of your situation
4. Seeking help from legal aid organizations if needed

Your fundamental rights under the Constitution of India include protection from discrimination, right to life and liberty, and access to justice. These rights provide the foundation for addressing various legal concerns."""
        
        return RightsQueryResult(
            legal_advice=cautious_advice,
            citations=[{"type": "constitution", "reference": "Fundamental Rights (Part III)", "link": None}],
            recommended_actions=["legal_aid", "document_incident", "contact_authorities"],
            urgency="medium",
            follow_up_questions=[
                "Can you provide more specific details about your situation?",
                "Have you consulted with any legal professionals?",
                "What immediate support do you need?"
            ],
            disclaimer=self.disclaimer,
            source_docs=[],
            confidence_score=0.3
        )
    
    def _generate_fallback_response(self, scenario: str, user_text: str) -> RightsQueryResult:
        """Generate fallback response when RAG generation fails."""
        
        fallback_advice = f"""I apologize, but I'm experiencing technical difficulties generating a comprehensive response to your {scenario}-related query. However, based on your situation, here are some immediate steps you should consider:

1. If you're in immediate danger, contact emergency services (100/112)
2. Document your situation with dates, times, and any evidence
3. Consult with a qualified lawyer for proper legal guidance
4. Consider contacting relevant authorities or legal aid organizations

Your constitutional rights protect you from various forms of harm and discrimination. Please seek professional legal assistance for guidance specific to your situation."""
        
        return RightsQueryResult(
            legal_advice=fallback_advice,
            citations=[{"type": "constitution", "reference": "Fundamental Rights (Part III)", "link": None}],
            recommended_actions=["legal_aid", "document_incident", "call_police" if scenario in ["threat", "harassment"] else "contact_authorities"],
            urgency="medium",
            follow_up_questions=[
                "Are you in immediate danger requiring emergency assistance?",
                "Have you been able to document this situation?",
                "Do you have access to legal representation?"
            ],
            disclaimer=self.disclaimer,
            source_docs=[],
            confidence_score=0.4
        )
    
    def _generate_error_response(self, scenario: str, error_msg: str) -> RightsQueryResult:
        """Generate response for error cases."""
        
        error_advice = f"""I apologize, but I encountered an error while processing your {scenario}-related query. For your safety and to ensure you receive proper guidance:

1. If this is an emergency requiring immediate assistance, please contact emergency services (100/112)
2. For legal guidance, please consult with a qualified lawyer
3. Consider contacting legal aid organizations or relevant authorities
4. Document your situation while details are fresh in your memory

Your constitutional rights remain protected regardless of technical issues. Please seek professional assistance for your situation."""
        
        logger.error(f"Error response generated for {scenario}: {error_msg}")
        
        return RightsQueryResult(
            legal_advice=error_advice,
            citations=[{"type": "constitution", "reference": "Fundamental Rights (Part III)", "link": None}],
            recommended_actions=["legal_aid", "document_incident"],
            urgency="medium",
            follow_up_questions=[
                "Do you need immediate emergency assistance?",
                "Can you retry your query with simpler language?"
            ],
            disclaimer=self.disclaimer,
            source_docs=[],
            confidence_score=0.2
        )
    
    # Prompt Templates
    
    def _create_bribe_prompt(self) -> str:
        return """
You are a constitutional law expert helping an Indian citizen understand their rights regarding corruption and bribery.

User's Situation: {user_situation}

Please provide comprehensive guidance that includes:

1. **Constitutional Rights**: Cite relevant fundamental rights (especially Article 21 - Right to Life and Personal Liberty) and how they apply to this situation.

2. **Legal Framework**: Reference applicable provisions from:
   - Prevention of Corruption Act
   - Indian Penal Code sections on corruption
   - Any relevant constitutional provisions

3. **Immediate Actions**: Advise on immediate steps the citizen should take, including evidence collection and reporting procedures.

4. **Remedies Available**: Explain constitutional and legal remedies available to the citizen.

Ensure your response includes specific constitutional articles, relevant case law if applicable, and practical guidance. Focus on empowering the citizen with knowledge of their rights while emphasizing the importance of following legal procedures.

Format your response to be clear, actionable, and include proper legal citations.
"""

    def _create_threat_prompt(self) -> str:
        return """
You are a constitutional law expert helping an Indian citizen understand their rights regarding threats and intimidation.

User's Situation: {user_situation}

Please provide comprehensive guidance that includes:

1. **Constitutional Protection**: Cite Article 21 (Right to Life and Personal Liberty) and how it protects against threats and intimidation.

2. **Criminal Law Provisions**: Reference relevant sections from:
   - Indian Penal Code (criminal intimidation, threat to cause harm)
   - Code of Criminal Procedure (police protection, anticipatory bail if needed)

3. **Immediate Safety**: Advise on immediate steps for personal safety and legal protection.

4. **Legal Remedies**: Explain available constitutional and legal remedies including police protection and court intervention.

Ensure your response addresses both immediate safety concerns and long-term legal protection. Include specific legal provisions and emphasize the citizen's right to safety and legal protection.

Format your response to be clear, urgent where appropriate, and include proper legal citations.
"""

    def _create_harassment_prompt(self) -> str:
        return """
You are a constitutional law expert helping an Indian citizen understand their rights regarding harassment.

User's Situation: {user_situation}

Please provide comprehensive guidance that includes:

1. **Constitutional Rights**: Cite Article 21 (Right to Life with Dignity) and Article 14 (Right to Equality) as they apply to harassment situations.

2. **Legal Protections**: Reference relevant provisions from:
   - Indian Penal Code (outraging modesty, criminal intimidation)
   - Sexual Harassment of Women at Workplace Act (if applicable)
   - Any other relevant protective legislation

3. **Documentation and Evidence**: Advise on proper documentation and evidence collection procedures.

4. **Available Remedies**: Explain both constitutional and statutory remedies available.

Ensure your response is sensitive to the nature of harassment while being legally comprehensive. Include specific constitutional articles and relevant case law.

Format your response to be supportive, clear, and include proper legal citations.
"""

    def _create_online_harassment_prompt(self) -> str:
        return """
You are a constitutional law expert helping an Indian citizen understand their rights regarding online/cyber harassment.

User's Situation: {user_situation}

Please provide comprehensive guidance that includes:

1. **Constitutional Rights**: Cite Article 21 (Right to Privacy and Dignity) and how it extends to digital spaces.

2. **Cyber Law Framework**: Reference relevant provisions from:
   - Information Technology Act sections on cyber crimes
   - Indian Penal Code provisions applicable to online harassment
   - Any relevant constitutional protections for digital rights

3. **Digital Evidence**: Advise on preserving digital evidence (screenshots, URLs, communications).

4. **Reporting Mechanisms**: Explain both platform-based reporting and legal reporting procedures.

Ensure your response addresses the unique aspects of online harassment while maintaining constitutional foundation. Include specific legal provisions and digital rights protections.

Format your response to be tech-aware, legally sound, and include proper citations.
"""

    def _create_workplace_prompt(self) -> str:
        return """
You are a constitutional law expert helping an Indian citizen understand their workplace rights.

User's Situation: {user_situation}

Please provide comprehensive guidance that includes:

1. **Constitutional Rights**: Cite Article 19(1)(g) (Right to Practice Profession) and Article 21 (Right to Livelihood with Dignity).

2. **Labor Law Framework**: Reference relevant provisions from:
   - Industrial Relations Code
   - Sexual Harassment of Women at Workplace Act
   - Contract Labour Act
   - Any applicable constitutional protections for workers

3. **Internal Mechanisms**: Advise on workplace grievance mechanisms and due process.

4. **External Remedies**: Explain constitutional and legal remedies beyond workplace procedures.

Ensure your response balances workplace-specific procedures with broader constitutional rights. Include specific legal provisions and emphasize dignity at work.

Format your response to be workplace-relevant, legally comprehensive, and include proper citations.
"""

    def _create_general_prompt(self) -> str:
        return """
You are a constitutional law expert helping an Indian citizen understand their fundamental rights.

User's Situation: {user_situation}

Please provide comprehensive guidance that includes:

1. **Constitutional Analysis**: Identify and cite relevant fundamental rights from Part III of the Constitution that apply to this situation.

2. **Legal Framework**: Reference applicable constitutional provisions, statutes, and legal protections.

3. **Practical Guidance**: Provide actionable steps the citizen can take to protect and exercise their rights.

4. **Available Remedies**: Explain constitutional and legal remedies available including access to courts under Article 32 (Right to Constitutional Remedies).

Ensure your response is grounded in constitutional law while being practical and accessible. Include specific constitutional articles and relevant legal precedents where applicable.

Format your response to be clear, comprehensive, and include proper legal citations.
"""

def sanitize_text(text: str) -> str:
    """Utility function to redact PII from text for logging."""
    # Phone numbers
    text = re.sub(r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_REDACTED]', text)
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
    # Names (basic pattern for Indian names)
    text = re.sub(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', '[NAME_REDACTED]', text)
    # Addresses (basic pattern)
    text = re.sub(r'\b\d+[A-Za-z\s,-]*(?:Road|Street|Avenue|Lane|Nagar|Colony)\b', '[ADDRESS_REDACTED]', text)
    
    return text