""" This script will handle the loading and
execution of the sentiment analysis model."""

from transformers import pipeline

# Load sentiment classification model
SENTIMENT_CLASSIFIER = pipeline("sentiment-analysis")


def analyze_sentiment(text):
    """
    Analyze the sentiment of the provided text.

    Args:
        text (str): Text to analyze.

    Returns:
        A dictionary containing the prediction label and score.
    """

    prediction = SENTIMENT_CLASSIFIER(text)
    return prediction[0]
