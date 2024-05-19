# google_auth.py
from flask import redirect, session, abort, request
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token
import requests
import os
import pathlib
import ssl
import jwt

ssl._create_default_https_context = ssl._create_stdlib_context

GOOGLE_CLIENT_ID = "1079100803115-eem4517g30nda90sdnfk91jii6caaujl.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:8000/login/google/callback"
)

def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

def google_callback():
    try:
        flow.fetch_token(authorization_response=request.url)

        if "state" not in session or session["state"] != request.args.get("state"):
            abort(500)

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        
        return redirect("/login/google/success")
    except Exception as e:
        raise

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect("/")
        else:
            return function()

    return wrapper

def protected_area():
    # Encode the query parameters into a JWT token
    payload = {'username': session['name'], 'id': session['google_id'][:21]}
    encoded_token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    # Redirect back to Flutter app with the JWT token
    redirect_url = f'http://localhost:8080/welcome?token={encoded_token}'
    return redirect(redirect_url)