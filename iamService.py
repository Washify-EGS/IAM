# app.py
from flask import Flask, render_template, jsonify, redirect, session
from flask_swagger_ui import get_swaggerui_blueprint
from providers.linkedin.linkedin_auth import *
from providers.github.github_auth import *
from providers.google.google_auth import *
from flask_restful import Api
from db import get_last_logged_in_user

import os, json
import jwt

app = Flask("IAM Washify App", template_folder="static/templates", static_folder="static")

SWAGGER_URL = '/api/docs'  
API_URL = '/static/washifyIAM.json'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "IAM Washify App"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

api = Api(app)

app.secret_key = "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"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

config_file = 'backoffice/config.json'

## configuration given from backoffice
def load_config():
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'google': True, 'github': True, 'linkedin': True}

config = load_config()


# HOME
@app.route('/')
def welcome():
    return render_template('login.html', enabled_providers=config)


# GITHUB LOGIN
@app.route('/login/github', methods=["GET", "POST"])
def github_login_route():
    return github_login()

@github.tokengetter
def get_github_token():
    return get_github_oauth_token()

@app.route('/login/github/callback')
def github_authorized_route():
    return github_authorized()

@app.route('/login/github/success')
def github_success_route():
    return github_success()

# GOOGLE LOGIN    
@app.route("/login/google", methods=["GET", "POST"])
def google_login_route():
    return google_login()

@app.route("/login/google/callback")
def google_callback_route():
    return google_callback()

@app.route("/login/google/success")
@login_is_required
def google_protected_area():
    return protected_area()

# LINKEDIN LOGIN
@app.route("/login/linkedin", methods=["GET", "POST"])
def linkedin_login_route():
    return linkedin_login()

@app.route("/login/linkedin/callback")
def linkedin_authorized_route():
    print("Linkedin authorized route")
    return linkedin_authorized()

@app.route("/login/linkedin/success")
def linkedin_success_route():
    return linkedin_success()

# get user info
@app.route('/userinfo')
def get_user_info():
    user = get_last_logged_in_user()  # Call the function to fetch users from the database
    token = generate_jwt_token(user)
    return jsonify({'token': token})  # Return the users as JSON response


@app.route('/logout')
def logout():
    if "google_id" in session:
        print("Google out the user " + session["name"] + " from google")
        del session["google_id"]
    if "github_user" in session:
        print("Logging out the user " + session["github_user"] + " from github")
        del session["github_user"]
    if "linkedin_user" in session:
        print("Logging out the user from LinkedIn")
        del session["linkedin_user"]
    return redirect("/")

def generate_jwt_token(user_info):
    if user_info:
        payload = {
            'id': None,
            'name': user_info['username'], 
            'email': user_info['email']
        }
        
        for id_type in ['google_id', 'github_id', 'linkedin_id']:
            if user_info[id_type] is not None:
                payload['id'] = user_info[id_type]
                break

        jwt_token = jwt.encode(payload, app.secret_key, algorithm='HS256')
        return jwt_token
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
