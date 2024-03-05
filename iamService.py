# pip3 install flask_restful
# pip install Flask-OAuthlib
from flask import Flask, redirect, session, abort, url_for, render_template, request
from flask_restful import Api, Resource
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask_oauthlib.client import OAuth
import os
import pathlib
import requests
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


app = Flask("IAM Washify App", template_folder="templates", static_folder="static")
api = Api(app)

app.secret_key = "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"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

GOOGLE_CLIENT_ID = "1079100803115-eem4517g30nda90sdnfk91jii6caaujl.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/login/google/callback"
)

# Initialize Flask-OAuthlib
oauth = OAuth(app)

# GitHub OAuth configuration
github = oauth.remote_app(
    'github',
    consumer_key='f4e1a30e7adeb06aab7c',
    consumer_secret='d91ea7eb81393aee44b6e4b9315cafc79916eeb2',
    request_token_params=None,
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

# Path to your JSON file
json_file_path = 'washifyIAM.json'

@app.route('/')
def welcome():
    return render_template('login.html')

@app.route('/swagger/')
def swagger_ui():
    # Read the Swagger definition from the JSON file
    with open(json_file_path, 'r') as file:
        swagger_definition = file.read()

    # Serve the Swagger UI HTML with embedded JSON
    return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Swagger UI</title>
                    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
                </head>
                <body>
                    <div id="swagger-ui"></div>
                    <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
                    <script>
                        const ui = SwaggerUIBundle({{
                            spec: {swagger_definition},
                            dom_id: '#swagger-ui',
                        }})
                    </script>
                </body>
                </html>
            """
            

# GITHUB LOGIN
@app.route('/login/github', methods=["GET", "POST"])
def githubLogin():
    return github.authorize(callback=url_for('github_authorized', _external=True))

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

# Route for handling GitHub authorization callback
@app.route('/login/github/callback')
def github_authorized():
    error = request.args.get('error', '')
    if error:
        return f'Error: {error}'

    code = request.args.get('code')
    if code:
        data = {
            'code': code,
            'client_id': github.consumer_key,
            'client_secret': github.consumer_secret,
            'redirect_uri': url_for('github_authorized', _external=True),
        }
        auth = requests.auth.HTTPBasicAuth(github.consumer_key, github.consumer_secret)
        headers = {'Accept': 'application/json'}
        resp = requests.post('https://github.com/login/oauth/access_token', data=data, headers=headers, auth=auth)

        if 'access_token' in resp.json():
            session['github_token'] = (resp.json()['access_token'], '')
            user = github.get('user')
            session['github_user'] = user.data['login']

            return redirect(url_for('github_success'))

    return 'Access denied: reason={} error={}'.format(
        request.args['error_reason'],
        request.args['error_description']
    )



@app.route('/login/github/success')
def github_success():
    return f"Hello {session['github_user']}! <br/> <a href='/logout'><button>Logout</button></a>"


# GOOGLE LOGIN    
@app.route("/login/google", methods=["GET", "POST"])
def GoogleLogin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/login/google/callback")
def google_callback():
    try:
        print("Callback route entered")  
        flow.fetch_token(authorization_response=request.url)

        if "state" not in session or session["state"] != request.args.get("state"):
            print("Invalid state parameter")
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
        print("Authentication successful")  
        return redirect("/login/google/success")
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        raise  
    
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            # Authorization required redirect to login
            return redirect("/")
        else:
            return function()

    return wrapper

@app.route("/login/google/success")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

@app.route('/logout')
def logout():
    if "google_id" in session:
        print("Google out the user " + session["name"] + " from google")
        del session["google_id"]
    if "github_user" in session:
        print("Logging out the user " + session["github_user"] + " from github")
        del session["github_user"]
    return redirect("/")

# api.add_resource(GoogleLogin, '/login/google')
# api.add_resource(AppleLogin, '/login/apple')
# api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
