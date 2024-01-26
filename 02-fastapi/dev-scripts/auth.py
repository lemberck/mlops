# This script will contain the function to authenticate a user.

# import the function 'create_conn' from the created 'database' module
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
    # establish a connection to the database and create a cursor
    conn, cursor = create_conn()

    # execute an sql query to find a user with the provided name and password
    cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
    # fetch one record (user) from the query result
    user = cursor.fetchone()
    # close the database connection
    conn.close()
    # return the user object if found, or none if not found
    return user

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