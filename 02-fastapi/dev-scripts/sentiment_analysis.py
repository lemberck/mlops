# This script will handle the loading and execution of the sentiment analysis model.

from transformers import pipeline

# load the sentiment classification model using the 'pipeline' function and store it in 'SENTIMENT_CLASSIFIER'
SENTIMENT_CLASSIFIER = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """
    Analyze the sentiment of the provided text.

    Args:
        text (str): Text to analyze.

    Returns:
        A dictionary containing the prediction label and score.
    """
    # use the loaded sentiment analysis model to predict the sentiment of the provided text
    prediction = SENTIMENT_CLASSIFIER(text)

    # return the first prediction result (the model can return multiple predictions, one for each input text)
    return prediction[0]