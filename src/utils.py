import os
import json
from datetime import datetime
import numpy as np

def save_data_quality_report(df, report_path):
    """Save data quality report"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'dataset_info': {
            'total_records': int(len(df)),  # Convert to int
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
        },
        'completeness': {
            col: {
                'non_null': int(df[col].notna().sum()),  # Convert to int
                'null': int(df[col].isna().sum()),  # Convert to int
                'completeness_percentage': float(round((df[col].notna().sum() / len(df)) * 100, 2))  # Convert to float
            }
            for col in df.columns
        }
    }
    
    # Handle numeric columns summary - simplified version
    numeric_cols = df.select_dtypes(include=['int64', 'float64'])
    if not numeric_cols.empty:
        summary_stats = {}
        for col in numeric_cols.columns:
            summary_stats[col] = {
                'count': int(numeric_cols[col].count()),
                'mean': float(numeric_cols[col].mean()),
                'std': float(numeric_cols[col].std()),
                'min': float(numeric_cols[col].min()),
                '25%': float(numeric_cols[col].quantile(0.25)),
                '50%': float(numeric_cols[col].quantile(0.50)),
                '75%': float(numeric_cols[col].quantile(0.75)),
                'max': float(numeric_cols[col].max())
            }
        report['summary_stats'] = summary_stats
    else:
        report['summary_stats'] = {}
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📋 Data quality report saved: {report_path}")
    return report