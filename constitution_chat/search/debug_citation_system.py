#!/usr/bin/env python3
"""
Debug script for citation system analysis.
"""

import logging
from advanced_constitution_parser import AdvancedConstitutionParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_constitutional_sections():
    """Analyze the structure of constitutional sections."""
    print("🔍 ANALYZING CONSTITUTIONAL SECTIONS STRUCTURE")
    print("=" * 60)
    
    # Initialize parser
    parser = AdvancedConstitutionParser()
    sections = parser.parse_constitution()
    
    print(f"Total sections found: {len(sections)}")
    print()
    
    # Analyze section types
    section_types = {}
    for section in sections:
        section_type = section.section_type
        if section_type not in section_types:
            section_types[section_type] = []
        section_types[section_type].append(section)
    
    print("📊 SECTION TYPES BREAKDOWN:")
    for section_type, sections_list in section_types.items():
        print(f"  {section_type}: {len(sections_list)} sections")
    print()
    
    # Show some examples of each type
    print("📝 SECTION TYPE EXAMPLES:")
    for section_type, sections_list in section_types.items():
        print(f"\n{section_type.upper()} Examples:")
        for i, section in enumerate(sections_list[:3]):  # Show first 3
            print(f"  {i+1}. Title: {section.title[:80]}...")
            print(f"     Content: {section.content[:100]}...")
            print(f"     Page: {section.page_number}")
    
    # Specifically look for article-like content
    print("\n🔍 SEARCHING FOR ARTICLE PATTERNS:")
    article_sections = []
    for section in sections:
        if 'article' in section.title.lower() or 'article' in section.content[:200].lower():
            article_sections.append(section)
    
    print(f"Found {len(article_sections)} sections with 'article' in title/content")
    
    if article_sections:
        print("\nFirst 5 article-like sections:")
        for i, section in enumerate(article_sections[:5]):
            print(f"  {i+1}. {section.title}")
            print(f"     Type: {section.section_type}")
            print(f"     Content: {section.content[:150]}...")
            print()
    
    # Test citation patterns
    print("🔍 TESTING CITATION EXTRACTION:")
    test_text = """
    Article 19 of the Constitution guarantees freedom of speech and expression.
    Part III deals with fundamental rights.
    Section 23 prohibits traffic in human beings.
    Schedule VII contains the Union List.
    """
    
    from advanced_citation_system import CitationExtractor
    extractor = CitationExtractor()
    citations = extractor.extract_citations(test_text)
    
    print(f"Test text: {test_text}")
    print(f"Citations extracted: {len(citations)}")
    for citation in citations:
        print(f"  - {citation['raw_text']} (groups: {citation['groups']})")


if __name__ == "__main__":
    analyze_constitutional_sections()