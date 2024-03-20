import mysql.connector

def connect_to_mysql():
    # Connect to MySQL server
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Assuming the user is root
        password=""   # No password specified
    )

def create_database(cursor):
    # Create a new database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS IAMDATABASE")

def create_users_table(cursor):
    # Create the users table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, github_id VARCHAR(255), linkedin_id VARCHAR(512), google_id VARCHAR(512))")

def connect_to_database():
    mydb = connect_to_mysql()
    cursor = mydb.cursor()

    # Create database and users table if they don't exist
    create_database(cursor)
    mydb.database = "IAMDATABASE"
    create_users_table(cursor)

    return mydb

def insert_user(username, github_id=None, linkedin_id=None, google_id=None):
    mydb = connect_to_database()
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        cursor.execute("INSERT INTO users (username, github_id, linkedin_id, google_id) VALUES (%s, %s, %s, %s)",
                       (username, github_id, linkedin_id, google_id))
        mydb.commit()
        print(f"User '{username}' inserted successfully.")
    else:
        print(f"User '{username}' already exists in the database.")

    mydb.close()

# Create the database and users table if they don't exist
connect_to_database()
