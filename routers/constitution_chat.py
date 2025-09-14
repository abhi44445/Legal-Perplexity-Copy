"""
Constitution Chat API Router
============================

Provides REST API endpoints for constitutional legal questions.
Integrates with existing ConstitutionRAG system without modifications.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
import time

# Import existing RAG system
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from constitution_chat.core.constitution_rag import ConstitutionRAG

logger = logging.getLogger(__name__)

router = APIRouter()

# Global RAG instance (same pattern as main.py)
_constitution_rag: Optional[ConstitutionRAG] = None
_rag_initialization_lock = False

def get_constitution_rag() -> ConstitutionRAG:
    """Get initialized Constitution RAG system (sync version for FastAPI)."""
    global _constitution_rag, _rag_initialization_lock
    
    if _constitution_rag is None and not _rag_initialization_lock:
        _rag_initialization_lock = True
        try:
            logger.info("Initializing Constitution RAG system...")
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
class ConstitutionChatRequest(BaseModel):
    query: str = Field(..., description="Constitutional legal question", min_length=1, max_length=1000)
    user_type: Optional[str] = Field("general_public", description="User type: lawyer, law_student, general_public")

class ConstitutionChatResponse(BaseModel):
    answer: str
    reasoning: str
    citations: List[Dict[str, Any]]
    citation_validation: Dict[str, Any]
    response_time: float
    confidence_score: Optional[float] = None
    user_type: str

class ChatHistoryResponse(BaseModel):
    history: List[Dict[str, Any]]
    total_queries: int

class QuickSuggestionsResponse(BaseModel):
    suggestions: List[Dict[str, str]]
    user_type: str

@router.post("/constitution", response_model=ConstitutionChatResponse)
def ask_constitutional_question(
    request: ConstitutionChatRequest,
    rag: ConstitutionRAG = Depends(get_constitution_rag)
):
    """
    Ask a constitutional legal question and get an AI-powered response.
    
    This endpoint preserves all existing functionality from the Streamlit version:
    - DeepSeek R1 reasoning capabilities
    - Citation validation and accuracy scoring
    - Transparent reasoning process
    - User type-specific responses
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing constitutional query: {request.query[:50]}...")
        
        # Use existing RAG system with enhanced error handling
        result = rag.ask_constitutional_question(request.query, request.user_type)
        
        response_time = time.time() - start_time
        logger.info(f"RAG processing completed successfully in {response_time:.2f}s")
        
        # Extract citations from citation_validation
        citation_validation = result.get("citation_validation", {})
        citations = []
        
        # Convert citation validation to proper citations list
        if citation_validation:
            response_citations = citation_validation.get("response_citations", {})
            valid_articles = citation_validation.get("valid_articles", [])
            
            # Create citations list from articles
            for article in response_citations.get("articles", []):
                citations.append({
                    "type": "article",
                    "reference": article,
                    "is_valid": article in valid_articles
                })
            
            # Add parts citations
            for part in response_citations.get("parts", []):
                citations.append({
                    "type": "part",
                    "reference": part,
                    "is_valid": True  # Parts are generally valid
                })
        
        response = ConstitutionChatResponse(
            answer=result.get("answer", ""),
            reasoning=result.get("reasoning", ""),
            citations=citations,
            citation_validation=citation_validation,
            response_time=result.get("response_time", response_time),
            confidence_score=citation_validation.get("citation_accuracy"),
            user_type=request.user_type
        )
        
        logger.info(f"Successfully generated AI response for: {request.query[:50]}...")
        logger.info(f"Response length: {len(response.answer)} chars, Citations: {len(citations)}")
        
        return response
        
    except Exception as e:
        logger.error(f"RAG processing failed for query '{request.query[:50]}...': {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Fallback response if RAG fails
        fallback_response = ConstitutionChatResponse(
            answer=f"I apologize, but I encountered an error while processing your question about '{request.query}'. Please try again or rephrase your question. The error has been logged for investigation.",
            reasoning="RAG system encountered an error during processing. This is likely due to resource constraints or model connectivity issues.",
            citations=[],
            citation_validation={},
            response_time=time.time() - start_time,
            confidence_score=0.0,
            user_type=request.user_type
        )
        
        logger.info(f"Returned fallback response due to RAG error")
        return fallback_response
        
    except Exception as e:
        logger.error(f"Error in constitutional question processing: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing constitutional question: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Error in constitutional question processing: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing constitutional question: {str(e)}"
        )

@router.get("/suggestions", response_model=QuickSuggestionsResponse)
def get_quick_suggestions(user_type: str = "general_public"):
    """
    Get quick query suggestions based on user type.
    Preserves the same suggestions from the Streamlit version.
    """
    try:
        # Same suggestions as in constitution_app.py
        suggestions_map = {
            "lawyer": [
                {"title": "Article 14 Interpretation", "query": "Explain the scope and limitations of Article 14 equality before law"},
                {"title": "Emergency Provisions Analysis", "query": "Analyze the constitutional provisions for emergency and their judicial review"},
                {"title": "Fundamental Rights vs DPSP", "query": "Compare fundamental rights and directive principles in constitutional jurisprudence"},
                {"title": "Amendment Procedure", "query": "Explain Article 368 and the constitutional amendment process"},
                {"title": "Federal Structure", "query": "Analyze the federal structure of Indian Constitution"}
            ],
            "law_student": [
                {"title": "Basic Structure Doctrine", "query": "What is the basic structure doctrine and its significance?"},
                {"title": "Separation of Powers", "query": "Explain separation of powers in the Indian Constitution"},
                {"title": "Judicial Review", "query": "What is judicial review and its scope in India?"},
                {"title": "Fundamental Duties", "query": "Explain fundamental duties under Article 51A"},
                {"title": "Constitutional Remedies", "query": "What are constitutional remedies under Article 32?"}
            ],
            "general_public": [
                {"title": "Right to Education", "query": "What are my rights to education under the Constitution?"},
                {"title": "Freedom of Speech", "query": "What does freedom of speech and expression mean for me?"},
                {"title": "Right to Privacy", "query": "Is privacy a fundamental right in India?"},
                {"title": "Equality Rights", "query": "How does the Constitution protect my right to equality?"},
                {"title": "Religious Freedom", "query": "What are my rights regarding religion and belief?"}
            ]
        }
        
        suggestions = suggestions_map.get(user_type, suggestions_map["general_public"])
        
        return QuickSuggestionsResponse(
            suggestions=suggestions,
            user_type=user_type
        )
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving suggestions: {str(e)}"
        )

@router.get("/history", response_model=ChatHistoryResponse)
def get_chat_history():
    """
    Get chat history (placeholder for now - would integrate with session management).
    """
    # TODO: Implement session management and history storage
    return ChatHistoryResponse(
        history=[],
        total_queries=0
    )