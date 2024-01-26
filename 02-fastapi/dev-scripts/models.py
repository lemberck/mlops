# This script contains the Pydantic models that define the structure and validation rules for data of requests and responses.

# Pydantic models are used here to ensure that the data conforms to the expected format, which helps in avoiding 
# common data-related errors and makes the code more robust and maintainable.

from pydantic import BaseModel

class User(BaseModel):
    """Data model that represents a user's authentication information."""
    # define a string field for the user's name and password
    name: str
    password: str

class Prediction(BaseModel):
    """Data model that holds the sentiment analysis prediction and its confidence score."""
    # define a string field for the model's prediction and a float field for the model's calculated score
    prediction: str
    score: float

class Text(BaseModel):
    """Data model that encapsulates the text data for analysis."""
    # define a string field for the text data that will be analyzed
    text: str
