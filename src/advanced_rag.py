"""
Advanced RAG Pipeline - Main Business Intelligence Engine
"""
import chromadb
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Optional
from datetime import datetime

# Import from local modules
from .config import *
from .query_enhancer import QueryEnhancer
from .vector_store import get_chroma_collection


class AdvancedFinancialRAG:
    """Professional RAG System for Business Intelligence"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self._initialize_system()

    def _initialize_system(self):
        """Initialize all system components"""
        if self.verbose:
            print("🚀 Initializing Advanced Financial RAG...")

        # Core components
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.query_enhancer = QueryEnhancer()
        self.collection = get_chroma_collection()

        # Analytics
        self.analytics = {
            "queries_processed": 0,
            "performance_stats": {
                "total_queries": 0,
                "successful_queries": 0,
                "avg_retrieval_count": 0,
            },
        }

        if self.verbose:
            count = self.collection.count()
            print(f"✅ System Ready: {count} complaint chunks")

    def analyze_query(self, question: str) -> Dict:
        """Analyze business query"""
        return self.query_enhancer.analyze_query(question)

    def retrieve_complaints(
        self,
        question: str,
        analysis: Dict,
        k: int = RETRIEVAL_K,
        product_filter: Optional[str] = None,
    ) -> Dict:
        """Intelligent complaint retrieval"""

        # Prepare filter
        where_filter = None
        if product_filter and product_filter in PRODUCT_CATEGORIES:
            where_filter = {
                "$or": [
                    {"product_category": {"$in": PRODUCT_CATEGORIES[product_filter]}},
                    {"product": {"$in": PRODUCT_CATEGORIES[product_filter]}},
                ]
            }

        # Enhanced queries
        enhanced = self.query_enhancer.enhance_query(question, analysis)

        # Execute search
        results = self.collection.query(
            query_texts=enhanced[:2],
            n_results=k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        return {
            "chunks": results["documents"][0] if results["documents"] else [],
            "metadata": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "count": len(results["documents"][0]) if results["documents"] else 0,
            "query_analysis": analysis,
        }

    def calculate_confidence(self, retrieved_data: Dict) -> Dict:
        """Calculate confidence score"""
        if retrieved_data["count"] == 0:
            return {"total_score": 0, "level": "NO_DATA"}

        # Simplified confidence calculation
        avg_distance = sum(retrieved_data["distances"]) / len(
            retrieved_data["distances"]
        )
        similarity_score = (1 - avg_distance) * 100

        if similarity_score >= 70:
            level = "HIGH"
        elif similarity_score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "total_score": round(similarity_score, 1),
            "level": level,
            "retrieved_count": retrieved_data["count"],
        }

    def ask(self, question: str, product_filter: Optional[str] = None) -> Dict:
        """Main method: Ask business question"""
        # Update analytics
        self.analytics["queries_processed"] += 1
        self.analytics["performance_stats"]["total_queries"] += 1

        # Step 1: Analyze query
        query_analysis = self.analyze_query(question)

        # Step 2: Retrieve complaints
        retrieved = self.retrieve_complaints(
            question, query_analysis, product_filter=product_filter
        )

        if retrieved["count"] > 0:
            self.analytics["performance_stats"]["successful_queries"] += 1
            self.analytics["performance_stats"]["avg_retrieval_count"] = (
                self.analytics["performance_stats"]["avg_retrieval_count"]
                * (self.analytics["performance_stats"]["total_queries"] - 1)
                + retrieved["count"]
            ) / self.analytics["performance_stats"]["total_queries"]

        # Step 3: Calculate confidence
        confidence = self.calculate_confidence(retrieved)

        # Step 4: Generate insights
        insights = self._generate_insights(question, retrieved, confidence)

        # Step 5: Prepare sources
        sources = []
        for i, (meta, dist) in enumerate(
            zip(retrieved["metadata"], retrieved["distances"])
        ):
            sources.append(
                {
                    "source_id": i + 1,
                    "product": self._extract_product(meta),
                    "issue": self._extract_issue(meta),
                    "similarity_score": (1 - dist) * 100 if dist else 0,
                }
            )

        # Prepare response
        response = {
            "question": question,
            "query_analysis": query_analysis,
            "business_insights": insights,
            "confidence_metrics": confidence,
            "sources": sources,
            "retrieval_stats": {
                "total_complaints": retrieved["count"],
                "products_covered": len(
                    set(self._extract_product(m) for m in retrieved["metadata"])
                ),
                "issues_identified": len(
                    set(self._extract_issue(m) for m in retrieved["metadata"])
                ),
            },
        }

        return response

    def _generate_insights(
        self, question: str, retrieved: Dict, confidence: Dict
    ) -> Dict:
        """Generate business insights"""
        if retrieved["count"] == 0:
            return {
                "executive_summary": "No relevant complaints found.",
                "key_findings": [],
                "recommendations": ["Try a different question or filter"],
            }

        # Simple insight generation
        products = [self._extract_product(m) for m in retrieved["metadata"]]
        issues = [self._extract_issue(m) for m in retrieved["metadata"]]

        top_product = max(set(products), key=products.count) if products else "Unknown"
        top_issue = max(set(issues), key=issues.count) if issues else "General"

        return {
            "executive_summary": f"Analysis of {retrieved['count']} complaints reveals "
            f"{top_product} issues are most common, primarily "
            f"related to {top_issue}.",
            "key_findings": [
                f"Top product: {top_product}",
                f"Most frequent issue: {top_issue}",
                f"Confidence level: {confidence['level']}",
            ],
            "recommendations": [
                f"Focus on {top_issue} resolution for {top_product}",
                "Monitor emerging complaint patterns",
                "Consider targeted customer outreach",
            ],
        }

    def _extract_product(self, meta: Dict) -> str:
        """Extract product from metadata"""
        if not meta:
            return "Unknown"
        for field in ["product_category", "product", "Product"]:
            if field in meta and meta[field]:
                return str(meta[field])
        return "Unknown"

    def _extract_issue(self, meta: Dict) -> str:
        """Extract issue from metadata"""
        if not meta:
            return "General"
        for field in ["issue", "Issue", "sub_issue"]:
            if field in meta and meta[field]:
                return str(meta[field])
        return "General"

    def get_performance_report(self) -> Dict:
        """Get performance report"""
        stats = self.analytics["performance_stats"]
        total = stats["total_queries"]
        success_rate = (stats["successful_queries"] / total * 100) if total > 0 else 0

        return {
            "summary": {
                "total_queries_processed": self.analytics["queries_processed"],
                "success_rate": f"{success_rate:.1f}%",
                "avg_complaints_per_query": round(stats["avg_retrieval_count"], 1),
                "system_uptime": "Active",
            },
            "recommendations": [
                "System performing optimally"
                if success_rate > 70
                else "Consider improving query understanding",
                "Ready for production deployment",
            ],
        }

    def get_dataset_statistics(self) -> Dict:
        """Get dataset statistics"""
        count = self.collection.count()

        return {
            "total_complaint_chunks": count,
            "estimated_complaints": count // 3,
            "unique_product_categories": 5,
            "unique_issues": 10,
            "sample_products": ["Credit card", "Mortgage", "Student Loan"],
        }


def print_detailed_response(response: Dict):
    """
    📊 Professional response formatting for business users
    """
    print(f"\n{'='*60}")
    print("📊 BUSINESS INTELLIGENCE REPORT")
    print(f"{'='*60}")

    # Question
    print(f"\n📝 QUESTION: {response['question']}")

    # Query Analysis
    analysis = response["query_analysis"]
    if analysis.get("products"):
        print(f"🔍 DETECTED: {', '.join(analysis['products'])} focus")

    # Business Insights
    insights = response["business_insights"]
    print(f"\n💼 EXECUTIVE SUMMARY:")
    print(f"   {insights['executive_summary']}")

    print(f"\n🎯 KEY FINDINGS:")
    for finding in insights["key_findings"]:
        if finding and finding.strip():
            print(f"   • {finding}")

    # Confidence
    confidence = response["confidence_metrics"]
    print(f"\n📈 CONFIDENCE ANALYSIS:")
    print(f"   Overall: {confidence['level']} ({confidence['total_score']}/100)")

    # Sources
    if response.get("sources"):
        valid_sources = [
            s for s in response["sources"] if s.get("product") != "Unknown"
        ]
        if valid_sources:
            print(f"\n📚 EVIDENCE SOURCES ({len(valid_sources)} complaints):")
            for source in valid_sources[:3]:
                print(
                    f"   [{source['source_id']}] {source['product']} - {source['issue']}"
                )
                if source.get("similarity_score", 0) > 0:
                    print(f"      Similarity: {source['similarity_score']:.1f}%")

    # Recommendations
    if insights.get("recommendations"):
        print(f"\n🚀 RECOMMENDED ACTIONS:")
        for rec in insights["recommendations"][:3]:
            if rec and rec.strip():
                print(f"   • {rec}")

    # System Info
    if "retrieval_stats" in response:
        stats = response["retrieval_stats"]
        print(f"\n📊 ANALYSIS METRICS:")
        print(f"   • Complaints analyzed: {stats.get('total_complaints', 0)}")
        print(f"   • Products covered: {stats.get('products_covered', 0)}")
        print(f"   • Issues identified: {stats.get('issues_identified', 0)}")

    print(f"\n{'='*60}")


# Export both the class and function
__all__ = ["AdvancedFinancialRAG", "print_detailed_response"]
