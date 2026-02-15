"""Data loading utilities for large datasets"""
import pandas as pd
import logging
from typing import Optional, Generator
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Optimized data types for memory efficiency
DTYPE_STRATEGY = {
    'Complaint ID': 'str',
    'Date received': 'str',
    'Product': 'category',
    'Sub-product': 'category',
    'Issue': 'category',
    'Sub-issue': 'category',
    'Company': 'category',
    'State': 'category',
    'ZIP code': 'str',
    'Tags': 'category',
    'Consumer consent provided?': 'category',
    'Submitted via': 'category',
    'Company response to consumer': 'category',
    'Timely response?': 'category',
    'Consumer disputed?': 'category',
    'Consumer complaint narrative': 'object'
}

CHUNK_SIZE = 50000

def load_complaints_data(filepath: str, sample_size: Optional[int] = None) -> pd.DataFrame:
    """
    Load complaints data efficiently with memory optimization
    
    Parameters:
    -----------
    filepath : str
        Path to the complaints CSV file
    sample_size : int, optional
        If provided, load only this many rows for testing
    
    Returns:
    --------
    pd.DataFrame
        Loaded complaints data
    """
    try:
        if sample_size:
            # Load sample for testing
            logger.info(f"📊 Loading sample of {sample_size:,} records...")
            df = pd.read_csv(
                filepath,
                dtype=DTYPE_STRATEGY,
                parse_dates=['Date received'],
                nrows=sample_size
            )
            logger.info(f"✅ Loaded sample: {len(df):,} records")
            return df
        
        # Load full dataset in chunks
        logger.info("🚀 Loading complaint database...")
        chunks = []
        total_rows = 0
        
        for i, chunk in enumerate(pd.read_csv(
            filepath,
            dtype=DTYPE_STRATEGY,
            parse_dates=['Date received'],
            chunksize=CHUNK_SIZE
        )):
            chunks.append(chunk)
            total_rows += len(chunk)
            
            # Progress update every 5 chunks
            if (i + 1) % 5 == 0:
                logger.info(f"   📊 Chunk {i+1}: {total_rows:,} records loaded")
        
        # Combine all chunks
        df = pd.concat(chunks, ignore_index=True)
        logger.info(f"✅ Loaded complete dataset: {len(df):,} records")
        
        # Memory usage info
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        logger.info(f"💾 Memory usage: {memory_mb:.1f} MB")
        
        return df
    
    except FileNotFoundError:
        logger.error(f"❌ File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"❌ Error loading data: {e}")
        raise

def stream_complaints(filepath: str) -> Generator[pd.DataFrame, None, None]:
    """
    Stream complaints data in chunks without loading all into memory
    
    Parameters:
    -----------
    filepath : str
        Path to the complaints CSV file
    
    Yields:
    -------
    pd.DataFrame
        Chunk of complaints data
    """
    logger.info("🚀 Streaming complaints data...")
    
    for i, chunk in enumerate(pd.read_csv(
        filepath,
        dtype=DTYPE_STRATEGY,
        parse_dates=['Date received'],
        chunksize=CHUNK_SIZE
    )):
        if i == 0:
            logger.info(f"📦 Streaming in chunks of {CHUNK_SIZE:,} records")
        yield chunk
    
    logger.info("✅ Streaming complete")

def filter_complaints_streaming(filepath: str, product_mapping: dict, target_products: list) -> pd.DataFrame:
    """
    Filter complaints while streaming - most memory efficient for large datasets
    
    Parameters:
    -----------
    filepath : str
        Path to the complaints CSV file
    product_mapping : dict
        Dictionary mapping raw product names to categories
    target_products : list
        List of target product categories to keep
    
    Returns:
    --------
    pd.DataFrame
        Filtered complaints with narratives
    """
    logger.info("🚀 Streaming filtering of complaints...")
    
    filtered_chunks = []
    total_processed = 0
    total_filtered = 0
    
    for i, chunk in enumerate(pd.read_csv(
        filepath,
        dtype=DTYPE_STRATEGY,
        parse_dates=['Date received'],
        chunksize=CHUNK_SIZE
    )):
        total_processed += len(chunk)
        
        # Apply product mapping
        chunk['Product_Category'] = chunk['Product'].map(product_mapping).fillna('Other')
        
        # Filter to target products AND narratives
        chunk_filtered = chunk[
            chunk['Product_Category'].isin(target_products) & 
            chunk['Consumer complaint narrative'].notna()
        ].copy()
        
        if len(chunk_filtered) > 0:
            filtered_chunks.append(chunk_filtered)
            total_filtered += len(chunk_filtered)
        
        # Progress update every 10 chunks
        if (i + 1) % 10 == 0:
            logger.info(f"   📊 Chunk {i+1}: Processed {total_processed:,} → Kept {total_filtered:,} ({total_filtered/total_processed*100:.1f}%)")
    
    # Combine filtered chunks
    result = pd.concat(filtered_chunks, ignore_index=True) if filtered_chunks else pd.DataFrame()
    logger.info(f"✅ Streaming complete: {len(result):,} relevant complaints")
    
    return result

def load_with_optimized_types(filepath: str, usecols: Optional[list] = None) -> pd.DataFrame:
    """
    Load only necessary columns for even better memory optimization
    
    Parameters:
    -----------
    filepath : str
        Path to the complaints CSV file
    usecols : list, optional
        List of columns to load (None loads all)
    
    Returns:
    --------
    pd.DataFrame
        Loaded complaints data
    """
    # Filter dtype strategy to only requested columns
    if usecols:
        dtype_subset = {col: DTYPE_STRATEGY[col] for col in usecols if col in DTYPE_STRATEGY}
    else:
        dtype_subset = DTYPE_STRATEGY
        usecols = list(DTYPE_STRATEGY.keys())
    
    logger.info(f"🚀 Loading selected columns: {usecols}")
    
    df = pd.read_csv(
        filepath,
        dtype=dtype_subset,
        parse_dates=['Date received'] if 'Date received' in usecols else False,
        usecols=usecols
    )
    
    logger.info(f"✅ Loaded {len(df):,} records with {len(df.columns)} columns")
    
    # Memory usage info
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    logger.info(f"💾 Memory usage: {memory_mb:.1f} MB")
    
    return df

def get_data_info(filepath: str) -> dict:
    """
    Get basic information about the dataset without loading it
    
    Parameters:
    -----------
    filepath : str
        Path to the complaints CSV file
    
    Returns:
    --------
    dict
        Dataset information
    """
    # Read just the first row to get columns
    first_row = pd.read_csv(filepath, nrows=0)
    
    # Count total rows (approximate for large files)
    import subprocess
    import platform
    
    info = {
        'columns': list(first_row.columns),
        'num_columns': len(first_row.columns),
        'file_path': filepath
    }
    
    # Get file size
    file_size_bytes = Path(filepath).stat().st_size
    info['file_size_mb'] = file_size_bytes / 1024 / 1024
    
    # Try to count rows (platform dependent)
    try:
        if platform.system() == 'Windows':
            # Windows: use find command
            result = subprocess.run(['find', '/c', '/v', '', filepath], 
                                  capture_output=True, text=True, shell=True)
            # Parse the output
            import re
            match = re.search(r': (\d+)$', result.stdout.strip())
            if match:
                # Subtract 1 for header row
                info['approx_rows'] = int(match.group(1)) - 1
        else:
            # Unix: use wc -l
            result = subprocess.run(['wc', '-l', filepath], 
                                  capture_output=True, text=True)
            # Subtract 1 for header row
            info['approx_rows'] = int(result.stdout.split()[0]) - 1
    except:
        info['approx_rows'] = 'Unknown'
    
    logger.info(f"📁 File: {Path(filepath).name}")
    logger.info(f"📊 Columns: {info['num_columns']}")
    logger.info(f"💾 Size: {info['file_size_mb']:.1f} MB")
    logger.info(f"📈 Approx rows: {info['approx_rows']}")
    
    return info