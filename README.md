# Authentication API

This API is responsible for authenticating users via Google, Github or LinkedIn. The user is redirected to the respective login page and upon successful login, the user is redirected back to the application.

### Google API Authentication

Using OAuth 2.0, the user is authenticated via Google. The user is redirected to the Google login page and upon successful login, the user is redirected back to the application.

### Github API Authentication

Using Oath, the user is authenticated via Github. The user is redirected to the Github login page and upon successful login, the user is redirected back to the application

### LinkedIn API Authentication

Using OAuth 2.0, the user is authenticated via LinkedIn. The user is redirected to the LinkedIn login page and upon successful login, the user is redirected back to the application.

### Run IAM

In order to configure the authentication API, run the following command:

```bash
docker-compose up --build -d
```

The backoffice will be running in your browser at `http://localhost:5002/` where you can configure the authentication API with the authentication providers you wish.

the application will be running in your browser at `http://localhost:8000/`.

