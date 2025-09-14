#!/usr/bin/env python3
"""
Debug script to understand article structure and fix citation system.
"""

import logging
import re
from advanced_constitution_parser import AdvancedConstitutionParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_article_structure():
    """Analyze how articles are structured in the constitutional sections."""
    print("🔍 ANALYZING ARTICLE STRUCTURE")
    print("=" * 60)
    
    # Initialize parser
    parser = AdvancedConstitutionParser()
    sections = parser.parse_constitution()
    
    # Get article sections
    article_sections = [s for s in sections if s.section_type == 'article']
    print(f"Total article sections: {len(article_sections)}")
    
    # Analyze article content patterns
    print("\n📝 ARTICLE CONTENT PATTERNS:")
    for i, section in enumerate(article_sections[:10]):
        print(f"\nArticle {i+1}:")
        print(f"  Title: {section.title}")
        print(f"  Content preview: {section.content[:200]}...")
        print(f"  Section number: {section.section_number}")
        
        # Look for article numbers in content
        article_matches = re.findall(r'\b(\d+)\.\s*([^\n]+)', section.content[:500])
        if article_matches:
            print(f"  Detected patterns: {article_matches[:3]}")
    
    # Check specific patterns in content
    print("\n🔍 ANALYZING CONTENT FOR ARTICLE NUMBERS:")
    article_numbers = set()
    
    for section in article_sections[:50]:  # Check first 50
        # Look for numbered articles at start of content
        content_start = section.content[:100]
        number_match = re.match(r'^(\d+)\.\s*([^\n]+)', content_start.strip())
        if number_match:
            article_num = number_match.group(1)
            article_title = number_match.group(2)
            article_numbers.add(article_num)
            if len(article_numbers) <= 10:  # Show first 10 examples
                print(f"  Article {article_num}: {article_title}")
    
    print(f"\nFound {len(article_numbers)} distinct article numbers")
    
    # Test with specific articles
    print("\n🧪 TESTING ARTICLE LOOKUP:")
    test_articles = ['1', '19', '21', '32']
    
    for test_num in test_articles:
        found = False
        for section in article_sections:
            if section.content.strip().startswith(f"{test_num}."):
                print(f"  Article {test_num}: FOUND - {section.content[:100]}...")
                found = True
                break
        if not found:
            print(f"  Article {test_num}: NOT FOUND")


if __name__ == "__main__":
    analyze_article_structure()