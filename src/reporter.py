"""Reporting utilities for data quality"""
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.config import cfg

def save_data_quality_report(df: pd.DataFrame, report_path: Path):
    """Save comprehensive data quality report"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'dataset_info': {
            'total_records': int(len(df)),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
        },
        'completeness': {
            col: {
                'non_null': int(df[col].notna().sum()),
                'null': int(df[col].isna().sum()),
                'completeness_percentage': float(round((df[col].notna().sum() / len(df)) * 100, 2))
            }
            for col in df.columns
        }
    }
    
    # Add numeric summary if available
    numeric_cols = df.select_dtypes(include=['int64', 'float64'])
    if not numeric_cols.empty:
        report['summary_stats'] = {
            col: {
                'mean': float(numeric_cols[col].mean()),
                'std': float(numeric_cols[col].std()),
                'min': float(numeric_cols[col].min()),
                'max': float(numeric_cols[col].max())
            }
            for col in numeric_cols.columns
        }
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

def generate_task1_summary(final_df: pd.DataFrame, product_dist: pd.Series) -> str:
    """Generate task 1 completion summary"""
    avg_words = final_df['Text_Length_Words'].mean()
    
    summary = f"""
    ================================================================================
    TASK 1 COMPLETE - DATA READY FOR TASK 2
    ================================================================================
    
    📊 YOUR CLEANED DATASET:
    ────────────────────────────────────────────────────
    • Size: {len(final_df):,} complaints
    • Products: {', '.join(cfg.TARGET_PRODUCTS)}
    • Cleaned text: Available in 'Cleaned_Narrative' column
    • Text length: Average {avg_words:.0f} words/complaint
    
    📁 FILES CREATED:
    ────────────────────────────────────────────────────
    1. data/filtered_complaints.csv (Main dataset)
    2. reports/task1_quality_report.json (Report)
    3. reports/product_dashboard.html (Visualization)
    
    🚀 NEXT STEPS:
    ────────────────────────────────────────────────────
    1. Use 'data/filtered_complaints.csv' for Task 2
    2. Focus on 'Cleaned_Narrative' column for text processing
    3. Use 'Product_Category' for filtering
    4. Proceed with chunking and embedding
    """
    
    return summary

def create_text_report(df: pd.DataFrame, save_path: Path):
    """Create a simple text report with key statistics"""
    with open(save_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DATA QUALITY REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total complaints: {len(df):,}\n\n")
        
        f.write("PRODUCT DISTRIBUTION:\n")
        f.write("-" * 40 + "\n")
        for product, count in df['Product_Category'].value_counts().items():
            f.write(f"{product}: {count:,} ({(count/len(df)*100):.1f}%)\n")
        
        f.write("\nTEXT STATISTICS:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Average words: {df['Text_Length_Words'].mean():.0f}\n")
        f.write(f"Median words: {df['Text_Length_Words'].median():.0f}\n")
        f.write(f"Min words: {df['Text_Length_Words'].min()}\n")
        f.write(f"Max words: {df['Text_Length_Words'].max():,}\n")