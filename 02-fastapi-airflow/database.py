# This script handles the database connection and table creation.

import sqlite3

DATABASE_PATH = "database.db"

def create_conn():
    """Create a database connection and return both the connection and cursor."""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):
    """Create tables in the database."""
    # Create a table for texts
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS textos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            texto TEXT NOT NULL,
            classificacao TEXT NOT NULL
        );
        """
    )

    # Create a table for users with name and password
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        );
        """
    )

def setup_database():
    """Set up the database by creating tables."""
    conn, cursor = create_conn()
    create_tables(cursor)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
