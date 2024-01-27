# This script will contain the function to authenticate a user.

from database import create_conn

def authenticate_user(name: str, password: str):
    """
    Authenticate a user based on name and password.

    Args:
        name (str): The name of the user.
        password (str): The password of the user.

    Returns:
        A user object if authentication is successful, None otherwise.
    """
    conn, cursor = create_conn()
    cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
    user = cursor.fetchone()
    conn.close()
    return user