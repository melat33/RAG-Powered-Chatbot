"""Visualization functions for EDA"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from src.config import cfg

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)

def create_product_dashboard(df: pd.DataFrame, viable_df: pd.DataFrame, save_path: Path = None):
    """Create comprehensive product analysis dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Top 10 Products (All Data)', 
                       'Our Products Distribution (NLP-Viable)',
                       'Narratives Availability',
                       'Complaints by Product Category'),
        specs=[[{'type': 'bar'}, {'type': 'pie'}],
               [{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # 1. Top 10 products
    top_products = df['Product'].value_counts().head(10)
    fig.add_trace(
        go.Bar(x=top_products.values, y=top_products.index, orientation='h',
               marker_color='steelblue', name='Top Products'),
        row=1, col=1
    )
    
    # 2. Our products distribution (pie)
    if 'Product_Category' in viable_df.columns:
        our_counts = viable_df[viable_df['Product_Category'].isin(cfg.TARGET_PRODUCTS)]['Product_Category'].value_counts()
        fig.add_trace(
            go.Pie(labels=our_counts.index, values=our_counts.values, hole=0.3,
                   marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']),
            row=1, col=2
        )
    
    # 3. Narratives availability
    with_narrative = len(viable_df)
    without_narrative = len(df) - with_narrative
    fig.add_trace(
        go.Bar(x=['With Narratives', 'Without Narratives'], 
               y=[with_narrative, without_narrative],
               marker_color=['#4ECDC4', '#FF6B6B']),
        row=2, col=1
    )
    
    # 4. Complaints by product category
    if 'Product_Category' in df.columns:
        product_counts = df[df['Product_Category'].isin(cfg.TARGET_PRODUCTS)]['Product_Category'].value_counts()
        fig.add_trace(
            go.Bar(x=product_counts.index, y=product_counts.values,
                   marker_color='#45B7D1'),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=False,
                     title_text="Product Analysis Dashboard")
    
    if save_path:
        fig.write_html(save_path)
    
    return fig

def create_text_length_plot(df: pd.DataFrame, save_path: Path = None):
    """Create text length distribution plot"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Word Length Distribution', 'Character Length Distribution'),
        specs=[[{'type': 'histogram'}, {'type': 'histogram'}]]
    )
    
    fig.add_trace(
        go.Histogram(x=df['Text_Length_Words'], nbinsx=50, 
                    marker_color='#4ECDC4', name='Words'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Histogram(x=df['Text_Length_Chars'], nbinsx=50,
                    marker_color='#FF6B6B', name='Characters'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, title_text="Text Length Analysis")
    
    if save_path:
        fig.write_html(save_path)
    
    return fig

def create_missing_data_plot(df: pd.DataFrame, save_path: Path = None):
    """Create missing data visualization"""
    missing_data = df.isnull().sum()
    missing_percentage = (missing_data / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percentage': missing_percentage.values
    }).sort_values('Missing_Percentage', ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Top missing columns
    top_missing = missing_df.head(10)
    ax1.barh(top_missing['Column'][::-1], top_missing['Missing_Percentage'][::-1], 
             color='lightcoral')
    ax1.set_xlabel('Missing Percentage (%)')
    ax1.set_title('Top 10 Columns with Missing Data', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Heatmap (sampled for speed)
    sample_df = df.sample(min(1000, len(df)), random_state=42)
    sns.heatmap(sample_df.isnull().T, cmap='YlOrRd', cbar_kws={'label': 'Missing Data'}, ax=ax2)
    ax2.set_title('Missing Data Heatmap (1K Sample)', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def create_stratified_sample_plot(df: pd.DataFrame, sample_size: int = 12000):
    """Create stratified sample visualization"""
    # Get top products
    product_counts = df['Product_Category'].value_counts()
    top_products = product_counts.head(8).index
    
    # Filter to top products
    filtered_df = df[df['Product_Category'].isin(top_products)].copy()
    
    # Calculate sampling proportions
    proportions = product_counts[top_products] / product_counts[top_products].sum()
    
    # Create stratified sample
    sample_per_product = (proportions * sample_size).round().astype(int)
    
    # Collect samples
    samples = []
    for product in top_products:
        product_data = filtered_df[filtered_df['Product_Category'] == product]
        if len(product_data) >= sample_per_product[product]:
            sample = product_data.sample(n=sample_per_product[product], random_state=42)
        else:
            sample = product_data
        samples.append(sample)
    
    stratified_sample = pd.concat(samples, ignore_index=True)
    
    # Create visualization
    fig = go.Figure(data=[
        go.Bar(
            x=stratified_sample['Product_Category'].value_counts().index,
            y=stratified_sample['Product_Category'].value_counts().values,
            marker_color='#667eea'
        )
    ])
    
    fig.update_layout(
        title=f"Stratified Sample Distribution (n={len(stratified_sample):,})",
        xaxis_title="Product Category",
        yaxis_title="Number of Samples",
        height=400
    )
    
    return stratified_sample, fig

def create_data_quality_dashboard(df: pd.DataFrame, stratified_sample: pd.DataFrame = None):
    """Create comprehensive data quality dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Top Products by Complaint Volume',
            'Missing Data Distribution',
            'Text Length Categories',
            'Stratified Sample Distribution'
        )
    )
    
    # 1. Top products
    top_products = df['Product'].value_counts().head(10)
    fig.add_trace(
        go.Bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            marker_color='steelblue',
            name='Top Products'
        ),
        row=1, col=1
    )
    
    # 2. Missing data
    missing_data = df.isnull().sum().nlargest(10)
    fig.add_trace(
        go.Bar(
            x=missing_data.values,
            y=missing_data.index,
            orientation='h',
            marker_color='lightcoral',
            name='Missing Data'
        ),
        row=1, col=2
    )
    
    # 3. Text length categories
    if 'Consumer complaint narrative' in df.columns:
        text_lengths = df['Consumer complaint narrative'].str.split().str.len()
        bins = [0, 50, 100, 200, 500, 1000, float('inf')]
        labels = ['<50', '50-100', '100-200', '200-500', '500-1000', '>1000']
        
        length_categories = pd.cut(text_lengths, bins=bins, labels=labels).value_counts().sort_index()
        fig.add_trace(
            go.Bar(
                x=length_categories.index,
                y=length_categories.values,
                marker_color='#4ECDC4',
                name='Text Length'
            ),
            row=2, col=1
        )
    
    # 4. Stratified sample distribution
    if stratified_sample is not None and 'Product_Category' in stratified_sample.columns:
        sample_counts = stratified_sample['Product_Category'].value_counts()
        fig.add_trace(
            go.Bar(
                x=sample_counts.index,
                y=sample_counts.values,
                marker_color='#FF6B6B',
                name='Stratified Sample'
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        title_text="Data Quality Dashboard",
        title_font_size=16,
        height=800,
        showlegend=False
    )
    
    return fig