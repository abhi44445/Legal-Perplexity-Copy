"""
Unit Tests for Know Your Rights Service
=======================================

Tests the core service functionality with mocked dependencies to ensure
proper business logic, citation extraction, and response formatting.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import the service under test
from features.know_your_rights.backend.service import (
    KnowYourRightsService,
    RightsQueryResult,
    sanitize_text
)

class TestKnowYourRightsService:
    """Test suite for KnowYourRightsService"""
    
    def setup_method(self):
        """Setup method run before each test"""
        # Create a mock RAG instance
        self.mock_rag = Mock()
        self.service = KnowYourRightsService(rag_instance=self.mock_rag)
    
    def test_sanitize_input_basic(self):
        """Test basic input sanitization"""
        # Test normal input
        result = self.service._sanitize_input("This is a normal legal question about my rights.")
        assert result == "This is a normal legal question about my rights."
        
        # Test input with extra whitespace
        result = self.service._sanitize_input("  Spaced input  ")
        assert result == "Spaced input"
    
    def test_sanitize_input_length_validation(self):
        """Test input length validation"""
        # Test input too short
        with pytest.raises(ValueError, match="Description too short"):
            self.service._sanitize_input("short")
        
        # Test input too long (over 2000 chars)
        long_input = "a" * 2500
        result = self.service._sanitize_input(long_input)
        assert len(result) <= 2003  # 2000 + "..."
        assert result.endswith("...")
    
    def test_sanitize_input_dangerous_content(self):
        """Test sanitization of potentially dangerous content"""
        dangerous_inputs = [
            "Help me <script>alert('xss')</script>",
            "My case involves javascript:void(0)",
            "Please exec('rm -rf /')",
            "Can you eval(malicious_code)",
            "DELETE FROM users WHERE id=1"
        ]
        
        for dangerous_input in dangerous_inputs:
            result = self.service._sanitize_input(dangerous_input + " and also help with my legal rights")
            assert "[CONTENT_REMOVED]" in result
            assert "legal rights" in result
    
    def test_extract_citations_constitutional(self):
        """Test extraction of constitutional citations"""
        answer = """
        Based on Article 21 of the Constitution, you have the right to life and liberty.
        Article 19(1)(g) protects your right to profession. Also consider Article 14 for equality.
        """
        
        mock_docs = []
        citations = self.service._extract_citations(answer, mock_docs)
        
        # Should extract Articles 21, 19(1)(g), and 14
        article_refs = [c["reference"] for c in citations if c["type"] == "constitution"]
        assert "Article 21" in article_refs
        assert "Article 19(1)(g)" in article_refs 
        assert "Article 14" in article_refs
    
    def test_extract_citations_statutory(self):
        """Test extraction of statutory citations"""
        answer = """
        This falls under Section 383 of the Indian Penal Code for extortion.
        You can also refer to Section 66A of the IT Act for cyber crimes.
        Section 145 of the Criminal Procedure Code may apply.
        """
        
        mock_docs = []
        citations = self.service._extract_citations(answer, mock_docs)
        
        # Should extract various statutory provisions
        statute_refs = [c["reference"] for c in citations if c["type"] == "statute"]
        assert any("383" in ref for ref in statute_refs)
        assert any("66A" in ref for ref in statute_refs)
        assert any("145" in ref for ref in statute_refs)
    
    def test_extract_citations_case_law(self):
        """Test extraction of case law citations"""
        answer = """
        In the landmark case of Kesavananda Bharati v. State of Kerala,
        the Supreme Court established important precedents. Also see
        Maneka Gandhi v. Union of India for procedural due process.
        """
        
        mock_docs = []
        citations = self.service._extract_citations(answer, mock_docs)
        
        # Should extract case references
        case_refs = [c["reference"] for c in citations if c["type"] == "case"]
        assert any("Kesavananda Bharati" in ref for ref in case_refs)
        assert any("Maneka Gandhi" in ref for ref in case_refs)
    
    def test_extract_citations_fallback(self):
        """Test citation extraction fallback when no citations found"""
        answer = "This is a generic response without specific legal citations."
        
        mock_docs = []
        citations = self.service._extract_citations(answer, mock_docs)
        
        # Should have at least one fallback citation
        assert len(citations) >= 1
        assert citations[0]["type"] == "constitution"
        assert "Fundamental Rights" in citations[0]["reference"]
    
    def test_determine_urgency_emergency(self):
        """Test urgency classification for emergency situations"""
        scenario = "threat"
        user_text = "Someone is threatening immediate violence against my family"
        answer = "Call police immediately as this is an emergency situation"
        
        urgency = self.service._determine_urgency(scenario, user_text, answer)
        assert urgency == "emergency"
    
    def test_determine_urgency_high(self):
        """Test urgency classification for high priority situations"""
        scenario = "threat"
        user_text = "My neighbor has been threatening me repeatedly"
        answer = "This constitutes criminal intimidation and requires prompt action"
        
        urgency = self.service._determine_urgency(scenario, user_text, answer)
        assert urgency == "high"
    
    def test_determine_urgency_medium(self):
        """Test urgency classification for medium priority situations"""
        scenario = "bribe"
        user_text = "A government official asked for a bribe to process my application"
        answer = "This is corruption and should be reported to authorities"
        
        urgency = self.service._determine_urgency(scenario, user_text, answer)
        assert urgency == "medium"
    
    def test_determine_urgency_low(self):
        """Test urgency classification for low priority situations"""
        scenario = "other"
        user_text = "I want to understand my general constitutional rights"
        answer = "You have various fundamental rights under the Constitution"
        
        urgency = self.service._determine_urgency(scenario, user_text, answer)
        assert urgency == "low"
    
    def test_generate_recommended_actions_emergency(self):
        """Test action generation for emergency situations"""
        scenario = "threat"
        urgency = "emergency"
        answer = "Immediate police intervention required"
        
        actions = self.service._generate_recommended_actions(scenario, urgency, answer)
        
        assert "call_police" in actions
        assert actions[0] == "call_police"  # Should be first for emergency
        assert "document_incident" in actions
        assert "collect_evidence" in actions
    
    def test_generate_recommended_actions_bribe(self):
        """Test action generation for bribery scenarios"""
        scenario = "bribe"
        urgency = "medium"
        answer = "Report this corruption to authorities"
        
        actions = self.service._generate_recommended_actions(scenario, urgency, answer)
        
        assert "contact_authorities" in actions
        assert "document_incident" in actions
        assert len(actions) <= 6  # Should be limited
    
    def test_generate_follow_up_questions_bribe(self):
        """Test follow-up question generation for bribe scenarios"""
        scenario = "bribe"
        user_text = "Official asked for money"
        answer = "This is corruption"
        
        questions = self.service._generate_follow_up_questions(scenario, user_text, answer)
        
        assert len(questions) <= 4  # Should be limited
        assert any("amount" in q.lower() for q in questions)
        assert any("evidence" in q.lower() or "document" in q.lower() for q in questions)
    
    def test_generate_follow_up_questions_threat(self):
        """Test follow-up question generation for threat scenarios"""
        scenario = "threat"
        user_text = "Someone threatened me"
        answer = "This is criminal intimidation"
        
        questions = self.service._generate_follow_up_questions(scenario, user_text, answer)
        
        assert any("specific" in q.lower() and "threat" in q.lower() for q in questions)
        assert any("danger" in q.lower() for q in questions)
    
    def test_calculate_confidence_high(self):
        """Test confidence calculation for high-quality responses"""
        rag_result = {
            "answer": "A" * 600,  # Long, comprehensive answer
            "reasoning": "Detailed reasoning provided"
        }
        context_docs = [Mock(), Mock(), Mock(), Mock()]  # 4 documents
        citations = [
            {"type": "constitution", "reference": "Article 21"},
            {"type": "statute", "reference": "Section 383 IPC"},
            {"type": "case", "reference": "Test v. Case"}
        ]
        
        confidence = self.service._calculate_confidence(rag_result, context_docs, citations)
        
        assert confidence >= 0.8  # Should be high confidence
        assert confidence <= 1.0  # Should not exceed 1.0
    
    def test_calculate_confidence_low(self):
        """Test confidence calculation for low-quality responses"""
        rag_result = {
            "answer": "Short answer",  # Short answer
            "reasoning": None
        }
        context_docs = []  # No documents
        citations = []  # No citations
        
        confidence = self.service._calculate_confidence(rag_result, context_docs, citations)
        
        assert confidence <= 0.6  # Should be low confidence
        assert confidence >= 0.0  # Should not be negative
    
    @patch('features.know_your_rights.backend.service.ConstitutionRAG')
    def test_process_query_success(self, mock_rag_class):
        """Test successful query processing with mocked RAG"""
        # Setup mocks
        mock_rag_instance = Mock()
        mock_rag_class.return_value = mock_rag_instance
        
        # Mock retrieval
        mock_docs = [
            Mock(page_content="Article 21 ensures right to life", metadata={"source": "constitution"}),
            Mock(page_content="Corruption is prohibited", metadata={"source": "law"})
        ]
        mock_rag_instance.retrieve_relevant_context.return_value = mock_docs
        
        # Mock RAG response
        mock_rag_result = {
            "status": "success",
            "answer": "Based on Article 21, you have the right to life and liberty. Corruption by officials violates your rights.",
            "reasoning": "Constitutional analysis shows...",
            "response_time": 2.5
        }
        mock_rag_instance.ask_constitutional_question.return_value = mock_rag_result
        
        # Create service with mocked RAG
        service = KnowYourRightsService(rag_instance=mock_rag_instance)
        
        # Process query
        result = service.process_query(
            scenario="bribe",
            user_text="A police officer asked me for Rs.500 to avoid a fine."
        )
        
        # Verify result
        assert isinstance(result, RightsQueryResult)
        assert result.legal_advice == mock_rag_result["answer"]
        assert len(result.citations) > 0
        assert result.urgency in ["low", "medium", "high", "emergency"]
        assert len(result.recommended_actions) > 0
        assert len(result.follow_up_questions) <= 4
        assert result.disclaimer == service.disclaimer
        assert 0.0 <= result.confidence_score <= 1.0
    
    @patch('features.know_your_rights.backend.service.ConstitutionRAG')
    def test_process_query_no_documents(self, mock_rag_class):
        """Test query processing when no relevant documents found"""
        # Setup mocks
        mock_rag_instance = Mock()
        mock_rag_class.return_value = mock_rag_instance
        
        # Mock empty retrieval
        mock_rag_instance.retrieve_relevant_context.return_value = []
        
        # Create service
        service = KnowYourRightsService(rag_instance=mock_rag_instance)
        
        # Process query
        result = service.process_query(
            scenario="other",
            user_text="I need help with my rights."
        )
        
        # Should return low confidence response
        assert isinstance(result, RightsQueryResult)
        assert result.confidence_score <= 0.5
        assert "don't have sufficient specific" in result.legal_advice
        assert len(result.recommended_actions) > 0
        assert result.disclaimer == service.disclaimer
    
    @patch('features.know_your_rights.backend.service.ConstitutionRAG')
    def test_process_query_rag_failure(self, mock_rag_class):
        """Test query processing when RAG generation fails"""
        # Setup mocks
        mock_rag_instance = Mock()
        mock_rag_class.return_value = mock_rag_instance
        
        # Mock documents available but RAG fails
        mock_docs = [Mock(page_content="Some content")]
        mock_rag_instance.retrieve_relevant_context.return_value = mock_docs
        
        mock_rag_result = {
            "status": "failed",
            "error": "Model unavailable"
        }
        mock_rag_instance.ask_constitutional_question.return_value = mock_rag_result
        
        # Create service
        service = KnowYourRightsService(rag_instance=mock_rag_instance)
        
        # Process query
        result = service.process_query(
            scenario="bribe",
            user_text="Need help with corruption issue."
        )
        
        # Should return fallback response
        assert isinstance(result, RightsQueryResult)
        assert "technical difficulties" in result.legal_advice
        assert result.confidence_score <= 0.5
    
    def test_process_query_handles_exceptions(self):
        """Test that service handles exceptions gracefully"""
        # Create service with mock that raises exception
        mock_rag = Mock()
        mock_rag.retrieve_relevant_context.side_effect = Exception("Network error")
        
        service = KnowYourRightsService(rag_instance=mock_rag)
        
        # Process query
        result = service.process_query(
            scenario="other",
            user_text="Test query that will cause an error."
        )
        
        # Should return error response
        assert isinstance(result, RightsQueryResult)
        assert "encountered an error" in result.legal_advice
        assert result.confidence_score <= 0.3

class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_sanitize_text_pii_redaction(self):
        """Test PII redaction in sanitize_text function"""
        test_cases = [
            # Phone numbers
            ("My number is 9876543210", "My number is [PHONE_REDACTED]"),
            ("Call me at 987-654-3210", "Call me at [PHONE_REDACTED]"),
            
            # Email addresses
            ("Email me at test@example.com", "Email me at [EMAIL_REDACTED]"),
            ("Contact: user.name+tag@domain.co.in", "Contact: [EMAIL_REDACTED]"),
            
            # Names (basic pattern)
            ("My name is John Smith", "My name is [NAME_REDACTED]"),
            ("Contact Priya Sharma for details", "Contact [NAME_REDACTED] for details"),
            
            # Addresses (basic pattern)
            ("I live at 123 MG Road", "I live at [ADDRESS_REDACTED]"),
            ("Visit 45 Park Street", "Visit [ADDRESS_REDACTED]"),
        ]
        
        for original, expected in test_cases:
            result = sanitize_text(original)
            assert result == expected

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])