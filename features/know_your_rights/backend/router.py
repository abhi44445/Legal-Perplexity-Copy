"""
Know Your Rights API Router
============================

Provides REST API endpoints for constitutional rights guidance.
Integrates with existing ConstitutionRAG system to provide scenario-based legal advice.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
import logging
import time
import re
import os

# Import existing RAG system
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from constitution_chat.core.constitution_rag import ConstitutionRAG

logger = logging.getLogger(__name__)

router = APIRouter()

# Global RAG instance (same pattern as constitution_chat.py)
_constitution_rag: Optional[ConstitutionRAG] = None
_rag_initialization_lock = False

def get_constitution_rag() -> ConstitutionRAG:
    """Get initialized Constitution RAG system (sync version for FastAPI)."""
    global _constitution_rag, _rag_initialization_lock
    
    if _constitution_rag is None and not _rag_initialization_lock:
        _rag_initialization_lock = True
        try:
            logger.info("Initializing Constitution RAG system for Know Your Rights...")
            _constitution_rag = ConstitutionRAG()
            logger.info("Constitution RAG system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG: {e}")
            _rag_initialization_lock = False
            raise
        finally:
            _rag_initialization_lock = False
    
    if _constitution_rag is None:
        raise HTTPException(status_code=503, detail="RAG system not available")
    
    return _constitution_rag

# Request/Response models
class KnowYourRightsRequest(BaseModel):
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    scenario: Literal["bribe", "threat", "harassment", "online_harassment", "workplace", "other"] = Field(
        ..., description="Type of rights violation scenario"
    )
    text: str = Field(..., min_length=10, max_length=2000, description="Detailed user description")
    language: str = Field("en", description="Response language")
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()

class Citation(BaseModel):
    type: Literal["constitution", "statute", "case", "other"]
    reference: str
    link: Optional[str] = None

class KnowYourRightsResponse(BaseModel):
    legal_advice: str
    citations: List[Citation]
    recommended_actions: List[Literal["collect_evidence", "call_police", "legal_aid", "block_report", "contact_authorities", "document_incident"]]
    urgency: Literal["low", "medium", "high", "emergency"]
    follow_up_questions: List[str]
    disclaimer: str
    source_docs: List[Dict[str, Any]]

class ValidationRequest(BaseModel):
    output_id: str
    expected: Dict[str, Any]
    score: float = Field(..., ge=0, le=1)
    notes: str

class HealthResponse(BaseModel):
    status: str
    message: str

# PII redaction utility
def sanitize_text(text: str) -> str:
    """Remove/redact PII from text for logging."""
    # Basic phone number pattern
    text = re.sub(r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_REDACTED]', text)
    # Basic email pattern  
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
    # Common Indian names (basic pattern)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME_REDACTED]', text)
    return text

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    try:
        # Test RAG system availability
        rag = get_constitution_rag()
        return HealthResponse(status="ok", message="Know Your Rights service is operational")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(status="error", message=f"Service unavailable: {str(e)}")

@router.post("/query", response_model=KnowYourRightsResponse)
def query_rights(request: KnowYourRightsRequest):
    """
    Process a Know Your Rights query and return constitutional guidance.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing Know Your Rights query - Scenario: {request.scenario}, Language: {request.language}")
        logger.info(f"Query text (sanitized): {sanitize_text(request.text)}")
        
        # Get RAG system
        rag = get_constitution_rag()
        
        # Build specialized prompt for Know Your Rights
        enhanced_query = _build_rights_query(request.scenario, request.text)
        
        # Get relevant constitutional context using existing retrieval
        context_docs = rag.retrieve_relevant_context(enhanced_query)
        
        # Generate response using existing model
        result = rag.ask_constitutional_question(enhanced_query, user_type="general_public")
        
        if result['status'] != 'success':
            raise HTTPException(status_code=500, detail="Failed to generate response")
        
        # Process response into Know Your Rights format
        response = _process_rights_response(
            result['answer'], 
            result.get('reasoning', ''),
            context_docs, 
            request.scenario,
            request.text
        )
        
        response_time = time.time() - start_time
        logger.info(f"Know Your Rights query processed in {response_time:.2f}s")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing Know Your Rights query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.post("/validate")
def validate_output(request: ValidationRequest):
    """
    Validate Know Your Rights output for evaluation and fine-tuning.
    """
    try:
        logger.info(f"Validating output: {request.output_id}")
        
        # Store validation result (in production, save to database)
        validation_result = {
            "output_id": request.output_id,
            "score": request.score,
            "expected": request.expected,
            "notes": request.notes,
            "timestamp": time.time()
        }
        
        # For now, just log the validation
        logger.info(f"Validation recorded: {validation_result}")
        
        return {"status": "success", "message": "Validation recorded"}
        
    except Exception as e:
        logger.error(f"Error validating output: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error validating output: {str(e)}"
        )

def _build_rights_query(scenario: str, user_text: str) -> str:
    """Build enhanced query for constitutional rights guidance."""
    
    scenario_context = {
        "bribe": "corruption, illegal demands for money, Article 21 (life and liberty), prevention of corruption",
        "threat": "intimidation, coercion, personal safety, Article 21 (right to life), criminal intimidation",
        "harassment": "harassment, dignity, Article 21 (right to life with dignity), personal liberty",
        "online_harassment": "cyber harassment, digital rights, privacy, Article 21 (privacy), IT Act provisions",
        "workplace": "workplace rights, labor law, dignity at work, Article 19 (profession), labor protections",
        "other": "fundamental rights, constitutional protections, legal remedies"
    }
    
    context = scenario_context.get(scenario, scenario_context["other"])
    
    enhanced_query = f"""
    Constitutional Rights Guidance Request:
    
    Scenario Type: {scenario}
    Situation: {user_text}
    
    Legal Context: {context}
    
    Please provide comprehensive constitutional guidance including:
    1. Relevant fundamental rights and constitutional articles
    2. Applicable statutory provisions  
    3. Recommended immediate actions
    4. Legal remedies available
    5. Emergency procedures if applicable
    """
    
    return enhanced_query

def _process_rights_response(answer: str, reasoning: str, context_docs: List, scenario: str, user_text: str) -> KnowYourRightsResponse:
    """Process RAG response into Know Your Rights format."""
    
    # Extract citations from answer
    citations = _extract_citations(answer, context_docs)
    
    # Determine urgency based on scenario and content
    urgency = _determine_urgency(scenario, user_text, answer)
    
    # Generate recommended actions
    recommended_actions = _generate_actions(scenario, urgency)
    
    # Generate follow-up questions
    follow_up_questions = _generate_follow_up_questions(scenario, user_text)
    
    # Process source documents
    source_docs = [
        {
            "id": f"doc_{i}",
            "score": 0.9 - (i * 0.1),  # Mock similarity scores
            "snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        }
        for i, doc in enumerate(context_docs[:3])
    ]
    
    # Always include disclaimer
    disclaimer = "This is informational only and not legal advice. Consult a qualified lawyer for legal advice."
    
    return KnowYourRightsResponse(
        legal_advice=answer,
        citations=citations,
        recommended_actions=recommended_actions,
        urgency=urgency,
        follow_up_questions=follow_up_questions,
        disclaimer=disclaimer,
        source_docs=source_docs
    )

def _extract_citations(answer: str, context_docs: List) -> List[Citation]:
    """Extract and format citations from the response."""
    citations = []
    
    # Look for Article references
    article_matches = re.findall(r'Article\s+(\d+(?:[A-Z]?)?)', answer, re.IGNORECASE)
    for match in article_matches:
        citations.append(Citation(
            type="constitution",
            reference=f"Article {match}",
            link=None
        ))
    
    # Look for statutory references
    statute_patterns = [
        r'Section\s+(\d+)\s+(?:of\s+)?(?:the\s+)?(?:Indian\s+Penal\s+Code|IPC)',
        r'Section\s+(\d+)\s+(?:of\s+)?(?:the\s+)?(?:IT\s+Act|Information\s+Technology\s+Act)'
    ]
    
    for pattern in statute_patterns:
        matches = re.findall(pattern, answer, re.IGNORECASE)
        for match in matches:
            citations.append(Citation(
                type="statute",
                reference=f"Section {match} IPC" if "IPC" in pattern else f"Section {match} IT Act",
                link=None
            ))
    
    # Ensure at least one citation exists
    if not citations:
        citations.append(Citation(
            type="constitution",
            reference="Fundamental Rights (Part III)",
            link=None
        ))
    
    return citations[:5]  # Limit to 5 citations

def _determine_urgency(scenario: str, user_text: str, answer: str) -> str:
    """Determine urgency level based on scenario and content."""
    
    emergency_keywords = ["violence", "immediate danger", "threat to life", "emergency", "urgent"]
    high_keywords = ["threat", "harassment", "intimidation", "fear", "safety"]
    medium_keywords = ["bribe", "corruption", "workplace", "ongoing"]
    
    text_lower = (user_text + " " + answer).lower()
    
    if any(keyword in text_lower for keyword in emergency_keywords):
        return "emergency"
    elif scenario in ["threat"] or any(keyword in text_lower for keyword in high_keywords):
        return "high"
    elif any(keyword in text_lower for keyword in medium_keywords):
        return "medium"
    else:
        return "low"

def _generate_actions(scenario: str, urgency: str) -> List[str]:
    """Generate recommended actions based on scenario and urgency."""
    
    base_actions = ["document_incident", "collect_evidence"]
    
    scenario_actions = {
        "bribe": ["call_police", "contact_authorities"],
        "threat": ["call_police", "legal_aid"],
        "harassment": ["contact_authorities", "legal_aid"],
        "online_harassment": ["block_report", "contact_authorities"],
        "workplace": ["legal_aid", "contact_authorities"],
        "other": ["legal_aid"]
    }
    
    actions = base_actions + scenario_actions.get(scenario, ["legal_aid"])
    
    # Add emergency actions for high urgency
    if urgency in ["emergency", "high"]:
        actions.insert(0, "call_police")
    
    return list(set(actions))  # Remove duplicates

def _generate_follow_up_questions(scenario: str, user_text: str) -> List[str]:
    """Generate relevant follow-up questions."""
    
    base_questions = [
        "Do you have any evidence or documentation of this incident?",
        "Have you reported this matter to any authorities?"
    ]
    
    scenario_questions = {
        "bribe": [
            "What amount was demanded and by whom?",
            "Was this demand made verbally or in writing?"
        ],
        "threat": [
            "What specific threats were made?",
            "Do you feel you are in immediate danger?"
        ],
        "harassment": [
            "How long has this harassment been ongoing?",
            "Have there been witnesses to these incidents?"
        ],
        "online_harassment": [
            "What platform did the harassment occur on?",
            "Have you saved screenshots or other evidence?"
        ],
        "workplace": [
            "Is there a HR department or grievance mechanism?",
            "Have you documented these workplace issues?"
        ],
        "other": [
            "Can you provide more specific details about your situation?"
        ]
    }
    
    questions = base_questions + scenario_questions.get(scenario, scenario_questions["other"])
    return questions[:4]  # Limit to 4 questions