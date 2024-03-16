# Authentication API

This API is responsible for authenticating users via Google, Github or LinkedIn. The user is redirected to the respective login page and upon successful login, the user is redirected back to the application.

## Google API Authentication

Using OAuth 2.0, the user is authenticated via Google. The user is redirected to the Google login page and upon successful login, the user is redirected back to the application.

## Github API Authentication

Using Oath, the user is authenticated via Github. The user is redirected to the Github login page and upon successful login, the user is redirected back to the application

## LinkedIn API Authentication

Using OAuth 2.0, the user is authenticated via LinkedIn. The user is redirected to the LinkedIn login page and upon successful login, the user is redirected back to the application.

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

Now open the backoffice in your browser at `http://127.0.0.1:5002/` and configure the authentication API with the authentication providers you wish.

### Run the Application

In order to run the application, run the following command:

```bash
python3 iamService.py
```

Now open the application in your browser at `http://127.0.0.1:5000/`.


## QUESTION
se o user escolhe apenas google e github, ao verificar o swagger ui ele deve ver todos os métodos dos provedores ou apenas os escolhidos?

