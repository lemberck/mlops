# This script contains the Pydantic models that define the structure of requests and responses.

from pydantic import BaseModel

class User(BaseModel):
    """Data model that represents a user's authentication information."""
    name: str
    password: str

class Prediction(BaseModel):
    """Data model that holds the sentiment analysis prediction and its confidence score."""
    prediction: str
    score: float

class Text(BaseModel):
    """Data model that encapsulates the text data for analysis."""
    text: str
