# This script is the entry point to the FastAPI application and will tie everything together.

import uvicorn
from fastapi import FastAPI, HTTPException, Header
from typing import List
import sqlite3

# import created modules
from models import User, Prediction, Text
from database import create_conn, setup_database
from sentiment_analysis import analyze_sentiment
from auth import authenticate_user

# Initialize FastAPI application
app = FastAPI()

# Call the function to set up the database
# This ensures that tables are created before the application starts serving requests.
setup_database()

# response_model is used to specify the schema of the response data. 
# FastAPI will automatically serialize the return value of the route 
# function to match the structure of the specified model.

# Header is used to extract data from the request headers. 
# Here it is used for passing and accessing authentication credentials like the user's name and password.

'''
## FastAPI Parameter Types and Why Use Headers for Authentication

FastAPI offers various parameter types for different purposes:

1. **Path Parameters**: 
   - Capture values from the URL path.
   - Part of the route URL.
   - *Example*: `@app.get("/items/{item_id}")`, where `item_id` is a path parameter.

2. **Query Parameters**:
   - Capture values in the query string of the URL.
   - Directly accessed in function parameters.
   - *Example*: Request to `/items?name=widget`, where `name` is a query parameter.

3. **Request Body**:
   - Receive data in the request's body, usually for complex data like JSON.
   - Accessed via Pydantic models.
   - *Example*: `@app.post("/items/")` receiving a Pydantic model instance in the body.

4. **Form Fields**:
   - For receiving form data.
   - Accessed using `Form(...)` in function parameters.

5. **Cookies**:
   - Receive data sent in HTTP request cookies.
   - Accessed using `Cookie(...)` in function parameters.

6. **Header Parameters**:
   - Access specific data sent in HTTP headers.
   - Suitable for metadata like authentication tokens.
   - Accessed using `Header(...)`.

7. **File Uploads**:
   - Receive uploaded files.
   - Accessed using `File(...)` and `UploadFile`.

### Why Use `Header` for Authentication?

- **Security**: Headers are not part of the URL (which can be logged) or body (for business data), making them secure for sensitive data like tokens.
- **Standardization**: Many authentication standards utilize headers, aiding integration with common tools and practices.
- **Separation of Concerns**: Keeps the API's body and URL clean for actual business data.

Using headers for authentication offers advantages in security and standardization, making them a preferred choice for transmitting control information like authentication tokens.
'''

# define an api endpoint for creating a new user in the database
# Not adding the User model to the decorator so it wont return the password as well, for security measures.
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

# define an api endpoint (route) for making sentiment predictions with authentication
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

# define another api endpoint for retrieving a list of registered users from the database
# no authentication required
# 'response_model=List[str]' tells fastapi to expect a list of strings as the response
# which is also used for automatic response validation and documentation
@app.get("/users", response_model=List[str])
def get_users():
    """
    Retrieve all user names from the database.

    Returns:
        List[str]: A list of user names.
    """
    conn, cursor = create_conn()
    cursor.execute("SELECT name FROM users")
    # fetch all results of the query; each row contains a tuple with one element (the user name)
    users = cursor.fetchall()
    conn.close()
    # use a list comprehension to iterate through the list of tuples
    # extract the first element from each tuple, which is the user name, and create a list of these names
    # the list of user names is what's returned by the function (expected by the response_model)
    return [user[0] for user in users]

# define another api endpoint for retrieving saved texts of the registered user from the database
# 'response_model=List[Text]' indicates that the response is a list of items conforming to the Text model
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
    # fetch all the results from the database as tuples
    texts = cursor.fetchall()
    conn.close()

    # transform the list of tuples fetched from the database into a list of Text model instances
    # the text field in each tuple is used to create a Text instance
    # this list of Text instances is then returned as the response (expected by response_model)
    return [Text(text=t['text']) for t in texts]


# run the application using uvicorn when this script is executed directly
if __name__ == "__main__":
    # setup_database()  # Set up database tables ## This is not executed when app is run with 'uvicorn main:app --reload'. Taking to just after initializing the app.

    # this function call starts the uvicorn server with the fastapi application
    # 'app' is the instance of the fastapi app that we created and where we defined all our endpoints
    # the host '0.0.0.0' makes the server accessible on the local network
    # the application will be accessible on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # you can access the application by going to 'http://127.0.0.1:8000' in a web browser,
    # or 'http://<local_machine_ip>:8000' if accessing from another machine on the network
    # where <local_machine_ip> is the ip address of the machine where the server is running

"""
Note to prevent SQL injection: 
Uses '?' placeholders to inject 'name' and 'password' into the SQL query.
This prevents SQL injection, where attackers can alter queries to access unauthorized data.
This way, even if the input includes SQL commands, they will be treated as a string value rather than part of the SQL statement.
Example of SQL Injection:
--> If an attacker inputs : SELECT * FROM users WHERE username = 'admin' --' AND password = '';
Here, -- is a comment indicator in SQL, which makes the database ignore the rest of the query. 
This effectively logs the attacker in as admin without needing to know the password.
"""