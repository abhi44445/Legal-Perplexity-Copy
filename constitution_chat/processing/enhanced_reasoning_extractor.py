"""
Enhanced Reasoning Chain Extractor
==================================

Fixes the broken DeepSeek R1 <thinking> tag extraction with:
- Robust regex patterns for multiple thinking tag formats
- Multi-line reasoning extraction with proper formatting
- Validation and error handling for malformed responses
- Structured reasoning display for transparency

This module addresses the critical 0% functional reasoning chain issue.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReasoningChainExtractor:
    """
    Enhanced reasoning chain extractor for DeepSeek R1 responses.
    
    Features:
    - Multiple thinking tag format support
    - Robust multi-line extraction
    - Structured reasoning parsing
    - Error handling and fallback methods
    """
    
    def __init__(self):
        """Initialize the reasoning chain extractor."""
        
        # Multiple patterns for different thinking tag formats
        self.thinking_patterns = [
            # Standard format: <thinking>...</thinking>
            re.compile(r'<thinking>(.*?)</thinking>', re.DOTALL | re.IGNORECASE),
            
            # Variations with whitespace
            re.compile(r'<\s*thinking\s*>(.*?)<\s*/\s*thinking\s*>', re.DOTALL | re.IGNORECASE),
            
            # With attributes: <thinking type="analysis">...</thinking>
            re.compile(r'<thinking[^>]*>(.*?)</thinking>', re.DOTALL | re.IGNORECASE),
            
            # Alternative formats
            re.compile(r'\[thinking\](.*?)\[/thinking\]', re.DOTALL | re.IGNORECASE),
            re.compile(r'##\s*thinking\s*##(.*?)##\s*/thinking\s*##', re.DOTALL | re.IGNORECASE),
            
            # For responses that use reasoning without tags
            re.compile(r'(?:reasoning|analysis|thought process):\s*(.*?)(?:\n\n|$)', re.DOTALL | re.IGNORECASE)
        ]
        
        # Patterns for step identification
        self.step_patterns = [
            re.compile(r'(\d+)\.?\s+([A-Z\s]+):\s*(.*?)(?=\n\d+\.|\n\n|$)', re.MULTILINE),
            re.compile(r'step\s+(\d+):\s*(.*?)(?=step\s+\d+|\n\n|$)', re.IGNORECASE | re.MULTILINE),
            re.compile(r'-\s*([A-Z\s]+):\s*(.*?)(?=\n-|\n\n|$)', re.MULTILINE)
        ]
        
        # Constitutional analysis keywords
        self.constitutional_keywords = {
            'identification': ['identify', 'constitutional area', 'fundamental rights', 'directive principles'],
            'location': ['locate', 'relevant articles', 'provisions', 'constitutional text'],
            'verification': ['verify', 'article citations', 'accurate', 'complete'],
            'cross_reference': ['cross-references', 'related provisions', 'constitutional links'],
            'interpretation': ['legal interpretation', 'sound reasoning', 'constitutional meaning'],
            'validation': ['validate', 'constitutional text', 'grounded', 'verified']
        }
    
    def extract_reasoning_chain(self, response_text: str) -> Dict[str, Any]:
        """
        Extract and structure the reasoning chain from response text.
        
        Args:
            response_text: Full response text from the LLM
            
        Returns:
            Dictionary containing structured reasoning information
        """
        if not response_text or not isinstance(response_text, str):
            logger.warning("Empty or invalid response text for reasoning extraction")
            return self._empty_reasoning_result()
        
        logger.info(f"Extracting reasoning from {len(response_text)} character response")
        
        # Try different patterns to extract thinking content
        raw_reasoning = self._extract_thinking_content(response_text)
        
        if not raw_reasoning:
            logger.warning("No thinking tags found, attempting alternative extraction")
            raw_reasoning = self._extract_alternative_reasoning(response_text)
        
        if not raw_reasoning:
            logger.error("Failed to extract any reasoning content")
            return self._empty_reasoning_result()
        
        # Structure the reasoning
        structured_reasoning = self._structure_reasoning(raw_reasoning)
        
        # Analyze constitutional reasoning quality
        quality_analysis = self._analyze_reasoning_quality(raw_reasoning)
        
        # Clean and format the reasoning
        formatted_reasoning = self._format_reasoning_display(raw_reasoning, structured_reasoning)
        
        result = {
            'raw_reasoning': raw_reasoning.strip(),
            'structured_steps': structured_reasoning,
            'formatted_display': formatted_reasoning,
            'quality_analysis': quality_analysis,
            'extraction_success': True,
            'reasoning_length': len(raw_reasoning.strip()),
            'step_count': len(structured_reasoning)
        }
        
        logger.info(f"Successfully extracted reasoning with {len(structured_reasoning)} steps")
        return result
    
    def _extract_thinking_content(self, text: str) -> str:
        """Extract content from thinking tags using multiple patterns."""
        for pattern in self.thinking_patterns:
            match = pattern.search(text)
            if match:
                content = match.group(1).strip()
                if len(content) > 20:  # Minimum reasonable content length
                    logger.info(f"Extracted thinking content using pattern: {pattern.pattern[:50]}...")
                    return content
        return ""
    
    def _extract_alternative_reasoning(self, text: str) -> str:
        """Extract reasoning using alternative methods when thinking tags fail."""
        # Look for reasoning-like content at the start of responses
        lines = text.split('\n')
        reasoning_lines = []
        
        found_reasoning_start = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line contains reasoning keywords
            if any(keyword in line.lower() for keywords in self.constitutional_keywords.values() for keyword in keywords):
                found_reasoning_start = True
                reasoning_lines.append(line)
            elif found_reasoning_start:
                # Continue until we hit what looks like the final answer
                if line.startswith('Based on') or line.startswith('According to') or line.startswith('**'):
                    break
                reasoning_lines.append(line)
        
        if reasoning_lines:
            return '\n'.join(reasoning_lines)
        
        # Fallback: extract first substantial paragraph
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            if len(para.strip()) > 100 and ('constitutional' in para.lower() or 'article' in para.lower()):
                return para.strip()
        
        return ""
    
    def _structure_reasoning(self, reasoning_text: str) -> List[Dict[str, Any]]:
        """Structure reasoning into numbered steps."""
        structured_steps = []
        
        # Try different step extraction patterns
        for pattern in self.step_patterns:
            matches = pattern.findall(reasoning_text)
            if matches:
                for match in matches:
                    if len(match) >= 2:
                        step_data = {
                            'step_number': match[0] if match[0].isdigit() else len(structured_steps) + 1,
                            'step_title': match[1].strip() if len(match) > 2 else 'Analysis',
                            'step_content': match[-1].strip(),
                            'constitutional_area': self._identify_constitutional_area(match[-1])
                        }
                        structured_steps.append(step_data)
                
                if structured_steps:
                    break
        
        # If no structured steps found, create general steps
        if not structured_steps:
            structured_steps = self._create_general_steps(reasoning_text)
        
        return structured_steps
    
    def _create_general_steps(self, reasoning_text: str) -> List[Dict[str, Any]]:
        """Create general reasoning steps when structured extraction fails."""
        sentences = [s.strip() for s in reasoning_text.split('.') if s.strip()]
        
        steps = []
        for i, sentence in enumerate(sentences[:6], 1):  # Limit to 6 steps
            if len(sentence) > 20:  # Skip very short sentences
                steps.append({
                    'step_number': i,
                    'step_title': f'Analysis Step {i}',
                    'step_content': sentence,
                    'constitutional_area': self._identify_constitutional_area(sentence)
                })
        
        return steps
    
    def _identify_constitutional_area(self, text: str) -> str:
        """Identify the constitutional area being discussed."""
        text_lower = text.lower()
        
        area_indicators = {
            'fundamental_rights': ['fundamental rights', 'article 12', 'article 13', 'article 14', 'article 15', 'article 16', 'article 17', 'article 18', 'article 19', 'article 20', 'article 21', 'article 22'],
            'directive_principles': ['directive principles', 'part iv', 'article 36', 'article 37', 'article 38', 'article 39', 'article 40'],
            'union_government': ['union', 'parliament', 'president', 'prime minister', 'article 52', 'article 53'],
            'state_government': ['state', 'governor', 'chief minister', 'state legislature'],
            'judiciary': ['supreme court', 'high court', 'judicial', 'article 124', 'article 214'],
            'amendment': ['amendment', 'article 368', 'constitutional amendment'],
            'emergency': ['emergency', 'article 352', 'article 356', 'article 360'],
            'general': ['constitution', 'constitutional', 'legal']
        }
        
        for area, indicators in area_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return area
        
        return 'general'
    
    def _analyze_reasoning_quality(self, reasoning_text: str) -> Dict[str, Any]:
        """Analyze the quality of constitutional reasoning."""
        text_lower = reasoning_text.lower()
        
        quality_metrics = {
            'has_constitutional_references': any(term in text_lower for term in ['article', 'part', 'schedule', 'constitutional']),
            'has_step_by_step_analysis': bool(re.search(r'\d+\.', reasoning_text)),
            'has_legal_terminology': any(term in text_lower for term in ['provisions', 'clause', 'sub-article', 'amendment']),
            'has_citation_verification': any(term in text_lower for term in ['verify', 'validate', 'accurate', 'citation']),
            'has_cross_references': any(term in text_lower for term in ['related', 'cross-reference', 'connected']),
            'reasoning_length_adequate': len(reasoning_text.strip()) >= 100,
            'uses_constitutional_areas': len(set(self._identify_constitutional_area(sent) for sent in reasoning_text.split('.'))) > 1
        }
        
        quality_score = sum(quality_metrics.values()) / len(quality_metrics)
        
        return {
            'quality_score': quality_score,
            'quality_metrics': quality_metrics,
            'reasoning_completeness': 'complete' if quality_score >= 0.7 else 'partial' if quality_score >= 0.4 else 'basic'
        }
    
    def _format_reasoning_display(self, raw_reasoning: str, structured_steps: List[Dict[str, Any]]) -> str:
        """Format reasoning for display to users."""
        formatted_parts = []
        
        # Add header
        formatted_parts.append("🧠 CONSTITUTIONAL REASONING PROCESS")
        formatted_parts.append("=" * 50)
        
        # Add structured steps if available
        if structured_steps:
            for step in structured_steps:
                formatted_parts.append(f"\n{step['step_number']}. {step['step_title'].upper()}")
                formatted_parts.append(f"   {step['step_content']}")
                
                if step['constitutional_area'] != 'general':
                    formatted_parts.append(f"   📍 Area: {step['constitutional_area'].replace('_', ' ').title()}")
        else:
            # Fallback to raw reasoning with basic formatting
            formatted_parts.append("\nReasoning Analysis:")
            formatted_parts.append(raw_reasoning)
        
        return '\n'.join(formatted_parts)
    
    def _empty_reasoning_result(self) -> Dict[str, Any]:
        """Return empty result when reasoning extraction fails."""
        return {
            'raw_reasoning': '',
            'structured_steps': [],
            'formatted_display': 'Reasoning chain extraction failed. This may indicate the AI model did not provide structured thinking.',
            'quality_analysis': {'quality_score': 0.0, 'quality_metrics': {}, 'reasoning_completeness': 'failed'},
            'extraction_success': False,
            'reasoning_length': 0,
            'step_count': 0
        }
    
    def clean_response_text(self, response_text: str) -> str:
        """Clean response text by removing thinking tags."""
        if not response_text:
            return ""
        
        cleaned = response_text
        
        # Remove all thinking tag variations
        for pattern in self.thinking_patterns:
            cleaned = pattern.sub('', cleaned)
        
        # Clean up extra whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned


def test_reasoning_extractor():
    """Test the reasoning chain extractor with sample responses."""
    print("Testing Enhanced Reasoning Chain Extractor")
    print("=" * 50)
    
    extractor = ReasoningChainExtractor()
    
    # Test cases with different thinking tag formats
    test_cases = [
        # Standard thinking tags
        """<thinking>
Let me analyze this constitutional question step by step:

1. IDENTIFY the constitutional area: This question is about fundamental rights
2. LOCATE relevant articles: Article 19 covers freedom of speech and expression
3. VERIFY article citations: Article 19 is correctly referenced
4. CHECK for cross-references: Related to Article 14 (equality) and Article 21 (life and liberty)
5. ENSURE legal interpretation: Freedom of speech is subject to reasonable restrictions
6. VALIDATE based on constitutional text: This is grounded in Part III of the Constitution
</thinking>

Based on the constitutional provisions, Article 19 guarantees freedom of speech and expression...""",
        
        # Alternative format
        """[thinking]
Constitutional analysis needed for this question about directive principles.
Looking at Part IV of the Constitution.
Article 39 is the key provision here.
[/thinking]

The directive principles of state policy are outlined in Part IV...""",
        
        # No thinking tags
        """Let me analyze this constitutional question about fundamental rights.
First, I need to identify the relevant articles.
Article 21 protects life and personal liberty.
This is a fundamental right under Part III.

Based on constitutional analysis, the right to life..."""
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("-" * 30)
        
        result = extractor.extract_reasoning_chain(test_case)
        
        print(f"Extraction Success: {result['extraction_success']}")
        print(f"Reasoning Length: {result['reasoning_length']} characters")
        print(f"Steps Found: {result['step_count']}")
        print(f"Quality Score: {result['quality_analysis']['quality_score']:.2f}")
        
        if result['structured_steps']:
            print("Structured Steps:")
            for step in result['structured_steps'][:3]:  # Show first 3 steps
                print(f"  {step['step_number']}. {step['step_title']}: {step['step_content'][:80]}...")
        
        # Test cleaning
        cleaned = extractor.clean_response_text(test_case)
        print(f"Cleaned Response Length: {len(cleaned)} characters")
    
    print("\n✅ Reasoning extractor testing complete!")


if __name__ == "__main__":
    test_reasoning_extractor()