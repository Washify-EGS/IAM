from flask import redirect, session, url_for, request
from flask_oauthlib.client import OAuth
from db import insert_user
import jwt

# linkedin auth
oauth = OAuth()

linkedin = oauth.remote_app(
    "linkedin",
    consumer_key="77cjkwkseuc5j6",
    consumer_secret="kqmuy1W1HuxsQmBX",
    request_token_params={'scope': 'openid profile email'},
    base_url="https://api.linkedin.com/v2/userinfo",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
    authorize_url="https://www.linkedin.com/oauth/v2/authorization",
)

def linkedin_login():
    callback_url = url_for("linkedin_authorized_route", _external=True)
    print(f"Callback URL: {callback_url}")
    return linkedin.authorize(callback=callback_url)

@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')

@linkedin.authorized_handler
def linkedin_authorized(resp):
    if isinstance(resp, Exception):
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    
    session['linkedin_token'] = (resp['access_token'], '')

    # Fetch user information using v2 API
    me = linkedin.get('https://api.linkedin.com/v2/userinfo')
    print(me.data)
    name = me.data.get('name', '')
    linkedin_id = me.data.get('id', '')
    session['linkedin_user'] = f"{name}"
    session['linkedin_id'] = f"{linkedin_id}"
    session['linkedin_email'] = me.data.get('email', '')
    
    return redirect(url_for('linkedin_success_route'))

def linkedin_success():
    # Encode the query parameters into a JWT token
    payload = {'username': session['linkedin_user'], 'id': session['linkedin_id']}
    encoded_token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    # Redirect back to Flutter app with the JWT token
    redirect_url = f'http://localhost:8080/welcome?token={encoded_token}'
    return redirect(redirect_url)


