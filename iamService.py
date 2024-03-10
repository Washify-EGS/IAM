# app.py
from flask import Flask, render_template, jsonify, redirect, session
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from google_auth import google_login, google_callback, login_is_required, protected_area
from github_auth import github_login, get_github_oauth_token, github_authorized, github_success, github
from linkedin_auth import linkedin_login, linkedin_authorized, linkedin_success

import os, json

app = Flask("IAM Washify App", template_folder="templates", static_folder="static")
api = Api(app)

app.secret_key = "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"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

config_file = 'config.json'

def load_config():
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'google': True, 'github': True, 'linkedin': True}

config = load_config()

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

# ... (other code)

if __name__ == '__main__':
    app.run(debug=True)
