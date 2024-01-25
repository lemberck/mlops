# Sentiment Analysis API Project

## Project Overview

This project is a sentiment analysis application developed using FastAPI, a modern, fast web framework for Python. The application's core functionality is to analyze the sentiment of given text inputs, classifying them as positive, negative, or neutral. It integrates with SQLite for user authentication and storing the results of sentiment analyses.

## Project Structure

- `pyproject.toml`: Contains Poetry dependency configurations.
- `main.py`: The entry point of the FastAPI application.
- `database.py`: Manages database operations, including connection and schema definitions.
- `models.py`: Defines Pydantic models for request and response data structures.
- `sentiment_analysis.py`: Implements the sentiment analysis functionality using Hugging Face's `transformers`.
- `schemas.py`: Contains schemas for serialization and data validation.

## Features

- **Sentiment Analysis**: Leverages a pre-trained model from Hugging Face's `transformers` library for sentiment analysis.
- **User Authentication**: Supports user authentication to access and perform sentiment analysis.
- **Database Integration**: Utilizes SQLite for storing user information and text analysis results.
- **RESTful API Endpoints**: Offers API endpoints for user registration, authentication, text submission, and sentiment analysis.

## Usage

1. **User Registration**: Users can register with their name and password.
2. **Text Submission**: Authenticated users can submit text for sentiment analysis.
3. **Sentiment Analysis**: The submitted text is analyzed, and the sentiment is classified.
4. **Data Storage**: The text and its sentiment analysis result are stored in the database.

## Setup and Installation

- Install dependencies using Poetry: `poetry install`
- Run the application: `uvicorn main:app --reload`

## Endpoints

- `POST /criar_usuario/`: Create a new user.
- `POST /predicao_com_auth/`: Submit a text for sentiment analysis with user authentication.
- `GET /textos`: Retrieve all texts submitted by an authenticated user.



## cURL for Testing

> Note: Change *user_name* and *user_pasword* as needed. 

- Create User:

```bash
curl -X POST "http://127.0.0.1:8000/create_user/" -H "Content-Type: application/json" -d '{"name": "user_name", "password": "user_password"}'
```

- Obtain Prediction:

```bash
curl -X POST "http://127.0.0.1:8000/prediction_with_auth/" -H "Content-Type: application/json" -H "name: user_name" -H "password: user_password" -d '{"text": "This course is very good"}'
```