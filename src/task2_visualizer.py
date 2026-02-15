"""Visualization utilities for Task 2"""
import matplotlib.pyplot as plt
import numpy as np
from .task2_config import REPORTS_DIR

def plot_text_distribution(chunks_df, chunk_size, save=True):
    """Plot text length distribution"""
    plt.figure(figsize=(10, 5))
    
    lengths = chunks_df['chunk_length'].values
    
    plt.hist(lengths, bins=50, color='#3498db', alpha=0.7, edgecolor='black')
    plt.axvline(chunk_size, color='red', linestyle='--', label=f'Chunk Size ({chunk_size})')
    plt.axvline(np.median(lengths), color='green', linestyle='-', label=f'Median: {np.median(lengths):.0f}')
    
    plt.xlabel('Chunk Length (characters)')
    plt.ylabel('Number of Chunks')
    plt.title('Chunk Length Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save:
        plt.savefig(REPORTS_DIR / 'chunk_distribution.png', dpi=150, bbox_inches='tight')
    plt.show()

def plot_chunks_per_complaint(chunks_df, save=True):
    """Plot chunks per complaint distribution"""
    plt.figure(figsize=(10, 5))
    
    chunks_per = chunks_df.groupby('complaint_id').size()
    
    plt.hist(chunks_per, bins=30, color='#2ecc71', alpha=0.7, edgecolor='black')
    plt.axvline(chunks_per.mean(), color='red', linestyle='--', label=f'Mean: {chunks_per.mean():.2f}')
    
    plt.xlabel('Number of Chunks per Complaint')
    plt.ylabel('Number of Complaints')
    plt.title('Chunks per Complaint Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save:
        plt.savefig(REPORTS_DIR / 'chunks_per_complaint.png', dpi=150, bbox_inches='tight')
    plt.show()