# src/evaluation_dashboard.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

def create_evaluation_report(results_df):
    """Generate professional evaluation charts"""
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('RAG System Evaluation Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Confidence Scores by Question
    if 'confidence' in results_df.columns:
        bars = axes[0,0].barh(range(len(results_df)), results_df['confidence'].values)
        axes[0,0].set_yticks(range(len(results_df)))
        axes[0,0].set_yticklabels([f"Q{i+1}" for i in range(len(results_df))])
        axes[0,0].set_xlabel('Confidence Score')
        axes[0,0].set_title('Confidence by Question')
        axes[0,0].axvline(70, color='g', linestyle='--', alpha=0.7, label='High (70+)')
        axes[0,0].axvline(40, color='orange', linestyle='--', alpha=0.7, label='Medium (40-70)')
        axes[0,0].legend()
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            axes[0,0].text(width + 1, bar.get_y() + bar.get_height()/2, 
                          f'{width:.1f}', va='center', fontsize=9)
    
    # 2. Keyword Match Scores
    if 'keyword_score' in results_df.columns:
        bars = axes[0,1].bar(range(len(results_df)), results_df['keyword_score'].values, color='#4ECDC4')
        axes[0,1].set_xlabel('Question ID')
        axes[0,1].set_ylabel('Keyword Match (0-5)')
        axes[0,1].set_title('Keyword Relevance Score')
        axes[0,1].set_xticks(range(len(results_df)))
        axes[0,1].set_xticklabels([f"Q{i+1}" for i in range(len(results_df))])
        axes[0,1].axhline(3, color='g', linestyle='--', label='Target (3)')
        axes[0,1].legend()
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            axes[0,1].text(bar.get_x() + bar.get_width()/2, height + 0.1,
                          f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    # 3. Success Rate Pie Chart
    if 'success' in results_df.columns:
        success_counts = results_df['success'].value_counts()
        colors = ['#51cf66' if True else '#ff6b6b' for i in success_counts.index]
        axes[1,0].pie(success_counts.values, 
                      labels=['Success' if i else 'Failed' for i in success_counts.index],
                      autopct='%1.1f%%', 
                      colors=['#51cf66', '#ff6b6b'][:len(success_counts)],
                      startangle=90)
        axes[1,0].set_title(f'Success Rate: {results_df["success"].mean()*100:.1f}%')
    
    # 4. Metrics Summary Table
    axes[1,1].axis('off')
    
    # Calculate metrics
    avg_conf = results_df['confidence'].mean() if 'confidence' in results_df.columns else 0
    avg_keyword = results_df['keyword_score'].mean() if 'keyword_score' in results_df.columns else 0
    success_rate = results_df['success'].mean() * 100 if 'success' in results_df.columns else 0
    
    summary_text = f"""
    {'='*40}
    📊 EVALUATION SUMMARY
    {'='*40}
    
    📝 Questions Evaluated: {len(results_df)}
    
    📈 Confidence Score:
        • Average: {avg_conf:.1f}/100
        • Range: {results_df['confidence'].min():.1f} - {results_df['confidence'].max():.1f}
    
    🔍 Keyword Relevance:
        • Average: {avg_keyword:.1f}/5
        • Target: >3.0
    
    ✅ Success Rate:
        • Overall: {success_rate:.1f}%
        • Target: >50%
    
    {'='*40}
    """
    
    axes[1,1].text(0.1, 0.5, summary_text, fontsize=12, fontfamily='monospace',
                   verticalalignment='center',
                   bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.8))
    
    plt.tight_layout()
    
    # Save dashboard
    dashboard_path = Path('reports/evaluation_dashboard.png')
    plt.savefig(dashboard_path, dpi=150, bbox_inches='tight')
    print(f"✅ Dashboard saved to {dashboard_path}")
    
    plt.show()
    
    # Print detailed recommendations
    print("\n" + "="*60)
    print("📋 RECOMMENDATIONS")
    print("="*60)
    
    if avg_conf < 40:
        print("🔴 CRITICAL: Confidence scores are very low")
        print("   • Improve embedding quality")
        print("   • Add more training data")
    elif avg_conf < 60:
        print("🟡 MODERATE: Confidence scores need improvement")
        print("   • Fine-tune chunk size (currently 500)")
        print("   • Add hybrid search (semantic + keyword)")
    else:
        print("🟢 GOOD: Confidence scores are acceptable")
    
    if avg_keyword < 3:
        print("🔴 CRITICAL: Keyword relevance is low")
        print("   • Improve query understanding")
        print("   • Add query expansion")
    else:
        print("🟢 GOOD: Keyword relevance is acceptable")
    
    if success_rate < 50:
        print("🔴 CRITICAL: Success rate is below target")
        print("   • Review failed queries")
        print("   • Improve retrieval accuracy")
    else:
        print("🟢 GOOD: Success rate meets target")
    
    return dashboard_path


def create_performance_chart(performance_data):
    """Create performance tracking chart"""
    plt.figure(figsize=(10, 6))
    
    queries = list(performance_data.keys())
    times = list(performance_data.values())
    
    plt.plot(queries, times, marker='o', linewidth=2, markersize=8)
    plt.xlabel('Query')
    plt.ylabel('Response Time (seconds)')
    plt.title('RAG System Performance Over Time')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('reports/performance_chart.png', dpi=150)
    plt.show()


def print_evaluation_table(results_df):
    """Print a formatted evaluation table"""
    print("\n" + "="*100)
    print("📊 EVALUATION RESULTS TABLE")
    print("="*100)
    
    for i, row in results_df.iterrows():
        print(f"\nQ{row.get('question_id', i+1)}: {row.get('question', 'Unknown')[:60]}...")
        print(f"   Confidence: {row.get('confidence', 0):.1f}/100 | "
              f"Keyword: {row.get('keyword_score', 0):.1f}/5 | "
              f"Success: {'✅' if row.get('success', False) else '❌'}")
        print(f"   Retrieved: {row.get('retrieved', 0)} complaints")