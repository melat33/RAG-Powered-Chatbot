"""
Utility functions for the RAG system
"""
from typing import List, Dict


def load_sample_questions() -> List[Dict]:
    """Load sample questions for demonstration"""
    return [
        {
            "category": "Product Analysis",
            "questions": [
                "What are the top complaints about credit cards?",
                "Why do customers complain about savings accounts?",
                "What issues are specific to personal loans?",
            ],
        },
        {
            "category": "Trend Analysis",
            "questions": [
                "What are trending complaint topics?",
                "How have fraud complaints changed?",
                "Are billing complaints increasing?",
            ],
        },
        {
            "category": "Comparison",
            "questions": [
                "Compare complaints between products",
                "Which product has the most urgent complaints?",
                "How do complaint volumes differ by product?",
            ],
        },
    ]


def analyze_response_quality(response: Dict) -> Dict:
    """Analyze quality metrics of a response"""

    quality_metrics = {
        "has_answer": len(response.get("answer", "")) > 0,
        "answer_length": len(response.get("answer", "")),
        "source_count": response.get("source_count", 0),
        "confidence": response.get("confidence", 0),
        "has_sources": response.get("source_count", 0) > 0,
    }

    # Quality score calculation (0-6)
    quality_score = 0
    if quality_metrics["has_answer"]:
        quality_score += 2
    if quality_metrics["has_sources"]:
        quality_score += 2
    if quality_metrics["confidence"] > 0.5:
        quality_score += 1
    if 100 < quality_metrics["answer_length"] < 500:
        quality_score += 1

    quality_metrics["quality_score"] = quality_score

    return quality_metrics


def format_for_display(response: Dict, max_length: int = 200) -> str:
    """Format response for clean display"""
    if not response.get("business_insights"):
        return "No response generated"

    insights = response["business_insights"]
    summary = insights.get("executive_summary", "")

    if len(summary) > max_length:
        summary = summary[:max_length] + "..."

    return summary
