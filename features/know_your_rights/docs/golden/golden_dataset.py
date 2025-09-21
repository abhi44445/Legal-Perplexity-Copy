"""
Golden Dataset for Know Your Rights Evaluation
==============================================

This file contains curated test scenarios with expected validation criteria
for evaluating the Know Your Rights system performance.
"""

GOLDEN_SCENARIOS = [
    {
        "id": "bribe_police_traffic_detailed",
        "scenario": "bribe",
        "input": "A traffic police officer stopped me and my friend at a checkpoint near MG Road on September 20th, 2025, around 3 PM. He said we were speeding and that the fine would be Rs.500, but if we paid him Rs.100 right now, he would let us go without any paperwork. When I said I'd prefer to pay the official fine, he said it would actually become Rs.1000 and we'd have to go to court. My friend was scared and wanted to pay, but I felt this was wrong.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "fundamental rights", "constitution"],
            "must_contain_legal": ["corruption", "Prevention of Corruption Act", "bribe"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["medium", "high"],
            "must_contain_actions": ["document_incident", "contact_authorities"],
            "must_have_disclaimer": True,
            "min_response_length": 200,
            "max_response_length": 2000,
            "must_be_specific": True  # Should reference details from user input
        },
        "validation_notes": "Response should address police corruption specifically and provide constitutional foundation"
    },
    
    {
        "id": "threat_neighbor_property_dispute",
        "scenario": "threat",
        "input": "My neighbor Mr. Sharma has been threatening me and my family over a property boundary dispute. Yesterday he told me 'You and your family will face serious consequences if you don't move that fence.' He also said he knows people who can 'make problems disappear' and that I should be worried about my children's safety when they walk to school. I'm really scared and don't know what to do.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "right to life", "personal liberty"],
            "must_contain_legal": ["criminal intimidation", "threat", "IPC", "police"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["high", "emergency"],
            "must_contain_actions": ["call_police", "document_incident"],
            "must_have_disclaimer": True,
            "min_response_length": 200,
            "should_mention_emergency": True,
            "must_be_specific": True
        },
        "validation_notes": "Should treat as high/emergency priority due to family safety threats"
    },
    
    {
        "id": "harassment_workplace_gender",
        "scenario": "harassment",
        "input": "I work at a software company where my team leader has been making inappropriate comments about my appearance and asking personal questions about my relationships. When I ignored him, he started giving me impossible deadlines and criticizing my work in front of everyone. He also hinted that my appraisal depends on being 'more friendly' with him. I need this job but this is affecting my mental health.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "dignity", "equality"],
            "must_contain_legal": ["Sexual Harassment", "workplace", "POSH Act", "internal committee"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["medium", "high"],
            "must_contain_actions": ["document_incident", "legal_aid"],
            "must_have_disclaimer": True,
            "should_mention_workplace_mechanisms": True,
            "must_be_specific": True
        },
        "validation_notes": "Should address workplace sexual harassment laws and internal mechanisms"
    },
    
    {
        "id": "online_harassment_doxxing",
        "scenario": "online_harassment",
        "input": "Someone has posted my personal photos and phone number on Instagram and Facebook with vulgar comments. They created fake profiles claiming to be me and are sending friend requests to my colleagues and family members. I'm getting calls from unknown numbers with inappropriate messages. They also shared my home address saying 'come visit her, she's easy.' I'm scared to leave my house.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "privacy", "dignity"],
            "must_contain_legal": ["IT Act", "cyber crime", "privacy violation"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["high", "emergency"],
            "must_contain_actions": ["block_report", "call_police", "collect_evidence"],
            "must_have_disclaimer": True,
            "should_mention_digital_evidence": True,
            "must_be_specific": True
        },
        "validation_notes": "Should address cyber harassment and digital evidence preservation"
    },
    
    {
        "id": "workplace_caste_discrimination", 
        "scenario": "workplace",
        "input": "At my government office job, my colleagues constantly make jokes about my caste background during lunch breaks. They say things like 'people like you should be grateful for this opportunity' and exclude me from team activities. My supervisor assigned me to clean toilets saying it's 'appropriate work for your community' even though I'm a trained accountant. When I complained to HR, they said I'm being 'too sensitive' and should 'adjust to the culture.'",
        "expected_checks": {
            "must_contain_constitutional": ["Article 15", "Article 17", "equality", "non-discrimination"],
            "must_contain_legal": ["SC/ST Act", "discrimination", "caste"],
            "must_have_citations": True,
            "min_citations": 2,
            "urgency_level": ["medium", "high"],
            "must_contain_actions": ["legal_aid", "document_incident", "contact_authorities"],
            "must_have_disclaimer": True,
            "should_address_caste_discrimination": True,
            "must_be_specific": True
        },
        "validation_notes": "Should specifically address caste-based discrimination and constitutional remedies"
    },
    
    {
        "id": "bribe_government_certificate",
        "scenario": "bribe",
        "input": "I went to the tehsil office to get my caste certificate which should be issued free under government rules. The clerk told me it will take 6 months through normal process, but if I pay Rs.2000 'speed money' it can be done in one week. He said everyone pays this and it's 'normal procedure.' I need this certificate urgently for my daughter's college admission but I don't want to pay a bribe.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "fundamental rights"],
            "must_contain_legal": ["corruption", "Prevention of Corruption Act", "public servant"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["medium"],
            "must_contain_actions": ["contact_authorities", "document_incident"],
            "must_have_disclaimer": True,
            "should_mention_grievance_mechanisms": True,
            "must_be_specific": True
        },
        "validation_notes": "Should address corruption in government services and grievance redressal"
    },
    
    {
        "id": "threat_landlord_illegal_eviction",
        "scenario": "threat",
        "input": "My landlord wants me to vacate my rented apartment immediately because he wants to sell it, even though my lease agreement is valid for 8 more months. He has started cutting off electricity and water supply during the day and threatened to throw my belongings out if I don't leave by this weekend. He also brought some men who said they will 'make life difficult' if I stay. I have nowhere else to go with my family.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "right to shelter", "personal liberty"],
            "must_contain_legal": ["tenant rights", "illegal eviction", "criminal intimidation"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["high"],
            "must_contain_actions": ["legal_aid", "call_police", "document_incident"],
            "must_have_disclaimer": True,
            "should_address_housing_rights": True,
            "must_be_specific": True
        },
        "validation_notes": "Should address tenant rights and illegal eviction procedures"
    },
    
    {
        "id": "harassment_public_transport",
        "scenario": "harassment",
        "input": "Every day while traveling on the 8 AM bus from Nehru Place to Connaught Place for my job, a group of men sitting in the back seats make inappropriate gestures and comments about my body. The bus conductor has seen this happening but does nothing. Sometimes they deliberately bump into me while getting off. Yesterday one of them followed me for two blocks after I got off the bus. I'm afraid to take public transport but I have no other way to reach my office.",
        "expected_checks": {
            "must_contain_constitutional": ["Article 21", "dignity", "freedom of movement"],
            "must_contain_legal": ["harassment", "public space", "women safety"],
            "must_have_citations": True,
            "min_citations": 1,
            "urgency_level": ["medium", "high"],
            "must_contain_actions": ["call_police", "document_incident", "contact_authorities"],
            "must_have_disclaimer": True,
            "should_address_public_safety": True,
            "must_be_specific": True
        },
        "validation_notes": "Should address harassment in public spaces and women's safety"
    }
]

# Validation criteria explanation
VALIDATION_CRITERIA_EXPLANATION = {
    "must_contain_constitutional": "Response must reference constitutional articles or fundamental rights",
    "must_contain_legal": "Response must include relevant legal provisions or statutes",
    "must_have_citations": "Response must include at least one proper legal citation",
    "min_citations": "Minimum number of citations required",
    "urgency_level": "Acceptable urgency classifications for this scenario",
    "must_contain_actions": "Specific actions that must be recommended",
    "must_have_disclaimer": "Must include legal disclaimer",
    "min_response_length": "Minimum response length in characters",
    "max_response_length": "Maximum response length in characters", 
    "must_be_specific": "Response should reference specific details from user input",
    "should_mention_emergency": "Should indicate emergency nature if applicable",
    "should_mention_workplace_mechanisms": "Should address internal workplace grievance mechanisms",
    "should_mention_digital_evidence": "Should advise on preserving digital evidence",
    "should_address_caste_discrimination": "Should specifically address caste-based discrimination",
    "should_mention_grievance_mechanisms": "Should mention government grievance redressal mechanisms",
    "should_address_housing_rights": "Should address constitutional right to shelter",
    "should_address_public_safety": "Should address public safety and women's rights in public spaces"
}

# Pass criteria thresholds
PASS_CRITERIA = {
    "overall_pass_threshold": 0.70,  # 70% of checks must pass
    "critical_checks": [
        "must_have_citations",
        "must_have_disclaimer", 
        "must_contain_constitutional"
    ],  # These checks must always pass
    "response_time_threshold": 120,  # Maximum 2 minutes response time
    "minimum_scenarios_passing": 6  # At least 6 out of 8 scenarios must pass
}

def validate_response(response_data: dict, expected_checks: dict) -> dict:
    """
    Validate a Know Your Rights response against expected criteria.
    
    Args:
        response_data: The API response data
        expected_checks: Expected criteria from golden dataset
        
    Returns:
        Dictionary with validation results
    """
    results = {
        "passed_checks": [],
        "failed_checks": [],
        "score": 0.0,
        "critical_failures": []
    }
    
    legal_advice = response_data.get("legal_advice", "").lower()
    citations = response_data.get("citations", [])
    recommended_actions = response_data.get("recommended_actions", [])
    urgency = response_data.get("urgency", "")
    disclaimer = response_data.get("disclaimer", "")
    
    total_checks = 0
    passed_checks = 0
    
    # Check constitutional content
    if "must_contain_constitutional" in expected_checks:
        total_checks += 1
        required_terms = expected_checks["must_contain_constitutional"]
        if any(term.lower() in legal_advice for term in required_terms):
            results["passed_checks"].append("constitutional_content")
            passed_checks += 1
        else:
            results["failed_checks"].append(f"Missing constitutional content: {required_terms}")
    
    # Check legal content
    if "must_contain_legal" in expected_checks:
        total_checks += 1
        required_terms = expected_checks["must_contain_legal"]
        if any(term.lower() in legal_advice for term in required_terms):
            results["passed_checks"].append("legal_content")
            passed_checks += 1
        else:
            results["failed_checks"].append(f"Missing legal content: {required_terms}")
    
    # Check citations
    if expected_checks.get("must_have_citations", False):
        total_checks += 1
        if citations and len(citations) > 0:
            results["passed_checks"].append("has_citations")
            passed_checks += 1
        else:
            results["failed_checks"].append("No citations provided")
            if "must_have_citations" in PASS_CRITERIA["critical_checks"]:
                results["critical_failures"].append("no_citations")
    
    # Check minimum citations
    if "min_citations" in expected_checks:
        total_checks += 1
        min_required = expected_checks["min_citations"]
        if len(citations) >= min_required:
            results["passed_checks"].append("sufficient_citations")
            passed_checks += 1
        else:
            results["failed_checks"].append(f"Only {len(citations)} citations, need {min_required}")
    
    # Check urgency level
    if "urgency_level" in expected_checks:
        total_checks += 1
        acceptable_levels = expected_checks["urgency_level"]
        if urgency in acceptable_levels:
            results["passed_checks"].append("correct_urgency")
            passed_checks += 1
        else:
            results["failed_checks"].append(f"Urgency '{urgency}' not in {acceptable_levels}")
    
    # Check required actions
    if "must_contain_actions" in expected_checks:
        total_checks += 1
        required_actions = expected_checks["must_contain_actions"]
        if all(action in recommended_actions for action in required_actions):
            results["passed_checks"].append("required_actions")
            passed_checks += 1
        else:
            missing = [a for a in required_actions if a not in recommended_actions]
            results["failed_checks"].append(f"Missing actions: {missing}")
    
    # Check disclaimer
    if expected_checks.get("must_have_disclaimer", False):
        total_checks += 1
        if disclaimer and "not legal advice" in disclaimer.lower():
            results["passed_checks"].append("has_disclaimer")
            passed_checks += 1
        else:
            results["failed_checks"].append("Missing or invalid disclaimer")
            if "must_have_disclaimer" in PASS_CRITERIA["critical_checks"]:
                results["critical_failures"].append("no_disclaimer")
    
    # Check response length
    if "min_response_length" in expected_checks:
        total_checks += 1
        min_length = expected_checks["min_response_length"]
        if len(response_data.get("legal_advice", "")) >= min_length:
            results["passed_checks"].append("sufficient_length")
            passed_checks += 1
        else:
            results["failed_checks"].append(f"Response too short: {len(response_data.get('legal_advice', ''))} < {min_length}")
    
    if "max_response_length" in expected_checks:
        total_checks += 1
        max_length = expected_checks["max_response_length"]
        if len(response_data.get("legal_advice", "")) <= max_length:
            results["passed_checks"].append("appropriate_length")
            passed_checks += 1
        else:
            results["failed_checks"].append(f"Response too long: {len(response_data.get('legal_advice', ''))} > {max_length}")
    
    # Calculate score
    if total_checks > 0:
        results["score"] = passed_checks / total_checks
    
    return results

def calculate_overall_score(all_results: list) -> dict:
    """Calculate overall evaluation score across all scenarios."""
    
    total_scenarios = len(all_results)
    passing_scenarios = sum(1 for r in all_results if r["score"] >= PASS_CRITERIA["overall_pass_threshold"])
    
    average_score = sum(r["score"] for r in all_results) / total_scenarios if total_scenarios > 0 else 0
    
    critical_failures = sum(1 for r in all_results if r.get("critical_failures"))
    
    overall_pass = (
        passing_scenarios >= PASS_CRITERIA["minimum_scenarios_passing"] and
        critical_failures == 0 and
        average_score >= PASS_CRITERIA["overall_pass_threshold"]
    )
    
    return {
        "overall_pass": overall_pass,
        "average_score": average_score,
        "passing_scenarios": passing_scenarios,
        "total_scenarios": total_scenarios,
        "pass_rate": passing_scenarios / total_scenarios,
        "critical_failures": critical_failures,
        "recommendation": (
            "PASS" if overall_pass else 
            "NEEDS_IMPROVEMENT" if average_score >= 0.5 else 
            "MAJOR_ISSUES"
        )
    }