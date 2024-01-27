# This script is the entry point to the FastAPI application and will tie everything together.

import uvicorn
from fastapi import FastAPI, HTTPException, Header
from typing import List
import sqlite3

from models import User, Prediction, Text
from database import create_conn, setup_database
from sentiment_analysis import analyze_sentiment
from auth import authenticate_user

# Initialize FastAPI application
app = FastAPI()

# Call the function to set up the database
# This ensures that tables are created before the application starts serving requests.
setup_database()

@app.post("/create_user/")
def create_user(user: User):
    """
    Create a new user in the database.

    Args:
        user (User): User data.

    Returns:
        dict: Dictionary with a message about the user creation.
    """
    conn, cursor = create_conn()
    try:
        cursor.execute(
            "INSERT INTO users (name, password) VALUES (?, ?)",
            (user.name, user.password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()

    return {"message": "User created successfully"}

@app.post("/prediction_with_auth/", response_model=Prediction)
def predict(text: Text, name: str = Header(None), password: str = Header(None)):
    """
    Perform sentiment prediction with authentication.

    Args:
        text (Text): Text to be analyzed.
        name (str, optional): Name of the user. Defaults to Header(None).
        password (str, optional): Password of the user. Defaults to Header(None).

    Raises:
        HTTPException: If user authentication fails.

    Returns:
        Prediction: Prediction result with label and score.
    """
    # Authenticate user
    user = authenticate_user(name, password)
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Perform sentiment analysis
    prediction_result = analyze_sentiment(text.text)

    # Save prediction in the database
    conn, cursor = create_conn()
    cursor.execute(
        "INSERT INTO texts (name, text, classification) VALUES (?, ?, ?)",
        (name, text.text, prediction_result['label'])
    )
    conn.commit()
    conn.close()

    return Prediction(prediction=prediction_result["label"], score=prediction_result["score"])

@app.get("/users", response_model=List[str])
def get_users():
    """
    Retrieve all user names from the database.

    Returns:
        List[str]: A list of user names.
    """
    conn, cursor = create_conn()
    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    conn.close()
    # Convert to List
    return [user[0] for user in users]

@app.get("/texts", response_model=List[Text])
def get_texts(name: str = Header(None), password: str = Header(None)):
    """
    Retrieve all texts from the database for an authenticated user.

    Args:
        name (str, optional): Name of the user. Defaults to Header(None).
        password (str, optional): Password of the user. Defaults to Header(None).

    Raises:
        HTTPException: If user authentication fails.

    Returns:
        List[Text]: List of texts.
    """
    # Authenticate user
    user = authenticate_user(name, password)
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Retrieve all texts from the database
    conn, cursor = create_conn()
    cursor.execute("SELECT text FROM texts WHERE name = ?", (name,))
    texts = cursor.fetchall()
    conn.close()

    return [Text(text=t[0]) for t in texts]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
