### Initialize Poetry

Navigate to the project's root directory in the terminal and run:

```poetry init ```

### Poetry configuration
Specify the URL where the  CPU-only wheels for PyTorch are located, reducing size considerably (no GPU needed):

```poetry source add -p explicit pytorch https://download.pytorch.org/whl/cpu```

### Adding Dependencies
Use poetry to add the dependencies of the project:

```poetry add --source pytorch torch torchvision```

```poetry add fastapi uvicorn pydantic transformers ```

> Note: sqlite3 is already included in Python standard library

### Develop scripts
- database.py - Handles the database connection and table creation.
- auth.py - Function to authenticate a user.
- models.py - Pydantic models that define the structure and validation rules for data of requests and responses.
- sentiment_analysis - Handles the loading and execution of the sentiment analysis model.
- main.py - The entry point to the FastAPI application and will tie everything together.

### Test the application
1. Run the application : 

```uvicorn main:app --reload```

2. In another terminal, run the tests with cURL
#### Test 1 - Create user's credentials : 

```curl -X POST "http://127.0.0.1:8000/create_user/" -H "Content-Type: application/json" -d '{"name": "test_1", "password": "test1_pass"}'; echo```

    - Expected : {"message":"User created successfully"}

#### Test 2 - Try to create the same user's credential, but with different password

```curl -X POST "http://127.0.0.1:8000/create_user/" -H "Content-Type: application/json" -d '{"name": "test_1", "password": "test1111_pass"}'; echo```

    - Expected : {"detail":"User already exists"}


#### Test 3 : Get predictions for the created user

```curl -X POST "http://127.0.0.1:8000/prediction_with_auth/" -H "Content-Type: application/json" -H "name: test_1" -H "password: test1_pass" -d '{"text": "your coding skills are not enough"}'; echo```

    - Expected : {"prediction":"NEGATIVE","score":0.9997252821922302}

```curl -X POST "http://127.0.0.1:8000/prediction_with_auth/" -H "Content-Type: application/json" -H "name: test_1" -H "password: test1_pass" -d '{"text": "Your cat is awesome!"}'; echo```

    - Expected : {"prediction":"POSITIVE","score":0.9998716115951538}

#### Test 4 : Get the list of registered users (does not need authentication)

```curl -X GET "http://127.0.0.1:8000/users"; echo```

    - Expected : A list with the registered users, no duplicates.

#### Test 5 : Get texts sent by a registered user (needs authentication)

```curl -X GET "http://127.0.0.1:8000/texts" -H "name: test_1" -H "password: test1_pass"; echo```

    - Expected : A list with the messages sent by user *test_1*

#### Test 6 : Get predictions for a user that is not registered or the password is wrong

```curl -X POST "http://127.0.0.1:8000/prediction_with_auth/" -H "Content-Type: application/json" -H "name: test_2" -H "password: test1_pass" -d '{"text": "Your cat is awesome!"}'; echo```

```curl -X POST "http://127.0.0.1:8000/prediction_with_auth/" -H "Content-Type: application/json" -H "name: test_1" -H "password: test11111_pass" -d '{"text": "Your cat is awesome!"}'; echo```

    - Expected : {"detail":"User not authenticated"}


### Install Dependencies only
Navigate to the project's root directory in the terminal and run:

```poetry install --no-root```

This installs only the dependencies from the pyproject.toml and not the project package itself.
