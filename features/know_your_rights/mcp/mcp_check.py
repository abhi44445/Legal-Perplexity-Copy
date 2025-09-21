"""
Model Connectivity & Validation Check (MCP) for Know Your Rights
================================================================

This script validates the model endpoint connectivity and performs basic sanity checks
on the Know Your Rights service to ensure it's working correctly.
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, List
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Test configurations
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TEST_TIMEOUT = 30  # seconds

def test_api_connectivity() -> Dict[str, Any]:
    """Test basic API connectivity."""
    
    print("🔌 Testing API Connectivity...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return {"status": "success", "response_time": response.elapsed.total_seconds()}
        else:
            print(f"❌ API Health Check: FAILED (Status: {response.status_code})")
            return {"status": "failed", "error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        print(f"❌ API Health Check: FAILED (Connection Error: {e})")
        return {"status": "failed", "error": str(e)}

def test_know_your_rights_endpoint() -> Dict[str, Any]:
    """Test Know Your Rights endpoint connectivity."""
    
    print("\n🧪 Testing Know Your Rights Endpoint...")
    
    test_request = {
        "scenario": "bribe",
        "text": "A police officer stopped me and demanded Rs. 500 to avoid a traffic challan. This seems wrong to me.",
        "language": "en"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/api/know-your-rights/query",
            json=test_request,
            timeout=TEST_TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Know Your Rights Query: PASSED")
            print(f"⏱️ Response Time: {response_time:.2f}s")
            
            # Basic response validation
            required_fields = ["legal_advice", "citations", "recommended_actions", "urgency", "disclaimer"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"⚠️ Missing fields in response: {missing_fields}")
                return {"status": "partial", "missing_fields": missing_fields, "response_time": response_time}
            else:
                print("✅ Response Schema: VALID")
                return {"status": "success", "response_time": response_time, "data": data}
        
        else:
            print(f"❌ Know Your Rights Query: FAILED (Status: {response.status_code})")
            return {"status": "failed", "error": f"HTTP {response.status_code}", "response": response.text}
    
    except requests.exceptions.Timeout:
        print(f"❌ Know Your Rights Query: TIMEOUT (>{TEST_TIMEOUT}s)")
        return {"status": "failed", "error": "timeout"}
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Know Your Rights Query: FAILED (Connection Error: {e})")
        return {"status": "failed", "error": str(e)}
    
    except json.JSONDecodeError as e:
        print(f"❌ Know Your Rights Query: FAILED (JSON Error: {e})")
        return {"status": "failed", "error": f"Invalid JSON response: {e}"}

def test_model_endpoint_health() -> Dict[str, Any]:
    """Test if the underlying model endpoint is healthy."""
    
    print("\n🤖 Testing Model Endpoint Health...")
    
    # Test with minimal query
    minimal_request = {
        "scenario": "other",
        "text": "What are my basic constitutional rights?",
        "language": "en"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/api/know-your-rights/query",
            json=minimal_request,
            timeout=TEST_TIMEOUT
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if response contains constitutional content
            legal_advice = data.get("legal_advice", "").lower()
            constitutional_keywords = ["constitution", "article", "fundamental rights", "constitutional"]
            
            has_constitutional_content = any(keyword in legal_advice for keyword in constitutional_keywords)
            
            if has_constitutional_content:
                print("✅ Model Response Quality: GOOD (Contains constitutional content)")
                return {"status": "success", "response_time": response_time, "quality": "good"}
            else:
                print("⚠️ Model Response Quality: POOR (Limited constitutional content)")
                return {"status": "partial", "response_time": response_time, "quality": "poor"}
        
        else:
            print(f"❌ Model Health Check: FAILED (Status: {response.status_code})")
            return {"status": "failed", "error": f"HTTP {response.status_code}"}
    
    except Exception as e:
        print(f"❌ Model Health Check: FAILED ({e})")
        return {"status": "failed", "error": str(e)}

def test_response_format_validation() -> Dict[str, Any]:
    """Test that responses follow the expected schema."""
    
    print("\n📋 Testing Response Format Validation...")
    
    test_scenarios = [
        {"scenario": "bribe", "text": "Official demanded money"},
        {"scenario": "threat", "text": "Someone threatened me"},
        {"scenario": "harassment", "text": "Being harassed by neighbor"}
    ]
    
    results = []
    
    for test_case in test_scenarios:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/know-your-rights/query",
                json=test_case,
                timeout=TEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate schema
                validation_result = validate_response_schema(data)
                validation_result["scenario"] = test_case["scenario"]
                results.append(validation_result)
                
                if validation_result["valid"]:
                    print(f"✅ {test_case['scenario']}: Schema VALID")
                else:
                    print(f"❌ {test_case['scenario']}: Schema INVALID - {validation_result['errors']}")
            
            else:
                print(f"❌ {test_case['scenario']}: API FAILED (Status: {response.status_code})")
                results.append({"scenario": test_case["scenario"], "valid": False, "errors": [f"HTTP {response.status_code}"]})
        
        except Exception as e:
            print(f"❌ {test_case['scenario']}: ERROR ({e})")
            results.append({"scenario": test_case["scenario"], "valid": False, "errors": [str(e)]})
    
    valid_count = sum(1 for r in results if r["valid"])
    print(f"\n📊 Schema Validation: {valid_count}/{len(results)} passed")
    
    return {"status": "success" if valid_count == len(results) else "partial", "results": results}

def validate_response_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate response against expected schema."""
    
    errors = []
    
    # Required fields
    required_fields = {
        "legal_advice": str,
        "citations": list,
        "recommended_actions": list,
        "urgency": str,
        "follow_up_questions": list,
        "disclaimer": str,
        "source_docs": list
    }
    
    for field, expected_type in required_fields.items():
        if field not in data:
            errors.append(f"Missing field: {field}")
        elif not isinstance(data[field], expected_type):
            errors.append(f"Field {field} should be {expected_type.__name__}, got {type(data[field]).__name__}")
    
    # Validate urgency values
    if "urgency" in data and data["urgency"] not in ["low", "medium", "high", "emergency"]:
        errors.append(f"Invalid urgency value: {data['urgency']}")
    
    # Validate citations structure
    if "citations" in data and data["citations"]:
        for i, citation in enumerate(data["citations"]):
            if not isinstance(citation, dict):
                errors.append(f"Citation {i} should be a dict")
            elif "type" not in citation or "reference" not in citation:
                errors.append(f"Citation {i} missing required fields")
    
    # Check for disclaimer presence
    if "disclaimer" in data and not data["disclaimer"]:
        errors.append("Disclaimer is empty")
    
    return {"valid": len(errors) == 0, "errors": errors}

def test_environment_variables() -> Dict[str, Any]:
    """Test that required environment variables are set."""
    
    print("\n🔧 Testing Environment Variables...")
    
    # These are the env vars that might be used
    optional_env_vars = [
        "OPENROUTER_API_KEY",
        "DEEPSEEK_API_KEY", 
        "GEMINI_API_KEY",
        "CLAUDE_API_KEY"
    ]
    
    found_vars = []
    missing_vars = []
    
    for var in optional_env_vars:
        if os.getenv(var):
            found_vars.append(var)
            print(f"✅ {var}: SET")
        else:
            missing_vars.append(var)
            print(f"⚠️ {var}: NOT SET")
    
    if found_vars:
        print(f"\n✅ Environment: {len(found_vars)} API keys configured")
        return {"status": "success", "found": found_vars, "missing": missing_vars}
    else:
        print("\n⚠️ Environment: No API keys found (using mock/fallback mode)")
        return {"status": "warning", "found": found_vars, "missing": missing_vars}

def run_comprehensive_check() -> Dict[str, Any]:
    """Run comprehensive model connectivity and validation checks."""
    
    print("🚀 Starting Comprehensive MCP Check for Know Your Rights")
    print("=" * 60)
    
    start_time = time.time()
    
    # Run all tests
    test_results = {
        "timestamp": time.time(),
        "api_connectivity": test_api_connectivity(),
        "environment": test_environment_variables(),
        "endpoint_test": test_know_your_rights_endpoint(),
        "model_health": test_model_endpoint_health(),
        "schema_validation": test_response_format_validation()
    }
    
    total_time = time.time() - start_time
    
    # Calculate overall status
    test_statuses = [result.get("status", "failed") for result in test_results.values()]
    failed_tests = [name for name, result in test_results.items() if result.get("status") == "failed"]
    
    if not failed_tests:
        overall_status = "success"
        print("\n🎉 Overall Status: ALL TESTS PASSED")
    elif len(failed_tests) < len(test_statuses) / 2:
        overall_status = "partial"
        print(f"\n⚠️ Overall Status: PARTIAL SUCCESS ({len(failed_tests)} failures)")
    else:
        overall_status = "failed"
        print(f"\n❌ Overall Status: MULTIPLE FAILURES ({len(failed_tests)} failures)")
    
    test_results["overall_status"] = overall_status
    test_results["total_time"] = total_time
    test_results["failed_tests"] = failed_tests
    
    print(f"\n⏱️ Total Check Time: {total_time:.2f}s")
    
    return test_results

def save_results(results: Dict[str, Any], filename: str = "mcp_results.json"):
    """Save test results to file."""
    
    results_path = Path(__file__).parent / filename
    
    try:
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {results_path}")
    except Exception as e:
        print(f"\n❌ Failed to save results: {e}")

if __name__ == "__main__":
    print("Know Your Rights - Model Connectivity & Validation Check")
    print("========================================================")
    
    # Run comprehensive check
    results = run_comprehensive_check()
    
    # Save results
    save_results(results)
    
    # Exit with appropriate code
    if results["overall_status"] == "success":
        print("\n✅ MCP Check: PASSED")
        sys.exit(0)
    elif results["overall_status"] == "partial":
        print("\n⚠️ MCP Check: PARTIAL (Some issues detected)")
        sys.exit(1)
    else:
        print("\n❌ MCP Check: FAILED")
        sys.exit(2)