# Authentication API

This API is responsible for authenticating users via Google, Github or LinkedIn. The user is redirected to the respective login page and upon successful login, the user is redirected back to the application.

### Google API Authentication

Using OAuth 2.0, the user is authenticated via Google. The user is redirected to the Google login page and upon successful login, the user is redirected back to the application.

### Github API Authentication

Using Oath, the user is authenticated via Github. The user is redirected to the Github login page and upon successful login, the user is redirected back to the application

### LinkedIn API Authentication

Using OAuth 2.0, the user is authenticated via LinkedIn. The user is redirected to the LinkedIn login page and upon successful login, the user is redirected back to the application.

### Database

In order to create a local MySQL database, run the following command on your terminal:

```bash
brew services start mysql
brew info mysql
mysql -u root
mysql> CREATE DATABASE IAMDATABASE;
mysql> USE IAMDATABASE;
mysql> CREATE TABLE users (     id INT AUTO_INCREMENT PRIMARY KEY,     username VARCHAR(255) NOT NULL,     github_id VARCHAR(255),     linkedin_id VARCHAR(255),     google_id VARCHAR(255) );
```

### Backoffice

In order to configure the authentication API, run the following command:

```bash
python3 backoffice.py
```

Now open the backoffice in your browser at `http://127.0.0.1:5002/` and configure the authentication API with the authentication providers you wish.

### Run the Application

```bash
docker build -t iam_washify .
docker run -d -p 8000:5000 iam_washify
```

Now open the application in your browser at `http://localhost:8000/`.

