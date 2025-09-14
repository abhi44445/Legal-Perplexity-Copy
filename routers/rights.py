"""
Know Your Rights API Router
============================

Provides REST API endpoints for citizen rights information.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Response models
class RightCategory(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    article_references: List[str]

class RightsCategoriesResponse(BaseModel):
    categories: List[RightCategory]
    total_categories: int

class RightsSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    category: Optional[str] = None

class RightsSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_results: int
    query: str

@router.get("/categories", response_model=RightsCategoriesResponse)
async def get_rights_categories():
    """Get all available rights categories."""
    try:
        categories = [
            {
                "id": "fundamental_rights",
                "title": "Fundamental Rights",
                "description": "Basic rights guaranteed by the Constitution",
                "icon": "shield",
                "article_references": ["Article 12-35"]
            },
            {
                "id": "equality_rights", 
                "title": "Right to Equality",
                "description": "Equal treatment and non-discrimination",
                "icon": "balance",
                "article_references": ["Article 14-18"]
            },
            {
                "id": "freedom_rights",
                "title": "Right to Freedom", 
                "description": "Freedom of speech, movement, and association",
                "icon": "bird",
                "article_references": ["Article 19-22"]
            },
            {
                "id": "education_rights",
                "title": "Right to Education",
                "description": "Free and compulsory education",
                "icon": "book",
                "article_references": ["Article 21A"]
            },
            {
                "id": "privacy_rights",
                "title": "Right to Privacy",
                "description": "Protection of personal information and privacy",
                "icon": "lock",
                "article_references": ["Article 21"]
            },
            {
                "id": "constitutional_remedies",
                "title": "Constitutional Remedies",
                "description": "Right to constitutional remedies",
                "icon": "gavel",
                "article_references": ["Article 32"]
            }
        ]
        
        return RightsCategoriesResponse(
            categories=categories,
            total_categories=len(categories)
        )
        
    except Exception as e:
        logger.error(f"Error getting rights categories: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving rights categories: {str(e)}"
        )

@router.post("/search", response_model=RightsSearchResponse)
async def search_rights(request: RightsSearchRequest):
    """Search for specific rights information."""
    try:
        # TODO: Implement actual search functionality
        # This would integrate with the constitutional database
        
        results = [
            {
                "title": f"Search result for: {request.query}",
                "description": "Detailed explanation would go here",
                "article_reference": "Article XX",
                "category": request.category or "general"
            }
        ]
        
        return RightsSearchResponse(
            results=results,
            total_results=len(results),
            query=request.query
        )
        
    except Exception as e:
        logger.error(f"Error searching rights: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching rights: {str(e)}"
        )

@router.post("/generate-pdf")
async def generate_rights_pdf():
    """Generate PDF guide for rights information."""
    try:
        # TODO: Implement PDF generation
        return {"message": "PDF generation feature coming soon"}
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF: {str(e)}"
        )