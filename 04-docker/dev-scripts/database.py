# This script handles the database connection and table creation.

# import the sqlite3 module to work with sqlite databases
import sqlite3

# define the path to the database file
DATABASE_PATH = "database.db"

def create_conn():
    """Create a database connection and return both the connection and cursor."""
    
    # establish a connection to the sqlite database specified by DATABASE_PATH
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    # create a cursor object to interact with the database
    cursor = conn.cursor()

    return conn, cursor

def create_tables(cursor):
    """Create tables in the database."""
    # execute an sql command to create a 'texts' table if it does not exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS texts ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            text TEXT NOT NULL,
            classification TEXT NOT NULL
        );
        """
    )

    # execute an sql command to create a 'users' table if it does not exist
    # Add UNIQUE constraint to the name column to prevent duplicate entries
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
    )

def setup_database():
    """Set up the database by creating tables."""
    # create a database connection and cursor
    conn, cursor = create_conn()

    # call the function to create tables
    create_tables(cursor)

    # commit any changes made to the database
    conn.commit()

    # close the connection to the database
    conn.close()
