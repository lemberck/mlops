import pytest
import sqlite3
from backend.auth import authenticate_user  # Adjust the import path as necessary

@pytest.fixture(scope="module")
def db():
    """Set up an in-memory SQLite database for testing."""
    connection = sqlite3.connect(':memory:')
    # Ensure the table is created immediately and committed.
    with connection:
        connection.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        # Insert a test user
        connection.execute("INSERT INTO users (name, password) VALUES (?, ?)", ("test_user", "test_password"))
    
    yield connection  # Yield the connection for tests to use

    # Cleanup is automatic for in-memory databases when the connection is closed
    connection.close()


@pytest.fixture(scope="function")
def db_cursor(db):
    """Provide a fresh cursor for each test function."""
    yield db.cursor()
    db.commit()

def test_authenticate_user_success(db_cursor):
    """Test successful authentication with correct user credentials."""
    # Attempt to authenticate with the correct username and password
    user = authenticate_user("test_user", "test_password")
    # Ensure the authentication was successful
    assert user is not None
    assert user[1] == "test_user"  # Assuming the second element is the username

def test_authenticate_user_failure_incorrect_password(db_cursor):
    """Test unsuccessful authentication with an incorrect password."""
    # Attempt to authenticate with the correct username but incorrect password
    user = authenticate_user("test_user", "wrong_password")
    # Ensure the authentication failed
    assert user is None

def test_authenticate_user_failure_nonexistent_user(db_cursor):
    """Test unsuccessful authentication with a nonexistent username."""
    # Attempt to authenticate with a username that does not exist
    user = authenticate_user("nonexistent_user", "any_password")
    # Ensure the authentication failed
    assert user is None

