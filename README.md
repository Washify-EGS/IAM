# Authentication API

This API is responsible for authenticating users via Google and Github

## Google API Authentication

Using OAuth 2.0, the user is authenticated via Google. The user is redirected to the Google login page and upon successful login, the user is redirected back to the application. The user's information is then stored in the database.

## Github API Authentication

Using Oath, the user is authenticated via Github. The user is redirected to the Github login page and upon successful login, the user is redirected back to the application. The user's information is then stored in the database.

### Start Virtual Environment

In order to start the virtual environment, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Backoffice

In order to configure the authentication API, run the following command:

```bash
python3 backoffice.py
```

Now open the backoffice in your browser at `http://127.0.0.1:5001/` and configure the authentication API with the authentication providers you wish.

### Run the Application

In order to run the application, run the following command:

```bash
python3 iamService.py
```

Now open the application in your browser at `http://127.0.0.1:5000/`.



