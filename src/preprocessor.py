"""Data preprocessing and filtering utilities"""
import pandas as pd
from src.config import PRODUCT_MAPPING, TARGET_PRODUCTS, MIN_WORDS

def fast_filter_pipeline(df):
    """Combined filtering in one pass"""
    print("✅ Product mapping complete")
    
    # Apply all filters at once
    df_filtered = df[
        df['Consumer complaint narrative'].notna() & 
        df['Product'].map(PRODUCT_MAPPING).fillna('Other').isin(TARGET_PRODUCTS)
    ].copy()
    
    # Add category column
    df_filtered['Product_Category'] = df_filtered['Product'].map(PRODUCT_MAPPING)
    
    print(f"📊 Filtered to {len(df_filtered):,} business-relevant complaints with narratives")
    return df_filtered

def prepare_final_dataset(df):
    """Prepare final dataset for analysis"""
    if len(df) == 0:
        return df
    
    # Clean text
    df['Cleaned_Narrative'] = df['Consumer complaint narrative'].fillna('').astype(str).str.lower()
    df['Cleaned_Narrative'] = df['Cleaned_Narrative'].str.replace(r'[^\w\s]', ' ', regex=True)
    df['Cleaned_Narrative'] = df['Cleaned_Narrative'].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # Filter short texts
    df['Word_Count'] = df['Cleaned_Narrative'].str.split().str.len()
    df_final = df[df['Word_Count'] >= MIN_WORDS].copy()
    
    print(f"✅ Final dataset: {len(df_final):,} complaints ready for analysis")
    print(f"📊 Products: {df_final['Product_Category'].value_counts().to_dict()}")
    
    return df_final