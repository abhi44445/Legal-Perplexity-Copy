"""
Constitution Database Module
===========================

Implements vector database functionality for constitutional documents using:
- OpenAI Embeddings via OpenRouter API
- FAISS vector store for efficient similarity search
- Optimized chunking for legal documents

This module handles loading, processing, and indexing the Constitution of India
for RAG-based legal question answering.
"""

import os
import random
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging
from dotenv import load_dotenv
import sys

# Fix for PyTorch classes issue in Python 3.13
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

# Add parent directory to path for imports
sys.path.append('../..')
from constitution_chat.parsers.advanced_constitution_parser import AdvancedConstitutionParser, ConstitutionalSection

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConstitutionDatabase:
    """
    Manages the Constitution vector database with OpenRouter integration.
    
    Features:
    - OpenAI embeddings via OpenRouter API
    - FAISS vector store for fast similarity search
    - Optimized chunking (1500 tokens, 300 overlap)
    - Legal document preprocessing
    """
    
    def __init__(self, 
                 pdf_path: str = "data/THE CONSTITUTION OF INDIA.pdf",
                 vectorstore_path: str = "vectorstore/constitution_faiss",
                 chunk_size: int = 1500,
                 chunk_overlap: int = 300):
        """
        Initialize Constitution Database.
        
        Args:
            pdf_path: Path to Constitution PDF file
            vectorstore_path: Path to save/load FAISS vectorstore
            chunk_size: Size of text chunks for embedding (default: 1500)
            chunk_overlap: Overlap between chunks (default: 300)
        """
        self.pdf_path = Path(pdf_path)
        self.vectorstore_path = Path(vectorstore_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize OpenRouter embeddings
        self.embeddings = self._setup_embeddings()
        
        # Initialize text splitter for legal documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        self.vectorstore: Optional[FAISS] = None
        
    def _setup_embeddings(self, force_mock: bool = False) -> HuggingFaceEmbeddings:
        """Setup HuggingFace embeddings for local processing with memory optimization and fallbacks."""
        
        # Check environment variable first
        use_mock = os.environ.get('USE_MOCK_EMBEDDINGS', 'false').lower() == 'true'
        
        if force_mock or use_mock:
            logger.warning("Using mock embeddings (set USE_MOCK_EMBEDDINGS=false to use real models)")
            return self._create_mock_embeddings()
        
        # Try different models in order of memory efficiency and reliability
        models_to_try = [
            ("sentence-transformers/all-MiniLM-L6-v2", {"device": "cpu"}),
            ("sentence-transformers/all-MiniLM-L12-v2", {"device": "cpu"}),
            ("sentence-transformers/paraphrase-MiniLM-L3-v2", {"device": "cpu"}),
        ]
        
        for model_name, model_kwargs in models_to_try:
            try:
                logger.info(f"Attempting to load embedding model: {model_name}")
                
                # Test if the model can be loaded
                embeddings = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs={
                        'batch_size': 4,  # Small batch size for memory efficiency
                        'convert_to_numpy': True,
                        'normalize_embeddings': True  # Better for similarity search
                    }
                )
                
                # Test the embedding with a simple query
                test_text = "test constitutional text"
                test_embedding = embeddings.embed_query(test_text)
                
                if test_embedding and len(test_embedding) > 0:
                    logger.info(f"Successfully loaded {model_name} with {len(test_embedding)} dimensions")
                    return embeddings
                else:
                    logger.warning(f"Model {model_name} loaded but returned empty embedding")
                    
            except Exception as e:
                logger.warning(f"Failed to load {model_name}: {e}")
                continue
        
        # Final fallback - create a mock embeddings class
        logger.warning("All embedding models failed, using mock embeddings")
        return self._create_mock_embeddings()
    
    def _create_mock_embeddings(self):
        """Create mock embeddings for fallback."""
        class MockEmbeddings:
            """Mock embeddings that return random vectors for testing."""
            
            def __init__(self):
                self.dimension = 384  # Standard dimension for MiniLM models
                
            def embed_documents(self, texts):
                """Return mock embeddings for documents."""
                return [[random.random() for _ in range(self.dimension)] for _ in texts]
            
            def embed_query(self, text):
                """Return mock embedding for a query."""
                return [random.random() for _ in range(self.dimension)]
            
            def __call__(self, text):
                """Make the embeddings object callable (for FAISS compatibility)."""
                if isinstance(text, list):
                    return self.embed_documents(text)
                else:
                    return self.embed_query(text)
        
        return MockEmbeddings()
    
    def load_and_process_constitution(self) -> List[Document]:
        """
        Load and process the Constitution PDF into chunks using advanced parser.
        
        Returns:
            List of processed document chunks with enhanced metadata
        """
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Constitution PDF not found at {self.pdf_path}")
            
        logger.info(f"Loading Constitution from {self.pdf_path} using advanced parser")
        
        try:
            # Use advanced parser to extract constitutional sections
            parser = AdvancedConstitutionParser(str(self.pdf_path))
            constitutional_sections = parser.parse_constitution()
            
            logger.info(f"Advanced parser extracted {len(constitutional_sections)} constitutional sections")
            
            # Convert constitutional sections to LangChain documents
            documents = []
            for section in constitutional_sections:
                # Skip very short sections (likely parsing artifacts)
                if len(section.content.strip()) < 50:
                    continue
                
                # Create enhanced metadata
                metadata = {
                    'source': str(self.pdf_path),
                    'title': section.title or 'Constitutional Content',
                    'document_type': 'constitutional_law',
                    'section_type': section.section_type,
                    'section_number': section.section_number,
                    'part_number': section.part_number,
                    'chapter_number': section.chapter_number,
                    'page_number': section.page_number,
                    **section.metadata
                }
                
                # Create document
                doc = Document(
                    page_content=section.content,
                    metadata=metadata
                )
                documents.append(doc)
            
            logger.info(f"Created {len(documents)} documents from constitutional sections")
            
            # Split documents into optimized chunks for legal content
            all_chunks = []
            for doc in documents:
                chunks = self.text_splitter.split_documents([doc])
                
                # Enhance chunk metadata
                for i, chunk in enumerate(chunks):
                    chunk.metadata.update({
                        'chunk_id': len(all_chunks) + i,
                        'parent_section': doc.metadata.get('section_type', 'unknown'),
                        'is_constitutional_content': True
                    })
                
                all_chunks.extend(chunks)
            
            logger.info(f"Split into {len(all_chunks)} optimized chunks for embedding")
            
            # Log statistics
            stats = self._get_processing_stats(constitutional_sections, all_chunks)
            logger.info(f"Processing statistics: {stats}")
            
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error processing Constitution with advanced parser: {e}")
            # Fallback to sample content if advanced parsing fails
            logger.warning("Falling back to sample Constitution content")
            return self._load_sample_constitution()
    
    def _load_sample_constitution(self) -> List[Document]:
        """Fallback method to load sample constitution content."""
        sample_content = """
        THE CONSTITUTION OF INDIA
        
        PREAMBLE
        WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a 
        SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC and to secure to all its citizens:
        JUSTICE, social, economic and political;
        LIBERTY of thought, expression, belief, faith and worship;
        EQUALITY of status and of opportunity;
        and to promote among them all
        FRATERNITY assuring the dignity of the individual and the unity and integrity of the Nation;
        IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949, do HEREBY ADOPT, 
        ENACT AND GIVE TO OURSELVES THIS CONSTITUTION.
        
        PART III - FUNDAMENTAL RIGHTS
        
        Article 14. Equality before law
        The State shall not deny to any person equality before the law or the equal protection 
        of the laws within the territory of India.
        
        Article 15. Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth
        (1) The State shall not discriminate against any citizen on grounds only of religion, race, 
        caste, sex, place of birth or any of them.
        
        Article 16. Equality of opportunity in matters of public employment
        (1) There shall be equality of opportunity for all citizens in matters relating to employment 
        or appointment to any office under the State.
        
        Article 19. Protection of certain rights regarding freedom of speech etc.
        (1) All citizens shall have the right to—
        (a) freedom of speech and expression;
        (b) assemble peaceably and without arms;
        (c) form associations or unions;
        (d) move freely throughout the territory of India;
        (e) reside and settle in any part of the territory of India; and
        (f) practise any profession, or to carry on any occupation, trade or business.
        
        Article 21. Protection of life and personal liberty
        No person shall be deprived of his life or personal liberty except according to procedure 
        established by law.
        """
        
        # Create document from sample content
        full_document = Document(
            page_content=sample_content,
            metadata={
                'source': str(self.pdf_path),
                'title': 'Constitution of India (Sample)',
                'document_type': 'constitutional_law',
                'is_sample_content': True
            }
        )
        
        # Split into chunks
        chunks = self.text_splitter.split_documents([full_document])
        
        # Add metadata for constitutional sections
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                'source': 'Constitution of India (Sample)',
                'chunk_id': i,
                'document_type': 'constitutional_law',
                'is_sample_content': True
            })
            
        logger.info(f"Created {len(chunks)} chunks from sample Constitution")
        return chunks
    
    def _get_processing_stats(self, sections: List[ConstitutionalSection], chunks: List[Document]) -> Dict[str, Any]:
        """Get processing statistics for logging."""
        return {
            'total_sections': len(sections),
            'articles': len([s for s in sections if s.section_type == 'article']),
            'parts': len([s for s in sections if s.section_type == 'part']),
            'schedules': len([s for s in sections if s.section_type == 'schedule']),
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(len(c.page_content) for c in chunks) / len(chunks) if chunks else 0,
            'fundamental_rights': len([s for s in sections if s.section_type == 'article' and s.metadata.get('is_fundamental_right', False)]),
            'directive_principles': len([s for s in sections if s.section_type == 'article' and s.metadata.get('is_directive_principle', False)])
        }
    
    def create_vectorstore(self, force_recreate: bool = False) -> FAISS:
        """
        Create or load FAISS vectorstore.
        
        Args:
            force_recreate: If True, recreate even if vectorstore exists
            
        Returns:
            FAISS vectorstore instance
        """
        # Check if vectorstore already exists
        if self.vectorstore_path.exists() and not force_recreate:
            logger.info(f"Loading existing vectorstore from {self.vectorstore_path}")
            try:
                # Handle PyTorch classes issue with careful loading
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning)
                    self.vectorstore = FAISS.load_local(
                        str(self.vectorstore_path), 
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                return self.vectorstore
            except Exception as e:
                logger.warning(f"Failed to load existing vectorstore: {e}")
                logger.info("Creating new vectorstore...")
                # If loading fails due to PyTorch issues, recreate
                force_recreate = True
        
        # Create vectorstore directory
        self.vectorstore_path.mkdir(parents=True, exist_ok=True)
        
        # Load and process documents
        documents = self.load_and_process_constitution()
        
        logger.info("Creating FAISS vectorstore with OpenRouter embeddings...")
        
        # Create vectorstore
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # Save vectorstore
        self.vectorstore.save_local(str(self.vectorstore_path))
        logger.info(f"Vectorstore saved to {self.vectorstore_path}")
        
        return self.vectorstore
    
    def get_vectorstore(self) -> FAISS:
        """Get the vectorstore, creating if necessary with performance optimizations."""
        if self.vectorstore is None:
            # Use lazy loading for better performance
            if self.vectorstore_path.exists():
                try:
                    logger.info(f"Loading cached vectorstore from {self.vectorstore_path}")
                    # Optimized loading with reduced warnings
                    import warnings
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore")
                        self.vectorstore = FAISS.load_local(
                            str(self.vectorstore_path), 
                            self.embeddings,
                            allow_dangerous_deserialization=True
                        )
                    logger.info("Vectorstore loaded successfully from cache")
                except Exception as e:
                    logger.warning(f"Cache load failed: {e}, creating new vectorstore")
                    self.vectorstore = self.create_vectorstore(force_recreate=True)
            else:
                self.vectorstore = self.create_vectorstore()
        return self.vectorstore
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for similar constitutional content.
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of similar documents
        """
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search(query, k=k)
    
    def search_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """
        Search with similarity scores.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search_with_score(query, k=k)


def main():
    """Test the Constitution Database functionality."""
    try:
        # Initialize database
        db = ConstitutionDatabase()
        
        # Create/load vectorstore
        vectorstore = db.create_vectorstore()
        
        # Test search
        query = "fundamental rights"
        results = db.search_similar(query, k=3)
        
        print(f"\nSearch results for '{query}':")
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc.page_content[:200]}...")
            print(f"   Source: {doc.metadata.get('source', 'Unknown')}")
            print()
            
    except Exception as e:
        logger.error(f"Error in Constitution Database: {e}")
        raise


if __name__ == "__main__":
    main()