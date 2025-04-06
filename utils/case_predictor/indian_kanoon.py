"""
Indian Kanoon Data Handler

This module provides functionality for retrieving and processing data from Indian Kanoon
to be used in case analysis.
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
INDIAN_KANOON_API_KEY = os.getenv("INDIAN_KANOON_API_KEY")

class IndianKanoonDataHandler:
    """
    Handler for retrieving and processing data from Indian Kanoon.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Indian Kanoon data handler.
        
        Args:
            api_key: Indian Kanoon API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or INDIAN_KANOON_API_KEY
        if not self.api_key:
            print("Warning: Indian Kanoon API key not found. Some features may be limited.")
    
    def search_cases(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for cases on Indian Kanoon based on the query.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of case data dictionaries
        """
        # This is a placeholder for the actual API call
        # In a real implementation, you would use the Indian Kanoon API
        # For now, we'll return sample data
        
        # Sample data for demonstration
        sample_cases = [
            {
                "case_name": "Vishaka v. State of Rajasthan",
                "citation": "(1997) 6 SCC 241",
                "court": "Supreme Court of India",
                "year": 1997,
                "summary": "Landmark case on sexual harassment at workplace. The court laid down guidelines for preventing sexual harassment of women at workplace.",
                "link": "https://indiankanoon.org/doc/1031794/",
                "relevant_sections": ["Article 14", "Article 15", "Article 21"]
            },
            {
                "case_name": "MC Mehta v. Union of India",
                "citation": "(1987) 1 SCC 395",
                "court": "Supreme Court of India",
                "year": 1987,
                "summary": "Environmental law case establishing the principle of absolute liability for hazardous industries.",
                "link": "https://indiankanoon.org/doc/1929680/",
                "relevant_sections": ["Article 21", "Article 48A"]
            },
            {
                "case_name": "Olga Tellis v. Bombay Municipal Corporation",
                "citation": "(1985) 3 SCC 545",
                "court": "Supreme Court of India",
                "year": 1985,
                "summary": "Case establishing the right to livelihood as part of the right to life under Article 21.",
                "link": "https://indiankanoon.org/doc/1098135/",
                "relevant_sections": ["Article 21", "Article 19"]
            }
        ]
        
        # Filter sample cases based on the query
        # In a real implementation, this would be handled by the API
        filtered_cases = []
        query_terms = query.lower().split()
        
        for case in sample_cases:
            # Simple keyword matching
            case_text = f"{case['case_name']} {case['summary']} {' '.join(case.get('relevant_sections', []))}".lower()
            if any(term in case_text for term in query_terms):
                filtered_cases.append(case)
        
        return filtered_cases[:limit]
    
    def get_case_details(self, case_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific case.
        
        Args:
            case_id: ID of the case on Indian Kanoon
            
        Returns:
            Dictionary containing detailed case information
        """
        # This is a placeholder for the actual API call
        # In a real implementation, you would use the Indian Kanoon API
        
        # Sample data for demonstration
        sample_case = {
            "case_name": "Vishaka v. State of Rajasthan",
            "citation": "(1997) 6 SCC 241",
            "court": "Supreme Court of India",
            "year": 1997,
            "judges": ["J.S. Verma", "Sujata V. Manohar", "B.N. Kirpal"],
            "parties": {
                "petitioner": "Vishaka and others",
                "respondent": "State of Rajasthan and others"
            },
            "summary": "Landmark case on sexual harassment at workplace. The court laid down guidelines for preventing sexual harassment of women at workplace.",
            "judgment": "The Supreme Court held that sexual harassment of women at workplace violates their fundamental rights under Articles 14, 15, and 21 of the Constitution. The court laid down guidelines for preventing sexual harassment of women at workplace, which came to be known as the 'Vishaka Guidelines'.",
            "link": "https://indiankanoon.org/doc/1031794/",
            "relevant_sections": ["Article 14", "Article 15", "Article 21"],
            "related_cases": [
                {
                    "case_name": "Apparel Export Promotion Council v. A.K. Chopra",
                    "citation": "(1999) 1 SCC 759",
                    "link": "https://indiankanoon.org/doc/1031795/"
                },
                {
                    "case_name": "Medha Kotwal Lele v. Union of India",
                    "citation": "(2013) 1 SCC 297",
                    "link": "https://indiankanoon.org/doc/1031796/"
                }
            ]
        }
        
        return sample_case
    
    def get_relevant_laws(self, case_type: str) -> List[Dict[str, Any]]:
        """
        Get relevant laws for a specific case type.
        
        Args:
            case_type: Type of case (e.g., "Civil", "Criminal", "Family")
            
        Returns:
            List of relevant laws with descriptions and links
        """
        # This is a placeholder for the actual API call
        # In a real implementation, you would use the Indian Kanoon API
        
        # Sample data for demonstration
        sample_laws = {
            "Civil": [
                {
                    "name": "Indian Contract Act, 1872",
                    "description": "Governs the formation and enforcement of contracts in India.",
                    "link": "https://indiankanoon.org/doc/195875/"
                },
                {
                    "name": "Specific Relief Act, 1963",
                    "description": "Provides for specific relief for enforcing individual civil rights.",
                    "link": "https://indiankanoon.org/doc/195876/"
                },
                {
                    "name": "Limitation Act, 1963",
                    "description": "Sets time limits for filing different types of lawsuits.",
                    "link": "https://indiankanoon.org/doc/195877/"
                }
            ],
            "Criminal": [
                {
                    "name": "Indian Penal Code, 1860",
                    "description": "Defines crimes and their punishments in India.",
                    "link": "https://indiankanoon.org/doc/195878/"
                },
                {
                    "name": "Code of Criminal Procedure, 1973",
                    "description": "Governs the procedure for investigation and trial of criminal cases.",
                    "link": "https://indiankanoon.org/doc/195879/"
                },
                {
                    "name": "Evidence Act, 1872",
                    "description": "Defines the rules of evidence in Indian courts.",
                    "link": "https://indiankanoon.org/doc/195880/"
                }
            ],
            "Family": [
                {
                    "name": "Hindu Marriage Act, 1955",
                    "description": "Governs marriage, divorce, and other family matters for Hindus.",
                    "link": "https://indiankanoon.org/doc/195881/"
                },
                {
                    "name": "Muslim Personal Law (Shariat) Application Act, 1937",
                    "description": "Applies Muslim personal law to Muslims in India.",
                    "link": "https://indiankanoon.org/doc/195882/"
                },
                {
                    "name": "Guardians and Wards Act, 1890",
                    "description": "Deals with the appointment of guardians for minors.",
                    "link": "https://indiankanoon.org/doc/195883/"
                }
            ],
            "Property": [
                {
                    "name": "Transfer of Property Act, 1882",
                    "description": "Governs the transfer of property in India.",
                    "link": "https://indiankanoon.org/doc/195884/"
                },
                {
                    "name": "Registration Act, 1908",
                    "description": "Provides for the registration of documents.",
                    "link": "https://indiankanoon.org/doc/195885/"
                },
                {
                    "name": "Easements Act, 1882",
                    "description": "Defines and regulates easements and servitudes.",
                    "link": "https://indiankanoon.org/doc/195886/"
                }
            ],
            "Employment": [
                {
                    "name": "Industrial Disputes Act, 1947",
                    "description": "Provides for the investigation and settlement of industrial disputes.",
                    "link": "https://indiankanoon.org/doc/195887/"
                },
                {
                    "name": "Payment of Wages Act, 1936",
                    "description": "Regulates the payment of wages to certain classes of employed persons.",
                    "link": "https://indiankanoon.org/doc/195888/"
                },
                {
                    "name": "Minimum Wages Act, 1948",
                    "description": "Provides for fixing minimum rates of wages in certain employments.",
                    "link": "https://indiankanoon.org/doc/195889/"
                }
            ],
            "Consumer": [
                {
                    "name": "Consumer Protection Act, 2019",
                    "description": "Provides for protection of the interests of consumers.",
                    "link": "https://indiankanoon.org/doc/195890/"
                },
                {
                    "name": "Sale of Goods Act, 1930",
                    "description": "Defines the rights and duties of buyers and sellers.",
                    "link": "https://indiankanoon.org/doc/195891/"
                }
            ]
        }
        
        # Return relevant laws based on case type
        return sample_laws.get(case_type, [])
    
    def get_similar_cases(self, case_details: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get similar cases based on case details.
        
        Args:
            case_details: Dictionary containing case information
            limit: Maximum number of results to return
            
        Returns:
            List of similar case data dictionaries
        """
        # Extract key information from case details
        case_type = case_details.get("case_type", "")
        case_description = case_details.get("case_description", "")
        
        # Search for similar cases
        query = f"{case_type} {case_description}"
        similar_cases = self.search_cases(query, limit)
        
        return similar_cases 