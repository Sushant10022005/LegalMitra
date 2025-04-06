"""
Case Outcome Predictor Analyzer

This module provides functionality for analyzing case details and predicting outcomes
using the Gemini API with Indian Kanoon data.
"""

import json
import os
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv
import google.generativeai as genai
from ..api_handler import get_gemini_response
from .indian_kanoon import IndianKanoonDataHandler

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Indian Kanoon data handler
indian_kanoon_handler = IndianKanoonDataHandler()

def analyze_case_outcome(case_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze case details and predict the outcome using Gemini API with Indian Kanoon data.
    
    Args:
        case_details: Dictionary containing case information
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Get relevant laws from Indian Kanoon
        case_type = case_details.get("case_type", "")
        relevant_laws = indian_kanoon_handler.get_relevant_laws(case_type)
        
        # Get similar cases from Indian Kanoon
        similar_cases = indian_kanoon_handler.get_similar_cases(case_details)
        
        # Format case details for the prompt
        formatted_case = f"""
Case Type: {case_details.get('case_type', 'Not specified')}
Jurisdiction/Court: {case_details.get('jurisdiction', 'Not specified')}
Accuser/Plaintiff: {case_details.get('accuser', 'Not specified')}
Accused/Defendant: {case_details.get('accused', 'Not specified')}
Victim (if different from accuser): {case_details.get('victim', 'Not specified')}
Case Description: {case_details.get('case_description', 'Not provided')}
Timeline of Events: {case_details.get('timeline', 'Not provided')}
Evidence: {case_details.get('evidence', 'Not provided')}
Previous Legal History: {case_details.get('previous_legal_history', 'Not provided')}
"""

        # Format relevant laws for the prompt
        laws_text = "Relevant Indian Laws:\n"
        for law in relevant_laws:
            laws_text += f"- {law['name']}: {law['description']}\n"
        
        # Format similar cases for the prompt
        cases_text = "Similar Cases:\n"
        for case in similar_cases:
            cases_text += f"- {case['case_name']} ({case['citation']}): {case['summary']}\n"
        
        # Create the prompt for Gemini
        prompt = f"""
You are a legal expert analyzing a case in the Indian legal system. Please analyze the following case details and provide a structured prediction of the outcome.

{formatted_case}

{laws_text}

{cases_text}

Based ONLY on the provided case details, relevant laws, and similar cases, please provide a structured analysis in the following JSON format:

{{
    "win_probability": <percentage between 0-100>,
    "confidence_score": <percentage between 0-100>,
    "key_factors": [
        "Factor 1",
        "Factor 2",
        ...
    ],
    "strengths": [
        "Strength 1",
        "Strength 2",
        ...
    ],
    "weaknesses": [
        "Weakness 1",
        "Weakness 2",
        ...
    ],
    "legal_arguments": {{
        "plaintiff": [
            "Argument 1",
            "Argument 2",
            ...
        ],
        "defendant": [
            "Argument 1",
            "Argument 2",
            ...
        ]
    }},
    "applicable_laws": [
        {{
            "name": "Law Name",
            "description": "Description of how this law applies to the case",
            "link": "Link to the law on Indian Kanoon"
        }},
        ...
    ],
    "settlement_recommendation": "Recommendation for settlement if win probability is low",
    "similar_cases": [
        {{
            "case_name": "Case Name",
            "outcome": "Outcome of the case",
            "link": "Link to the case on Indian Kanoon"
        }},
        ...
    ]
}}

IMPORTANT: Base your analysis ONLY on the provided case details, relevant laws, and similar cases. Do not make assumptions or include information not provided in these sources.
"""

        # Get response from Gemini
        response_text = get_gemini_response(prompt)
        
        # Parse the response
        try:
            # Try to extract JSON from the response
            json_str = response_text.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            analysis = json.loads(json_str)
            
            # Create a mapping of case names to their links
            case_links = {case['case_name']: case['link'] for case in similar_cases}
            
            # Add links to similar cases from Indian Kanoon
            for case in analysis.get("similar_cases", []):
                case_name = case.get("case_name", "")
                if case_name in case_links:
                    case["link"] = case_links[case_name]
                else:
                    # If case name doesn't match exactly, try to find a close match
                    for ik_case in similar_cases:
                        if case_name.lower() in ik_case['case_name'].lower() or ik_case['case_name'].lower() in case_name.lower():
                            case["link"] = ik_case['link']
                            break
            
            # Create a mapping of law names to their links
            law_links = {law['name']: law['link'] for law in relevant_laws}
            
            # Add links to applicable laws from Indian Kanoon
            for law in analysis.get("applicable_laws", []):
                law_name = law.get("name", "")
                if law_name in law_links:
                    law["link"] = law_links[law_name]
                else:
                    # If law name doesn't match exactly, try to find a close match
                    for ik_law in relevant_laws:
                        if law_name.lower() in ik_law['name'].lower() or ik_law['name'].lower() in law_name.lower():
                            law["link"] = ik_law['link']
                            break
            
            return analysis
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured error response
            return {
                "error": "Failed to parse analysis results",
                "raw_response": response_text
            }
            
    except Exception as e:
        return {
            "error": f"Error analyzing case: {str(e)}",
            "raw_response": None
        } 