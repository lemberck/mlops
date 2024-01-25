# Sentiment Analysis API Project

## Project Overview

This project is a sentiment analysis application developed using FastAPI, a modern, fast web framework for Python. The application's core functionality is to analyze the sentiment of given text inputs, classifying them as positive, negative, or neutral. It integrates with SQLite for user authentication and storing the results of sentiment analyses.

## Project Structure

- `pyproject.toml`: Contains Poetry dependency configurations.
- `main.py`: The entry point of the FastAPI application.
- `auth.py` : Holds the function to authenticate a user.
- `database.py`: Manages database operations, including connection and schema definitions.
- `models.py`: Defines Pydantic models for request and response data structures.
- `sentiment_analysis.py`: Implements the sentiment analysis functionality using Hugging Face's `transformers`.

## Features

- **Sentiment Analysis**: Leverages a pre-trained model from Hugging Face's `transformers` library for sentiment analysis.
- **User Authentication**: Supports user authentication to access and perform sentiment analysis.
- **Database Integration**: Uses SQLite for storing user information and text analysis results.
- **RESTful API Endpoints**: Offers API endpoints for user registration, authentication, text submission, and sentiment analysis.

## Usage

1. **User Registration**: Users can register with their name and password.
2. **Text Submission**: Authenticated users can submit text for sentiment analysis.
3. **Sentiment Analysis**: The submitted text is analyzed, and the sentiment is classified.
4. **Data Storage**: The text and its sentiment analysis result are stored in the database.

## API documentation
With the application running, access ```http://127.0.0.1:8000/docs```  or  ```http://127.0.0.1:8000/redoc```


## Setup and Installation

- Install only dependencies using Poetry: `poetry install --no-root`
- Run the application: `uvicorn main:app --reload`

## Endpoints

- `POST /create_user/`: Create a new user.
- `POST /prediction_with_auth/`: Submit a text for sentiment analysis with user authentication.
- `GET /users`: Retrieve all authenticated users.
- `GET /texts`: Retrieve all texts submitted by an authenticated user.


## Using the App

> Note: Change *name*, *pasword* and *text* as desired. 
### Navigate to prd-scripts, then:

#### Initiate App

`just start-app`

#### Create User:

`just create-user name='your-user-here' password='your-password-here' `

#### Obtain Prediction:

`just classify-text name='default_user_name' password='default_user_password' text='Your text here'`

#### Get list of registered users

`just get-users`

#### Get list of texts sent by a registered user

`just get-texts name='' password=''`