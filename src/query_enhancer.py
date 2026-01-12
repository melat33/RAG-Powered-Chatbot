"""
Advanced query understanding for financial complaints
"""
import re
from typing import Dict, List, Optional

class QueryEnhancer:
    """Advanced query understanding with financial context"""
    
    # Financial product mapping
    FINANCIAL_PRODUCTS = {
        "credit card": ["credit card", "card", "credit", "visa", "mastercard", "amex"],
        "personal loan": ["personal loan", "loan", "borrowing", "debt"],
        "savings account": ["savings account", "savings", "account", "deposit"],
        "money transfers": ["money transfer", "transfer", "wire", "send money", "remittance"]
    }
    
    # Business intent mapping
    BUSINESS_INTENTS = {
        "analysis": ["what", "how many", "list", "show", "find"],
        "comparison": ["compare", "vs", "versus", "difference", "similar"],
        "root_cause": ["why", "reason", "cause", "root cause"],
        "trend": ["trend", "pattern", "over time", "recent", "last"],
        "urgency": ["urgent", "critical", "immediate", "emergency"]
    }
    
    @staticmethod
    def analyze_query(question: str) -> Dict:
        """Comprehensive query analysis with financial context"""
        question_lower = question.lower()
        
        analysis = {
            "original": question,
            "type": "general",
            "products": [],
            "business_intent": "analysis",
            "time_period": None,
            "urgency_level": "normal",
            "expected_keywords": []
        }
        
        # Detect financial products
        for product, keywords in QueryEnhancer.FINANCIAL_PRODUCTS.items():
            if any(keyword in question_lower for keyword in keywords):
                analysis["products"].append(product)
        
        # Detect business intent
        for intent, keywords in QueryEnhancer.BUSINESS_INTENTS.items():
            if any(keyword in question_lower for keyword in keywords):
                analysis["business_intent"] = intent
                analysis["type"] = intent
                break
        
        # Detect urgency
        if any(word in question_lower for word in ["urgent", "critical", "immediate"]):
            analysis["urgency_level"] = "high"
        
        # Extract time period
        time_patterns = [
            (r"last (\d+) (days|weeks|months)", "recent"),
            (r"in (\d{4})", "year_specific"),
            (r"this (month|week|year)", "current"),
            (r"q[1-4]", "quarter")
        ]
        
        for pattern, period_type in time_patterns:
            match = re.search(pattern, question_lower)
            if match:
                analysis["time_period"] = {"type": period_type, "value": match.group()}
                break
        
        # Extract expected keywords
        financial_keywords = ["fee", "charge", "fraud", "delay", "interest", 
                            "rate", "service", "billing", "transfer", "loan"]
        analysis["expected_keywords"] = [kw for kw in financial_keywords 
                                       if kw in question_lower]
        
        return analysis
    
    @staticmethod
    def enhance_query(question: str, analysis: Dict) -> List[str]:
        """Generate enhanced query variations for better retrieval"""
        enhanced = [question]
        
        # Add product-specific variations
        if analysis["products"]:
            for product in analysis["products"]:
                enhanced.append(f"{question} {product}")
        
        # Add intent-specific variations
        if analysis["business_intent"] == "comparison":
            enhanced.append(f"compare {question}")
        elif analysis["business_intent"] == "root_cause":
            enhanced.append(f"reason for {question}")
        
        # Add keyword expansions
        keyword_expansions = {
            "fee": ["charge", "cost", "payment"],
            "delay": ["slow", "late", "waiting"],
            "fraud": ["unauthorized", "theft", "scam"],
            "interest": ["rate", "percentage", "yield"]
        }
        
        for original, expansions in keyword_expansions.items():
            if original in question.lower():
                for expansion in expansions[:2]:
                    enhanced.append(question.lower().replace(original, expansion))
        
        return list(dict.fromkeys(enhanced))  # Remove duplicates