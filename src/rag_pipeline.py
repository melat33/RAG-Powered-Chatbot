"""
🏆 Advanced RAG Pipeline for Financial Complaint Analysis
Professional implementation with business intelligence features
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Optional, Tuple
import pandas as pd
from datetime import datetime
from src.config import *
from src.query_enhancer import QueryEnhancer
from src.prompt_templates import FinancialPrompts

class AdvancedFinancialRAG:
    """
    🏆 Professional RAG System for CrediTrust Financial
    
    Features:
    1. Semantic Search with Query Understanding
    2. Multi-level Confidence Scoring
    3. Business Intelligence Insights
    4. Source Attribution & Traceability
    5. Performance Analytics
    """
    
    def __init__(self, verbose: bool = True):
        """Initialize the advanced RAG system"""
        self.verbose = verbose
        self.performance_metrics = {
            "queries_processed": 0,
            "total_retrieved": 0,
            "avg_confidence": 0,
            "success_rate": 0
        }
        
        if verbose:
            print("🚀 Initializing Advanced Financial RAG System...")
        
        # Initialize components
        self._initialize_components()
        
        if verbose:
            print(f"✅ System Ready: {self.collection.count()} complaints loaded")
            print("   • Semantic Search Engine ✓")
            print("   • Query Understanding Module ✓")
            print("   • Business Intelligence Layer ✓")
            print("   • Confidence Scoring System ✓")
            print("   • Performance Analytics ✓")
    
    def _initialize_components(self):
        """Initialize all system components"""
        # 1. Embedding model for semantic search
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        
        # 2. Query understanding module
        self.query_analyzer = QueryEnhancer()
        
        # 3. Business prompt templates
        self.prompter = FinancialPrompts()
        
        # 4. ChromaDB vector store
        self.client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        self.collection = self.client.get_collection("complaint_embeddings")
        
        # 5. Initialize analytics
        self.analytics = {
            "query_log": [],
            "performance_stats": {
                "total_queries": 0,
                "successful_queries": 0,
                "avg_retrieval_count": 0,
                "avg_confidence": 0
            }
        }
    
    def analyze_query(self, question: str) -> Dict:
        """
        🎯 Advanced query analysis with business context
        
        Returns:
            Dict with query type, products, intent, and business context
        """
        analysis = self.query_analyzer.analyze_query(question)
        
        # Add business context analysis
        business_keywords = {
            "urgent": ["urgent", "critical", "immediate", "emergency"],
            "trend": ["trend", "pattern", "increasing", "decreasing", "over time"],
            "comparison": ["compare", "vs", "versus", "difference", "similar"],
            "root_cause": ["why", "reason", "cause", "root cause"],
            "volume": ["many", "often", "frequent", "common", "multiple"]
        }
        
        analysis["business_context"] = {
            "urgency": any(word in question.lower() for word in business_keywords["urgent"]),
            "needs_trend_analysis": any(word in question.lower() for word in business_keywords["trend"]),
            "is_comparative": any(word in question.lower() for word in business_keywords["comparison"]),
            "needs_root_cause": any(word in question.lower() for word in business_keywords["root_cause"]),
            "volume_analysis": any(word in question.lower() for word in business_keywords["volume"])
        }
        
        return analysis
    
    def retrieve_complaints(self, question: str, analysis: Dict, 
                          k: int = RETRIEVAL_K, 
                          product_filter: Optional[str] = None) -> Dict:
        """
        🔍 Intelligent retrieval with business-aware filtering
        
        Features:
        1. Query expansion based on business context
        2. Dynamic K adjustment based on query complexity
        3. Product-aware filtering
        4. Relevance scoring
        """
        if self.verbose:
            print(f"\n🔍 Processing: '{question}'")
            if product_filter:
                print(f"   Filter: {product_filter}")
        
        # Adjust K based on query complexity
        if analysis["business_context"]["is_comparative"]:
            k = min(8, k * 2)  # Need more for comparisons
        elif analysis["business_context"]["needs_trend_analysis"]:
            k = min(10, k * 2)  # Need more for trend analysis
        
        # Prepare filter
        where_filter = None
        if product_filter:
            where_filter = {"product_category": {"$eq": product_filter}}
        
        # Generate enhanced queries for better retrieval
        enhanced_queries = self.query_analyzer.enhance_query(question, analysis)
        
        # Execute search
        results = self.collection.query(
            query_texts=enhanced_queries[:2],  # Use top 2 enhanced queries
            n_results=k,
            where=where_filter,
            include=["documents", "metadatas", "distances", "embeddings"]
        )
        
        # Process results
        retrieved_data = {
            "chunks": results['documents'][0] if results['documents'] else [],
            "metadata": results['metadatas'][0] if results['metadatas'] else [],
            "distances": results['distances'][0] if results['distances'] else [],
            "count": len(results['documents'][0]) if results['documents'] else 0,
            "query_analysis": analysis,
            "retrieval_time": datetime.now().isoformat()
        }
        
        if self.verbose and retrieved_data["count"] > 0:
            print(f"   ✅ Retrieved: {retrieved_data['count']} complaints")
        
        return retrieved_data
    
    def calculate_confidence_score(self, retrieved_data: Dict) -> Dict:
        """
        📊 Multi-dimensional confidence scoring
        
        Scores:
        1. Semantic Similarity (0-40 points)
        2. Retrieval Quality (0-30 points)  
        3. Source Diversity (0-20 points)
        4. Metadata Completeness (0-10 points)
        """
        if retrieved_data["count"] == 0:
            return {
                "total_score": 0,
                "level": "NO_DATA",
                "breakdown": {
                    "semantic_similarity": 0,
                    "retrieval_quality": 0,
                    "source_diversity": 0,
                    "metadata_completeness": 0
                },
                "retrieved_count": 0
            }
        
        # 1. Semantic Similarity Score (0-40)
        if retrieved_data["distances"]:
            avg_distance = sum(retrieved_data["distances"]) / len(retrieved_data["distances"])
            similarity = 1 - avg_distance
            semantic_score = min(40, similarity * 40)
        else:
            semantic_score = 20  # Default medium score
        
        # 2. Retrieval Quality Score (0-30)
        # Based on number of retrieved items vs requested
        requested_k = RETRIEVAL_K
        actual_count = retrieved_data["count"]
        retrieval_ratio = actual_count / requested_k if requested_k > 0 else 0
        retrieval_score = min(30, retrieval_ratio * 30)
        
        # 3. Source Diversity Score (0-20)
        # Check if we have complaints from multiple products
        if retrieved_data["metadata"]:
            products = set()
            for meta in retrieved_data["metadata"]:
                if 'product_category' in meta:
                    products.add(meta['product_category'])
            diversity_ratio = len(products) / len(retrieved_data["metadata"])
            diversity_score = min(20, diversity_ratio * 20)
        else:
            diversity_score = 0
        
        # 4. Metadata Completeness Score (0-10)
        if retrieved_data["metadata"]:
            complete_metadata = 0
            for meta in retrieved_data["metadata"]:
                # Check for key metadata fields
                if all(key in meta for key in ['product_category', 'issue']):
                    complete_metadata += 1
            metadata_score = (complete_metadata / len(retrieved_data["metadata"])) * 10
        else:
            metadata_score = 0
        
        # Total score
        total_score = semantic_score + retrieval_score + diversity_score + metadata_score
        
        # Confidence level
        if total_score >= 70:
            level = "HIGH"
        elif total_score >= 40:
            level = "MEDIUM"
        elif total_score >= 20:
            level = "LOW"
        else:
            level = "VERY_LOW"
        
        return {
            "total_score": round(total_score, 1),
            "level": level,
            "breakdown": {
                "semantic_similarity": round(semantic_score, 1),
                "retrieval_quality": round(retrieval_score, 1),
                "source_diversity": round(diversity_score, 1),
                "metadata_completeness": round(metadata_score, 1)
            },
            "retrieved_count": retrieved_data["count"]
        }
    
    def generate_business_insights(self, question: str, 
                                 retrieved_data: Dict,
                                 confidence: Dict) -> Dict:
        """
        💼 Generate business intelligence insights
        
        Features:
        1. Executive summary
        2. Key findings with evidence
        3. Pattern analysis
        4. Actionable recommendations
        """
        if retrieved_data["count"] == 0:
            return {
                "executive_summary": "No relevant complaints found for analysis.",
                "key_findings": [],
                "patterns_detected": [],
                "recommendations": [],
                "evidence_count": 0
            }
        
        # Analyze retrieved complaints
        products = {}
        issues = {}
        severities = {"high": 0, "medium": 0, "low": 0}
        
        for meta in retrieved_data["metadata"]:
            # Product analysis
            product = meta.get('product_category', 'Unknown')
            products[product] = products.get(product, 0) + 1
            
            # Issue analysis
            issue = meta.get('issue', 'Uncategorized')
            issues[issue] = issues.get(issue, 0) + 1
            
            # Severity analysis (based on issue type)
            if any(term in str(issue).lower() for term in ['fraud', 'unauthorized', 'theft']):
                severities["high"] += 1
            elif any(term in str(issue).lower() for term in ['fee', 'charge', 'billing']):
                severities["medium"] += 1
            else:
                severities["low"] += 1
        
        # Generate insights based on query type
        analysis = retrieved_data["query_analysis"]
        
        if analysis["business_context"]["is_comparative"]:
            insights = self._generate_comparative_insights(products, issues, question)
        elif analysis["business_context"]["needs_trend_analysis"]:
            insights = self._generate_trend_insights(products, issues, question)
        elif analysis["business_context"]["needs_root_cause"]:
            insights = self._generate_root_cause_insights(products, issues, question)
        else:
            insights = self._generate_general_insights(products, issues, severities, question)
        
        # Add confidence context
        insights["confidence_context"] = {
            "score": confidence["total_score"],
            "level": confidence["level"],
            "evidence_strength": "Strong" if confidence["retrieved_count"] >= 3 else "Moderate" if confidence["retrieved_count"] >= 1 else "Weak"
        }
        
        return insights
    
    def _generate_general_insights(self, products: Dict, issues: Dict, 
                                 severities: Dict, question: str) -> Dict:
        """Generate general business insights"""
        # Top products with complaints
        top_products = sorted(products.items(), key=lambda x: x[1], reverse=True)[:3]
        top_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "executive_summary": f"Analysis of {sum(products.values())} relevant complaints reveals key customer pain points.",
            "key_findings": [
                f"Top product category: {top_products[0][0]} ({top_products[0][1]} complaints)" if top_products else "No product data",
                f"Most frequent issue: {top_issues[0][0]} ({top_issues[0][1]} occurrences)" if top_issues else "No issue data",
                f"Severity distribution: {severities['high']} high, {severities['medium']} medium, {severities['low']} low priority"
            ],
            "patterns_detected": [
                f"Product concentration: {len(products)} different products mentioned",
                f"Issue diversity: {len(issues)} distinct issues identified"
            ],
            "recommendations": [
                "Prioritize fixes for high-severity issues first",
                "Consider product-specific training for support teams",
                "Monitor emerging issues for proactive response"
            ],
            "evidence_count": sum(products.values())
        }
    
    def _generate_comparative_insights(self, products: Dict, issues: Dict, 
                                     question: str) -> Dict:
        """Generate comparative insights between products"""
        if len(products) < 2:
            return {
                "executive_summary": "Insufficient data for comparative analysis.",
                "key_findings": ["Need complaints from at least 2 different products for comparison"],
                "patterns_detected": [],
                "recommendations": ["Ask more general questions to gather broader data"],
                "evidence_count": sum(products.values())
            }
        
        sorted_products = sorted(products.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "executive_summary": f"Comparative analysis across {len(products)} product categories.",
            "key_findings": [
                f"Highest complaint volume: {sorted_products[0][0]} ({sorted_products[0][1]} complaints)",
                f"Lowest complaint volume: {sorted_products[-1][0]} ({sorted_products[-1][1]} complaints)",
                f"Complaint ratio: {sorted_products[0][0]} has {sorted_products[0][1]/sorted_products[-1][1]:.1f}x more complaints than {sorted_products[-1][0]}"
            ],
            "patterns_detected": [
                f"Product diversity: Complaints span {len(products)} categories",
                f"Distribution: {', '.join([f'{p}: {c}' for p, c in sorted_products[:3]])}"
            ],
            "recommendations": [
                f"Investigate why {sorted_products[0][0]} has highest complaint volume",
                f"Learn from {sorted_products[-1][0]}'s lower complaint rate",
                "Consider cross-product issue resolution teams"
            ],
            "evidence_count": sum(products.values())
        }
    
    def _generate_trend_insights(self, products: Dict, issues: Dict, 
                               question: str) -> Dict:
        """Generate trend analysis insights"""
        top_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "executive_summary": f"Trend analysis based on {sum(products.values())} relevant complaints.",
            "key_findings": [
                f"Top trending issue: {top_issues[0][0]} ({top_issues[0][1]} occurrences)" if top_issues else "No trend data",
                f"Issue frequency spread: {len(issues)} distinct issues identified",
                f"Product coverage: Complaints from {len(products)} product categories"
            ],
            "patterns_detected": [
                f"Dominant issues: Top 3 issues account for {sum(c for _, c in top_issues[:3])/sum(issues.values())*100:.1f}% of complaints" if len(top_issues) >= 3 else "Insufficient data for pattern detection"
            ],
            "recommendations": [
                "Monitor top issues for escalation patterns",
                "Set up alerts for emerging complaint types",
                "Conduct deep dive on most frequent issues"
            ],
            "evidence_count": sum(products.values())
        }
    
    def _generate_root_cause_insights(self, products: Dict, issues: Dict, 
                                    question: str) -> Dict:
        """Generate root cause analysis insights"""
        # Simple root cause categorization
        root_cause_categories = {
            "Process Issues": ["delay", "slow", "wait", "pending", "processing"],
            "Communication Issues": ["notification", "inform", "tell", "communication", "update"],
            "Technical Issues": ["error", "bug", "technical", "system", "website"],
            "Policy Issues": ["fee", "charge", "policy", "term", "condition"]
        }
        
        categorized_issues = {category: 0 for category in root_cause_categories.keys()}
        
        for issue, count in issues.items():
            issue_lower = str(issue).lower()
            for category, keywords in root_cause_categories.items():
                if any(keyword in issue_lower for keyword in keywords):
                    categorized_issues[category] += count
                    break
        
        top_categories = sorted(categorized_issues.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "executive_summary": f"Root cause analysis of {sum(issues.values())} issue occurrences.",
            "key_findings": [
                f"Primary root cause category: {top_categories[0][0]} ({top_categories[0][1]} issues)" if top_categories[0][1] > 0 else "No clear root cause pattern",
                f"Secondary category: {top_categories[1][0]} ({top_categories[1][1]} issues)" if len(top_categories) > 1 and top_categories[1][1] > 0 else "",
                f"Root cause distribution: {', '.join([f'{c}: {n}' for c, n in top_categories if n > 0])}"
            ],
            "patterns_detected": [
                f"Systemic issues: {top_categories[0][0]} appears most frequently" if top_categories[0][1] > 0 else "",
                f"Multiple root cause categories identified: {len([c for c in categorized_issues.values() if c > 0])}"
            ],
            "recommendations": [
                f"Address systemic {top_categories[0][0].lower()} issues first" if top_categories[0][1] > 0 else "Collect more specific complaint data",
                "Implement targeted fixes for each root cause category",
                "Track resolution effectiveness by root cause type"
            ],
            "evidence_count": sum(issues.values())
        }
    
    def ask(self, question: str, product_filter: Optional[str] = None) -> Dict:
        """
        🎯 Main method: Ask a business question about complaints
        
        Returns comprehensive analysis with:
        1. Business insights
        2. Confidence scoring
        3. Source attribution
        4. Performance metrics
        """
        # Update analytics
        self.analytics["query_log"].append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "filter": product_filter
        })
        self.analytics["performance_stats"]["total_queries"] += 1
        
        # Step 1: Query Analysis
        query_analysis = self.analyze_query(question)
        
        # Step 2: Intelligent Retrieval
        retrieved_data = self.retrieve_complaints(question, query_analysis, 
                                                product_filter=product_filter)
        
        # Step 3: Confidence Scoring
        confidence = self.calculate_confidence_score(retrieved_data)
        
        # Step 4: Business Insights Generation
        insights = self.generate_business_insights(question, retrieved_data, confidence)
        
        # Step 5: Prepare Sources with Details
        sources = []
        for i, (meta, distance) in enumerate(zip(retrieved_data["metadata"], 
                                                retrieved_data.get("distances", [])), 1):
            similarity = (1 - distance) * 100 if distance is not None else 0
            sources.append({
                "source_id": i,
                "product": meta.get('product_category', 'Unknown'),
                "issue": meta.get('issue', 'General'),
                "company": meta.get('company', 'Unknown'),
                "state": meta.get('state', 'Unknown'),
                "similarity_score": round(similarity, 1),
                "date_received": meta.get('date_received', 'Unknown')
            })
        
        # Update success rate
        if retrieved_data["count"] > 0:
            self.analytics["performance_stats"]["successful_queries"] += 1
        
        # Update average metrics
        total_queries = self.analytics["performance_stats"]["total_queries"]
        successful_queries = self.analytics["performance_stats"]["successful_queries"]
        
        self.analytics["performance_stats"]["success_rate"] = (
            successful_queries / total_queries * 100 if total_queries > 0 else 0
        )
        
        # Compile final response
        response = {
            "question": question,
            "query_analysis": query_analysis,
            "business_insights": insights,
            "confidence_metrics": confidence,
            "sources": sources,
            "retrieval_stats": {
                "total_complaints": retrieved_data["count"],
                "products_covered": len(set(s["product"] for s in sources)),
                "issues_identified": len(set(s["issue"] for s in sources)),
                "retrieval_time": retrieved_data["retrieval_time"]
            },
            "system_analytics": {
                "query_id": len(self.analytics["query_log"]),
                "success": retrieved_data["count"] > 0,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return response
    
    def get_performance_report(self) -> Dict:
        """📈 Get system performance analytics report"""
        stats = self.analytics["performance_stats"]
        
        return {
            "summary": {
                "total_queries_processed": stats["total_queries"],
                "success_rate": f"{stats['success_rate']:.1f}%",
                "avg_complaints_per_query": stats.get("avg_retrieval_count", 0),
                "system_uptime": "Active"
            },
            "recent_queries": self.analytics["query_log"][-5:] if self.analytics["query_log"] else [],
            "recommendations": [
                "System performing well for business queries" if stats["success_rate"] > 70 else "Consider improving query understanding",
                "Good complaint retrieval coverage" if stats.get("avg_retrieval_count", 0) >= 3 else "May need more diverse complaint data",
                "Ready for production use" if stats["total_queries"] >= 10 and stats["success_rate"] > 60 else "Needs more testing"
            ]
        }

def print_detailed_response(response: Dict):
    """
    📊 Professional response formatting for business users
    
    Features:
    1. Executive summary
    2. Key insights with evidence
    3. Confidence breakdown
    4. Source attribution
    5. Actionable recommendations
    """
    print(f"\n{'='*60}")
    print("📊 BUSINESS INTELLIGENCE REPORT")
    print(f"{'='*60}")
    
    # Question
    print(f"\n📝 QUESTION: {response['question']}")
    
    # Query Analysis
    analysis = response['query_analysis']
    if analysis.get('products'):
        print(f"🔍 DETECTED: {', '.join(analysis['products'])} focus")
    
    # Business Insights
    insights = response['business_insights']
    print(f"\n💼 EXECUTIVE SUMMARY:")
    print(f"   {insights['executive_summary']}")
    
    print(f"\n🎯 KEY FINDINGS:")
    for finding in insights['key_findings']:
        if finding:  # Skip empty findings
            print(f"   • {finding}")
    
    # Confidence
    confidence = response['confidence_metrics']
    print(f"\n📈 CONFIDENCE ANALYSIS:")
    print(f"   Overall: {confidence['level']} ({confidence['total_score']}/100)")
    
    if 'breakdown' in confidence:
        print(f"   Breakdown:")
        for metric, score in confidence['breakdown'].items():
            print(f"     • {metric.replace('_', ' ').title()}: {score}")
    
    # Sources
    if response['sources']:
        print(f"\n📚 EVIDENCE SOURCES ({len(response['sources'])} complaints):")
        for source in response['sources'][:3]:  # Show top 3
            print(f"   [{source['source_id']}] {source['product']} - {source['issue']}")
            if source.get('similarity_score', 0) > 0:
                print(f"      Similarity: {source['similarity_score']}%")
    
    # Recommendations
    if insights['recommendations']:
        print(f"\n🚀 RECOMMENDED ACTIONS:")
        for rec in insights['recommendations'][:3]:  # Top 3 recommendations
            print(f"   • {rec}")
    
    # System Info
    stats = response['retrieval_stats']
    print(f"\n📊 ANALYSIS METRICS:")
    print(f"   • Complaints analyzed: {stats['total_complaints']}")
    print(f"   • Products covered: {stats['products_covered']}")
    print(f"   • Issues identified: {stats['issues_identified']}")
    
    print(f"\n{'='*60}")