# app.py
from flask import Flask, render_template, redirect, session
from flask_swagger_ui import get_swaggerui_blueprint
from providers.linkedin.linkedin_auth import *
from providers.github.github_auth import *
from providers.google.google_auth import *
from flask_restful import Api

import os, json

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


# HOME
@app.route('/')
def welcome():
    return render_template('login.html', enabled_providers=load_config())


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')


