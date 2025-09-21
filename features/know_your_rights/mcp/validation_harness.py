"""
Validation Harness for Know Your Rights
=======================================

This script validates model outputs against expected criteria and provides
feedback for fine-tuning the prompt templates and response quality.
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@dataclass
class ValidationCriteria:
    """Criteria for validating Know Your Rights responses."""
    has_citations: bool = True
    has_disclaimer: bool = True
    non_empty_advice: bool = True
    valid_urgency: bool = True
    has_actions: bool = True
    has_follow_ups: bool = True
    contains_constitutional_content: bool = True
    appropriate_length: bool = True

@dataclass 
class ValidationResult:
    """Result of validating a single response."""
    test_id: str
    scenario: str
    prompt: str
    response: Optional[Dict[str, Any]]
    criteria_met: Dict[str, bool]
    score: float
    notes: List[str]
    response_time: float
    error: Optional[str] = None

class KnowYourRightsValidator:
    """Validates Know Your Rights responses against quality criteria."""
    
    def __init__(self, api_base_url: str = API_BASE_URL):
        self.api_base_url = api_base_url
        self.results: List[ValidationResult] = []
        
        # Load test prompts
        self.test_prompts = self._load_test_prompts()
    
    def _load_test_prompts(self) -> List[Dict[str, str]]:
        """Load curated test prompts for validation."""
        
        return [
            {
                "id": "bribe_police_traffic",
                "scenario": "bribe",
                "text": "A traffic police officer stopped me and demanded Rs. 500 to avoid writing a challan for speeding. He said if I don't pay, he'll make the fine much higher. What are my rights in this situation?",
                "expected_elements": ["Article 21", "corruption", "Prevention of Corruption Act", "complaint mechanism"]
            },
            {
                "id": "threat_neighbor_property",
                "scenario": "threat", 
                "text": "My neighbor is threatening to harm me and my family because of a property dispute. He said he knows people who can make us disappear. I'm scared for our safety.",
                "expected_elements": ["Article 21", "criminal intimidation", "police protection", "emergency"]
            },
            {
                "id": "harassment_workplace_gender",
                "scenario": "harassment",
                "text": "My supervisor at work has been making inappropriate comments about my appearance and asking me to go out with him. When I refused, he started giving me impossible deadlines and poor performance reviews.",
                "expected_elements": ["Article 21", "dignity", "Sexual Harassment Act", "internal committee"]
            },
            {
                "id": "online_harassment_social_media",
                "scenario": "online_harassment",
                "text": "Someone is posting my personal photos on social media with vulgar comments and sharing my phone number. Multiple people are now calling me with inappropriate messages.",
                "expected_elements": ["Article 21", "privacy", "IT Act", "cyber crime", "digital evidence"]
            },
            {
                "id": "workplace_discrimination_caste",
                "scenario": "workplace",
                "text": "My colleagues constantly make jokes about my caste background and exclude me from team activities. The manager said people like me should be grateful to have this job.",
                "expected_elements": ["Article 15", "Article 17", "equality", "discrimination", "SC/ST Act"]
            },
            {
                "id": "bribe_government_office",
                "scenario": "bribe",
                "text": "I need to get a caste certificate from the government office. The clerk told me it will take 6 months unless I pay Rs. 2000 under the table to get it in a week.",
                "expected_elements": ["corruption", "Prevention of Corruption Act", "RTI", "grievance redressal"]
            },
            {
                "id": "threat_landlord_eviction",
                "scenario": "threat",
                "text": "My landlord is threatening to cut off electricity and water if I don't vacate the house immediately, even though my rent agreement has 6 months remaining.",
                "expected_elements": ["Article 21", "right to shelter", "tenant rights", "civil remedy"]
            },
            {
                "id": "harassment_public_transport",
                "scenario": "harassment", 
                "text": "Every day while traveling on the bus, some men follow me and make inappropriate gestures. The conductor doesn't help and sometimes joins in their behavior.",
                "expected_elements": ["Article 21", "dignity", "public space safety", "women safety"]
            }
        ]
    
    def run_validation(self, save_results: bool = True) -> Dict[str, Any]:
        """Run validation on all test prompts."""
        
        print("🧪 Starting Know Your Rights Validation")
        print("=" * 50)
        
        start_time = time.time()
        
        for test_prompt in self.test_prompts:
            print(f"\n🔍 Testing: {test_prompt['id']}")
            result = self._validate_single_prompt(test_prompt)
            self.results.append(result)
            
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print(f"📊 Score: {result.score:.2f} ({result.response_time:.2f}s)")
        
        total_time = time.time() - start_time
        
        # Calculate overall metrics
        metrics = self._calculate_metrics()
        metrics["total_time"] = total_time
        
        print(f"\n📈 Validation Summary:")
        print(f"   Total Tests: {metrics['total_tests']}")
        print(f"   Pass Rate: {metrics['pass_rate']:.1%}")
        print(f"   Average Score: {metrics['average_score']:.2f}")
        print(f"   Total Time: {total_time:.2f}s")
        
        if save_results:
            self._save_results(metrics)
        
        return metrics
    
    def _validate_single_prompt(self, test_prompt: Dict[str, str]) -> ValidationResult:
        """Validate a single test prompt."""
        
        request_data = {
            "scenario": test_prompt["scenario"],
            "text": test_prompt["text"],
            "language": "en"
        }
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.api_base_url}/api/know-your-rights/query",
                json=request_data,
                timeout=60,
                headers={"Content-Type": "application/json"}
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                criteria_met, score, notes = self._evaluate_response(data, test_prompt)
                
                return ValidationResult(
                    test_id=test_prompt["id"],
                    scenario=test_prompt["scenario"],
                    prompt=test_prompt["text"],
                    response=data,
                    criteria_met=criteria_met,
                    score=score,
                    notes=notes,
                    response_time=response_time
                )
            else:
                return ValidationResult(
                    test_id=test_prompt["id"],
                    scenario=test_prompt["scenario"],
                    prompt=test_prompt["text"],
                    response=None,
                    criteria_met={},
                    score=0.0,
                    notes=[f"API Error: HTTP {response.status_code}"],
                    response_time=response_time,
                    error=f"HTTP {response.status_code}"
                )
        
        except Exception as e:
            response_time = time.time() - start_time
            return ValidationResult(
                test_id=test_prompt["id"],
                scenario=test_prompt["scenario"],
                prompt=test_prompt["text"],
                response=None,
                criteria_met={},
                score=0.0,
                notes=[f"Exception: {str(e)}"],
                response_time=response_time,
                error=str(e)
            )
    
    def _evaluate_response(self, response: Dict[str, Any], test_prompt: Dict[str, str]) -> tuple:
        """Evaluate response against validation criteria."""
        
        criteria_met = {}
        notes = []
        
        # Check basic schema requirements
        criteria_met["has_citations"] = bool(response.get("citations"))
        if not criteria_met["has_citations"]:
            notes.append("Missing citations")
        
        criteria_met["has_disclaimer"] = bool(response.get("disclaimer"))
        if not criteria_met["has_disclaimer"]:
            notes.append("Missing disclaimer")
        
        criteria_met["non_empty_advice"] = bool(response.get("legal_advice", "").strip())
        if not criteria_met["non_empty_advice"]:
            notes.append("Empty legal advice")
        
        criteria_met["valid_urgency"] = response.get("urgency") in ["low", "medium", "high", "emergency"]
        if not criteria_met["valid_urgency"]:
            notes.append(f"Invalid urgency: {response.get('urgency')}")
        
        criteria_met["has_actions"] = bool(response.get("recommended_actions"))
        if not criteria_met["has_actions"]:
            notes.append("Missing recommended actions")
        
        criteria_met["has_follow_ups"] = bool(response.get("follow_up_questions"))
        if not criteria_met["has_follow_ups"]:
            notes.append("Missing follow-up questions")
        
        # Check content quality
        legal_advice = response.get("legal_advice", "").lower()
        
        # Constitutional content check
        constitutional_keywords = ["constitution", "article", "fundamental rights", "constitutional"]
        criteria_met["contains_constitutional_content"] = any(kw in legal_advice for kw in constitutional_keywords)
        if not criteria_met["contains_constitutional_content"]:
            notes.append("Limited constitutional content")
        
        # Length check (should be substantial but not too verbose)
        advice_length = len(response.get("legal_advice", ""))
        criteria_met["appropriate_length"] = 200 <= advice_length <= 2000
        if not criteria_met["appropriate_length"]:
            notes.append(f"Inappropriate length: {advice_length} chars")
        
        # Check for expected elements specific to the test
        expected_elements = test_prompt.get("expected_elements", [])
        found_elements = []
        
        response_text = (response.get("legal_advice", "") + " " + 
                        str(response.get("citations", ""))).lower()
        
        for element in expected_elements:
            if element.lower() in response_text:
                found_elements.append(element)
        
        criteria_met["expected_elements"] = len(found_elements) / max(len(expected_elements), 1)
        
        if found_elements:
            notes.append(f"Found elements: {found_elements}")
        if len(found_elements) < len(expected_elements):
            missing = [e for e in expected_elements if e not in found_elements]
            notes.append(f"Missing elements: {missing}")
        
        # Calculate score
        basic_criteria = ["has_citations", "has_disclaimer", "non_empty_advice", "valid_urgency", "has_actions", "has_follow_ups"]
        quality_criteria = ["contains_constitutional_content", "appropriate_length"]
        
        basic_score = sum(criteria_met.get(c, False) for c in basic_criteria) / len(basic_criteria)
        quality_score = sum(criteria_met.get(c, False) for c in quality_criteria) / len(quality_criteria)
        element_score = criteria_met.get("expected_elements", 0)
        
        # Weighted score: 40% basic, 30% quality, 30% expected elements
        final_score = (basic_score * 0.4) + (quality_score * 0.3) + (element_score * 0.3)
        
        return criteria_met, final_score, notes
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate overall validation metrics."""
        
        total_tests = len(self.results)
        successful_tests = [r for r in self.results if r.error is None]
        
        if not successful_tests:
            return {
                "total_tests": total_tests,
                "successful_tests": 0,
                "pass_rate": 0.0,
                "average_score": 0.0,
                "passing_tests": 0,
                "failing_tests": total_tests,
                "errors": len(self.results)
            }
        
        scores = [r.score for r in successful_tests]
        average_score = sum(scores) / len(scores)
        
        # Pass threshold: 0.7 (70%)
        passing_tests = [r for r in successful_tests if r.score >= 0.7]
        pass_rate = len(passing_tests) / total_tests
        
        # Scenario analysis
        scenario_performance = {}
        for result in successful_tests:
            scenario = result.scenario
            if scenario not in scenario_performance:
                scenario_performance[scenario] = []
            scenario_performance[scenario].append(result.score)
        
        scenario_averages = {
            scenario: sum(scores) / len(scores)
            for scenario, scores in scenario_performance.items()
        }
        
        return {
            "total_tests": total_tests,
            "successful_tests": len(successful_tests),
            "pass_rate": pass_rate,
            "average_score": average_score,
            "passing_tests": len(passing_tests),
            "failing_tests": total_tests - len(passing_tests),
            "errors": total_tests - len(successful_tests),
            "scenario_performance": scenario_averages,
            "detailed_results": [
                {
                    "test_id": r.test_id,
                    "scenario": r.scenario,
                    "score": r.score,
                    "criteria_met": r.criteria_met,
                    "notes": r.notes,
                    "response_time": r.response_time,
                    "error": r.error
                }
                for r in self.results
            ]
        }
    
    def _save_results(self, metrics: Dict[str, Any]):
        """Save validation results to file."""
        
        results_file = Path(__file__).parent / "results.json"
        
        try:
            with open(results_file, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
            print(f"\n💾 Results saved to: {results_file}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")
    
    def generate_report(self) -> str:
        """Generate a human-readable validation report."""
        
        if not self.results:
            return "No validation results available."
        
        metrics = self._calculate_metrics()
        
        report = f"""
Know Your Rights Validation Report
==================================

Overall Performance:
- Total Tests: {metrics['total_tests']}
- Pass Rate: {metrics['pass_rate']:.1%}
- Average Score: {metrics['average_score']:.2f}
- Successful Tests: {metrics['successful_tests']}
- Failed Tests: {metrics['failing_tests']}
- Errors: {metrics['errors']}

Scenario Performance:
"""
        
        for scenario, avg_score in metrics.get('scenario_performance', {}).items():
            report += f"- {scenario}: {avg_score:.2f}\n"
        
        report += "\nDetailed Results:\n"
        
        for result in self.results:
            status = "✅ PASS" if result.score >= 0.7 else "❌ FAIL"
            report += f"- {result.test_id} ({result.scenario}): {status} ({result.score:.2f})\n"
            
            if result.notes:
                for note in result.notes[:2]:  # Show first 2 notes
                    report += f"  • {note}\n"
        
        if metrics['pass_rate'] < 0.9:
            report += f"""
Recommendations:
- Current pass rate ({metrics['pass_rate']:.1%}) is below 90% threshold
- Consider updating prompt templates for failing scenarios
- Review citation extraction and constitutional content coverage
- Check urgency classification logic
"""
        
        return report

def run_validation_suite():
    """Run the complete validation suite."""
    
    print("Know Your Rights - Validation Harness")
    print("=====================================")
    
    validator = KnowYourRightsValidator()
    metrics = validator.run_validation()
    
    print("\n" + validator.generate_report())
    
    # Return appropriate exit code
    if metrics['pass_rate'] >= 0.9:
        print("\n✅ Validation: PASSED (90%+ pass rate)")
        return 0
    elif metrics['pass_rate'] >= 0.7:
        print("\n⚠️ Validation: PARTIAL (70%+ pass rate)")
        return 1
    else:
        print("\n❌ Validation: FAILED (<70% pass rate)")
        return 2

if __name__ == "__main__":
    exit_code = run_validation_suite()
    sys.exit(exit_code)