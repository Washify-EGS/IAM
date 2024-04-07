from datetime import datetime, timedelta
import mysql.connector
import logging

def connect_to_mysql():
    # Connect to MySQL server
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password=""  
    )

def create_database(cursor):    
    # Create database "IAMDATABASE" if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS IAMDATABASE")

def create_users_table(cursor):
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            username VARCHAR(255) NOT NULL, 
            github_id VARCHAR(255), 
            linkedin_id VARCHAR(512), 
            google_id VARCHAR(512), 
            email VARCHAR(255), 
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

def connect_to_database():
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    
    create_database(cursor)
    mydb.database = "IAMDATABASE"
    create_users_table(cursor)

    return mydb

def insert_user(username, github_id=None, linkedin_id=None, google_id=None, email=None):
    mydb = connect_to_database()
    cursor = mydb.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND email = %s", (username, email))
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute("INSERT INTO users (username, github_id, linkedin_id, google_id, email, last_login) VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, github_id, linkedin_id, google_id, email, datetime.now()))
            mydb.commit()
            print(f"User '{username}' inserted successfully.")
        else:
            # Update last login datetime
            cursor.execute("UPDATE users SET last_login = %s WHERE username = %s OR email = %s",
                           (datetime.now(), username, email))
            mydb.commit()
            print(f"User '{username}' updated successfully.")
    except Exception as e:
        logging.error(f"Error inserting user '{username}': {e}")
        mydb.rollback()
    finally:
        mydb.close()

def get_last_logged_in_user():
    mydb = connect_to_database()
    cursor = mydb.cursor(dictionary=True)

    try:
        # Calculate the timestamp 30 seconds ago
        thirty_seconds_ago = datetime.now() - timedelta(seconds=30)
        
        # Execute the SQL query with the WHERE clause to filter records
        cursor.execute("SELECT * FROM users WHERE last_login >= %s ORDER BY last_login DESC LIMIT 1", (thirty_seconds_ago,))
        
        # Fetch the user data
        user = cursor.fetchone()
        print(f"Last logged-in user: {user}")
        return user
    except Exception as e:
        logging.error(f"Error fetching last logged-in user: {e}")
    finally:
        mydb.close()
