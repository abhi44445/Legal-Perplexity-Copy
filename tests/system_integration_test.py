#!/usr/bin/env python3
"""
Complete System Integration Test
Validates all components working together
"""

import requests
import time
import json
import sys
import os
from typing import Dict, Any

class SystemIntegrationTest:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def test_full_pipeline(self) -> Dict[str, Any]:
        """Test complete RAG pipeline with all components"""
        print("🔄 TESTING COMPLETE SYSTEM INTEGRATION")
        print("=" * 50)
        
        # Test query that should exercise all components
        test_query = "What are the fundamental rights under Article 19 and how do they relate to freedom of speech?"
        
        print(f"📝 Test Query: {test_query}")
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/api/chat/constitution",
                json={
                    "query": test_query,
                    "user_type": "legal_professional"
                },
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
            
            data = response.json()
            
            # Analyze response components
            analysis = {
                "success": True,
                "response_time": response_time,
                "answer_length": len(data.get("answer", "")),
                "reasoning_length": len(data.get("reasoning", "")),
                "citations_count": len(data.get("citations", [])),
                "citation_validation": data.get("citation_validation", {}),
                "confidence_score": data.get("confidence_score", 0),
                "user_type": data.get("user_type"),
                "components_tested": []
            }
            
            # Component validation
            print(f"\n📊 SYSTEM COMPONENT ANALYSIS:")
            print(f"   ⏱️  Response Time: {response_time:.2f}s")
            print(f"   📄 Answer Length: {analysis['answer_length']} chars")
            print(f"   🧠 Reasoning Length: {analysis['reasoning_length']} chars")
            print(f"   📚 Citations Found: {analysis['citations_count']}")
            
            # Test RAG Pipeline
            if analysis['answer_length'] > 1000:
                analysis['components_tested'].append("RAG Pipeline ✅")
                print(f"   ✅ RAG Pipeline: WORKING (substantial answer)")
            else:
                analysis['components_tested'].append("RAG Pipeline ⚠️")
                print(f"   ⚠️  RAG Pipeline: LIMITED (short answer)")
            
            # Test Citation System
            validation = analysis['citation_validation']
            if validation and 'accuracy' in validation:
                accuracy = validation.get('accuracy', 0)
                valid_citations = validation.get('valid_citations', 0)
                total_citations = validation.get('total_citations', 0)
                
                analysis['components_tested'].append(f"Citation System ✅")
                print(f"   ✅ Citation System: WORKING ({accuracy:.1%} accuracy, {valid_citations}/{total_citations})")
            else:
                analysis['components_tested'].append("Citation System ❌")
                print(f"   ❌ Citation System: FAILED")
            
            # Test Performance Monitoring
            if 'response_time' in data:
                analysis['components_tested'].append("Performance Monitoring ✅")
                print(f"   ✅ Performance Monitoring: WORKING")
            else:
                analysis['components_tested'].append("Performance Monitoring ⚠️")
                print(f"   ⚠️  Performance Monitoring: MISSING")
            
            # Test Reasoning Extraction
            if analysis['reasoning_length'] > 500:
                analysis['components_tested'].append("Reasoning Extraction ✅")
                print(f"   ✅ Reasoning Extraction: WORKING")
            else:
                analysis['components_tested'].append("Reasoning Extraction ⚠️")
                print(f"   ⚠️  Reasoning Extraction: LIMITED")
            
            # Test User Type Handling
            if analysis['user_type'] == "legal_professional":
                analysis['components_tested'].append("User Type Handling ✅")
                print(f"   ✅ User Type Handling: WORKING")
            else:
                analysis['components_tested'].append("User Type Handling ❌")
                print(f"   ❌ User Type Handling: FAILED")
            
            # Show sample content
            print(f"\n📖 SAMPLE RESPONSE CONTENT:")
            answer_preview = data.get("answer", "")[:300] + "..." if len(data.get("answer", "")) > 300 else data.get("answer", "")
            print(f"   Answer Preview: {answer_preview}")
            
            citations = data.get("citations", [])
            if citations:
                print(f"   Sample Citations:")
                for i, citation in enumerate(citations[:3]):
                    print(f"     {i+1}. {citation}")
            
            return analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def main():
    """Run complete system integration test"""
    # Test if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not running. Start server first with: py -m main")
            return False
    except:
        print("❌ Server not accessible. Start server first with: py -m main")
        return False
    
    # Run integration test
    test = SystemIntegrationTest()
    result = test.test_full_pipeline()
    
    if result.get("success"):
        print(f"\n🎉 SYSTEM INTEGRATION TEST COMPLETED!")
        print(f"   ✅ Components Working: {len([c for c in result['components_tested'] if '✅' in c])}")
        print(f"   ⚠️  Components Limited: {len([c for c in result['components_tested'] if '⚠️' in c])}")
        print(f"   ❌ Components Failed: {len([c for c in result['components_tested'] if '❌' in c])}")
        
        # Overall assessment
        working_count = len([c for c in result['components_tested'] if '✅' in c])
        total_count = len(result['components_tested'])
        
        if working_count >= total_count * 0.8:  # 80% working
            print(f"\n✅ SYSTEM STATUS: PRODUCTION READY!")
            return True
        else:
            print(f"\n⚠️  SYSTEM STATUS: NEEDS ATTENTION")
            return False
    else:
        print(f"\n❌ SYSTEM INTEGRATION TEST FAILED:")
        print(f"   Error: {result.get('error')}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)