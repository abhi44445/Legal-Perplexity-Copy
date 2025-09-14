"""
Constitution Chat Package
========================

This package implements a RAG-based Constitution Chat feature for LegalPerplexity2.0.
It provides constitutional legal assistance using DeepSeek R1 reasoning capabilities
with OpenRouter API integration.

Features:
- Vector database with constitutional documents
- Enhanced RAG with reasoning chains
- Citation validation for legal accuracy
- Professional Streamlit interface

Author: LegalPerplexity2.0 Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "LegalPerplexity2.0 Team"

from .constitution_db import ConstitutionDatabase
from .constitution_rag import ConstitutionRAG
# Commenting out Streamlit app import to avoid warnings in FastAPI context
# from .constitution_app import main as run_app

__all__ = [
    "ConstitutionDatabase",
    "ConstitutionRAG", 
    # "run_app"  # Commented out - use FastAPI instead
]