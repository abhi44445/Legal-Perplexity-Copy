"""
Automated Evaluation Script for Know Your Rights
===============================================

This script runs the golden dataset scenarios against the API and evaluates
response quality, generating detailed reports for fine-tuning.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Any
import csv
from datetime import datetime

# Add project paths
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent / "../docs/golden"))

from golden_dataset import GOLDEN_SCENARIOS, validate_response, calculate_overall_score, PASS_CRITERIA

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

class KnowYourRightsEvaluator:
    """Evaluator for Know Your Rights system using golden dataset."""
    
    def __init__(self, api_base_url: str = API_BASE_URL, save_results: bool = True):
        self.api_base_url = api_base_url
        self.save_results = save_results
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def run_evaluation(self) -> Dict[str, Any]:
        """Run complete evaluation on all golden scenarios."""
        
        print("🧪 Starting Know Your Rights Evaluation")
        print("=" * 60)
        print(f"API Base URL: {self.api_base_url}")
        print(f"Total Scenarios: {len(GOLDEN_SCENARIOS)}")
        print(f"Pass Threshold: {PASS_CRITERIA['overall_pass_threshold']:.1%}")
        print("=" * 60)
        
        self.start_time = time.time()
        
        for i, scenario in enumerate(GOLDEN_SCENARIOS, 1):
            print(f"\n📋 Scenario {i}/{len(GOLDEN_SCENARIOS)}: {scenario['id']}")
            print(f"   Type: {scenario['scenario']}")
            print(f"   Input length: {len(scenario['input'])} chars")
            
            result = self._evaluate_scenario(scenario)
            self.results.append(result)
            
            # Print immediate feedback
            if result['api_error']:
                print(f"   ❌ API Error: {result['api_error']}")
            else:
                print(f"   📊 Score: {result['validation_score']:.2f}")
                print(f"   ⏱️ Response Time: {result['response_time']:.1f}s")
                if result['validation_score'] >= PASS_CRITERIA['overall_pass_threshold']:
                    print(f"   ✅ PASS")
                else:
                    print(f"   ❌ FAIL")
        
        self.end_time = time.time()
        
        # Calculate overall metrics
        overall_metrics = self._calculate_metrics()
        
        # Print summary
        self._print_summary(overall_metrics)
        
        # Save results if requested
        if self.save_results:
            self._save_results(overall_metrics)
        
        return overall_metrics
    
    def _evaluate_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single scenario."""
        
        result = {
            'scenario_id': scenario['id'],
            'scenario_type': scenario['scenario'],
            'input_text': scenario['input'],
            'expected_checks': scenario['expected_checks'],
            'api_response': None,
            'api_error': None,
            'response_time': 0,
            'validation_result': None,
            'validation_score': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Prepare API request
        api_request = {
            "scenario": scenario['scenario'],
            "text": scenario['input'],
            "language": "en"
        }
        
        try:
            # Make API call
            start_time = time.time()
            response = requests.post(
                f"{self.api_base_url}/api/know-your-rights/query",
                json=api_request,
                timeout=120,  # 2 minute timeout
                headers={"Content-Type": "application/json"}
            )
            end_time = time.time()
            
            result['response_time'] = end_time - start_time
            
            if response.status_code == 200:
                api_data = response.json()
                result['api_response'] = api_data
                
                # Validate response against expected criteria
                validation_result = validate_response(api_data, scenario['expected_checks'])
                result['validation_result'] = validation_result
                result['validation_score'] = validation_result['score']
                
            else:
                result['api_error'] = f"HTTP {response.status_code}: {response.text}"
        
        except requests.exceptions.Timeout:
            result['api_error'] = "API timeout (>120s)"
            result['response_time'] = 120
        
        except requests.exceptions.ConnectionError:
            result['api_error'] = "Connection error - API server not available"
        
        except Exception as e:
            result['api_error'] = f"Unexpected error: {str(e)}"
        
        return result
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate overall evaluation metrics."""
        
        # Filter successful API calls
        successful_results = [r for r in self.results if not r['api_error']]
        
        if not successful_results:
            return {
                'overall_pass': False,
                'total_scenarios': len(self.results),
                'successful_api_calls': 0,
                'api_success_rate': 0,
                'average_score': 0,
                'pass_rate': 0,
                'total_time': self.end_time - self.start_time if self.end_time and self.start_time else 0,
                'recommendation': 'SYSTEM_DOWN',
                'detailed_results': self.results
            }
        
        # Calculate scores
        scores = [r['validation_score'] for r in successful_results]
        average_score = sum(scores) / len(scores)
        
        # Calculate pass rate
        passing_results = [r for r in successful_results if r['validation_score'] >= PASS_CRITERIA['overall_pass_threshold']]
        pass_rate = len(passing_results) / len(successful_results)
        
        # Calculate response times
        response_times = [r['response_time'] for r in successful_results]
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        # Check critical failures
        critical_failures = 0
        for result in successful_results:
            if result['validation_result'] and result['validation_result'].get('critical_failures'):
                critical_failures += 1
        
        # Determine overall pass/fail
        overall_pass = (
            len(passing_results) >= PASS_CRITERIA['minimum_scenarios_passing'] and
            critical_failures == 0 and
            average_score >= PASS_CRITERIA['overall_pass_threshold']
        )
        
        # Generate recommendation
        if overall_pass:
            recommendation = "PASS"
        elif average_score >= 0.5 and pass_rate >= 0.5:
            recommendation = "NEEDS_IMPROVEMENT"
        else:
            recommendation = "MAJOR_ISSUES"
        
        # Scenario type analysis
        scenario_performance = {}
        for result in successful_results:
            scenario_type = result['scenario_type']
            if scenario_type not in scenario_performance:
                scenario_performance[scenario_type] = []
            scenario_performance[scenario_type].append(result['validation_score'])
        
        scenario_averages = {
            scenario_type: sum(scores) / len(scores)
            for scenario_type, scores in scenario_performance.items()
        }
        
        return {
            'overall_pass': overall_pass,
            'total_scenarios': len(self.results),
            'successful_api_calls': len(successful_results),
            'api_success_rate': len(successful_results) / len(self.results),
            'average_score': average_score,
            'pass_rate': pass_rate,
            'passing_scenarios': len(passing_results),
            'critical_failures': critical_failures,
            'avg_response_time': avg_response_time,
            'max_response_time': max_response_time,
            'total_time': self.end_time - self.start_time if self.end_time and self.start_time else 0,
            'scenario_performance': scenario_averages,
            'recommendation': recommendation,
            'detailed_results': self.results
        }
    
    def _print_summary(self, metrics: Dict[str, Any]):
        """Print evaluation summary."""
        
        print("\n" + "=" * 60)
        print("📊 EVALUATION SUMMARY")
        print("=" * 60)
        
        print(f"🎯 Overall Result: {metrics['recommendation']}")
        print(f"✅ Pass Status: {'PASS' if metrics['overall_pass'] else 'FAIL'}")
        print(f"📈 Average Score: {metrics['average_score']:.2f}")
        print(f"📊 Pass Rate: {metrics['pass_rate']:.1%} ({metrics['passing_scenarios']}/{metrics['successful_api_calls']})")
        print(f"🔗 API Success Rate: {metrics['api_success_rate']:.1%}")
        print(f"⚠️ Critical Failures: {metrics['critical_failures']}")
        print(f"⏱️ Avg Response Time: {metrics['avg_response_time']:.1f}s")
        print(f"🕐 Total Evaluation Time: {metrics['total_time']:.1f}s")
        
        print(f"\n📋 Scenario Performance:")
        for scenario_type, avg_score in metrics['scenario_performance'].items():
            status = "✅" if avg_score >= PASS_CRITERIA['overall_pass_threshold'] else "❌"
            print(f"   {status} {scenario_type}: {avg_score:.2f}")
        
        # Show failed scenarios
        failed_scenarios = [r for r in self.results if r['validation_score'] < PASS_CRITERIA['overall_pass_threshold']]
        if failed_scenarios:
            print(f"\n❌ Failed Scenarios ({len(failed_scenarios)}):")
            for result in failed_scenarios:
                if result['api_error']:
                    print(f"   • {result['scenario_id']}: API Error - {result['api_error']}")
                else:
                    print(f"   • {result['scenario_id']}: Score {result['validation_score']:.2f}")
                    if result['validation_result']:
                        for failure in result['validation_result']['failed_checks'][:2]:
                            print(f"     - {failure}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if metrics['recommendation'] == 'PASS':
            print("   ✅ System performing well! Consider monitoring for regressions.")
        elif metrics['recommendation'] == 'NEEDS_IMPROVEMENT':
            print("   🔧 Review failed scenarios and update prompt templates.")
            print("   📚 Consider expanding training data for weak scenario types.")
        else:
            print("   🚨 Major issues detected! Review system architecture.")
            print("   🛠️ Check model connectivity and retrieval pipeline.")
    
    def _save_results(self, metrics: Dict[str, Any]):
        """Save evaluation results to files."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path(__file__).parent / "results"
        results_dir.mkdir(exist_ok=True)
        
        # Save JSON results
        json_file = results_dir / f"evaluation_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        
        # Save CSV summary
        csv_file = results_dir / f"evaluation_summary_{timestamp}.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Scenario ID', 'Type', 'Score', 'Pass', 'Response Time', 'Error'])
            
            for result in self.results:
                writer.writerow([
                    result['scenario_id'],
                    result['scenario_type'],
                    result['validation_score'],
                    'PASS' if result['validation_score'] >= PASS_CRITERIA['overall_pass_threshold'] else 'FAIL',
                    f"{result['response_time']:.1f}s",
                    result['api_error'] or ''
                ])
        
        # Update the standard results.json file for validation harness compatibility
        standard_results_file = Path(__file__).parent / "results.json"
        with open(standard_results_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        
        print(f"\n💾 Results saved:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📊 CSV: {csv_file}")
        print(f"   🔄 Standard: {standard_results_file}")
    
    def generate_fine_tuning_report(self) -> str:
        """Generate a report for fine-tuning recommendations."""
        
        if not self.results:
            return "No evaluation results available."
        
        report = []
        report.append("# Know Your Rights - Fine-tuning Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall performance
        successful_results = [r for r in self.results if not r['api_error']]
        if not successful_results:
            report.append("## Critical Issue: No successful API responses")
            return "\n".join(report)
        
        average_score = sum(r['validation_score'] for r in successful_results) / len(successful_results)
        pass_rate = len([r for r in successful_results if r['validation_score'] >= 0.7]) / len(successful_results)
        
        report.append(f"## Overall Performance")
        report.append(f"- Average Score: {average_score:.2f}")
        report.append(f"- Pass Rate: {pass_rate:.1%}")
        report.append(f"- Status: {'PASS' if pass_rate >= 0.75 else 'NEEDS IMPROVEMENT'}")
        report.append("")
        
        # Common failure patterns
        report.append("## Common Issues")
        all_failures = []
        for result in successful_results:
            if result['validation_result']:
                all_failures.extend(result['validation_result']['failed_checks'])
        
        from collections import Counter
        failure_counts = Counter(all_failures)
        
        for failure, count in failure_counts.most_common(5):
            report.append(f"- {failure} ({count} scenarios)")
        report.append("")
        
        # Scenario-specific recommendations
        report.append("## Scenario-Specific Recommendations")
        
        scenario_performance = {}
        for result in successful_results:
            scenario_type = result['scenario_type']
            if scenario_type not in scenario_performance:
                scenario_performance[scenario_type] = []
            scenario_performance[scenario_type].append(result)
        
        for scenario_type, results in scenario_performance.items():
            avg_score = sum(r['validation_score'] for r in results) / len(results)
            report.append(f"### {scenario_type.title()} Scenarios (Score: {avg_score:.2f})")
            
            if avg_score < 0.7:
                # Find most common failures for this scenario type
                failures = []
                for result in results:
                    if result['validation_result']:
                        failures.extend(result['validation_result']['failed_checks'])
                
                common_failures = Counter(failures).most_common(3)
                report.append("**Issues:**")
                for failure, _ in common_failures:
                    report.append(f"- {failure}")
                
                report.append("**Recommended Actions:**")
                if "missing constitutional content" in str(common_failures).lower():
                    report.append("- Update prompt template to emphasize constitutional analysis")
                if "missing legal content" in str(common_failures).lower():
                    report.append("- Add more specific legal provisions to prompt template")
                if "no citations" in str(common_failures).lower():
                    report.append("- Improve citation extraction regex patterns")
                if "incorrect urgency" in str(common_failures).lower():
                    report.append("- Review urgency classification keywords and logic")
            else:
                report.append("✅ Performing well")
            
            report.append("")
        
        return "\n".join(report)

def main():
    """Main evaluation function."""
    
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate Know Your Rights system")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to files")
    parser.add_argument("--report", action="store_true", help="Generate fine-tuning report")
    
    args = parser.parse_args()
    
    evaluator = KnowYourRightsEvaluator(
        api_base_url=args.api_url,
        save_results=not args.no_save
    )
    
    try:
        metrics = evaluator.run_evaluation()
        
        if args.report:
            print("\n" + "="*60)
            print("📝 FINE-TUNING REPORT")
            print("="*60)
            print(evaluator.generate_fine_tuning_report())
        
        # Return appropriate exit code
        if metrics['overall_pass']:
            print(f"\n🎉 EVALUATION PASSED!")
            exit_code = 0
        elif metrics['recommendation'] == 'NEEDS_IMPROVEMENT':
            print(f"\n⚠️ EVALUATION: NEEDS IMPROVEMENT")
            exit_code = 1
        else:
            print(f"\n❌ EVALUATION FAILED!")
            exit_code = 2
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Evaluation interrupted by user")
        sys.exit(3)
    except Exception as e:
        print(f"\n💥 Evaluation failed with error: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()