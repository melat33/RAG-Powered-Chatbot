"""Text processing utilities"""
import re
import pandas as pd
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def clean_text_batch(texts: pd.Series) -> pd.Series:
    """
    Fast batch text cleaning without NLTK
    """
    # Convert to string and lowercase
    cleaned = texts.fillna("").astype(str).str.lower()

    # Remove PII and patterns
    patterns = [
        (r"\S+@\S+", " "),  # Emails
        (r"http\S+|www\.\S+", " "),  # URLs
        (r"\d{3}-\d{2}-\d{4}", " "),  # SSN
        (r"\b\d{10,}\b", " "),  # Long numbers
        (r"xxxx", " "),  # Common placeholder
        (r"[^\w\s]", " "),  # Remove special chars
        (r"\s+", " "),  # Remove extra spaces
    ]

    for pattern, replacement in patterns:
        cleaned = cleaned.str.replace(pattern, replacement, regex=True)

    return cleaned.str.strip()


def analyze_vocabulary(texts: pd.Series, top_n: int = 20) -> dict:
    """Analyze vocabulary from text series"""
    all_words = []
    for text in texts.dropna():
        tokens = str(text).lower().split()
        all_words.extend(tokens)

    word_counts = {}
    for word in all_words:
        if word.isalpha():  # Only keep words with letters
            word_counts[word] = word_counts.get(word, 0) + 1

    # Get top words
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:top_n]

    return {
        "total_words": len(all_words),
        "unique_words": len(word_counts),
        "vocabulary_richness": len(word_counts) / len(all_words) if all_words else 0,
        "top_words": top_words,
    }


def calculate_sentiment_simple(texts: pd.Series) -> pd.Series:
    """Simple sentiment analysis based on negative words"""
    negative_words = {
        "fraud",
        "unauthorized",
        "charged",
        "overdraft",
        "fees",
        "error",
        "mistake",
        "wrong",
        "problem",
        "issue",
        "complaint",
        "dispute",
    }

    def text_sentiment(text):
        if pd.isna(text):
            return 0
        text_lower = str(text).lower()
        negative_count = sum(1 for word in negative_words if word in text_lower)
        word_count = len(text_lower.split())
        return -negative_count / max(word_count, 1)

    return texts.apply(text_sentiment)
