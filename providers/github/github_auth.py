# github_auth.py
from flask import redirect, request, session, url_for
from flask_oauthlib.client import OAuth
import jwt

oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key='084e782051652dc61b58',
    consumer_secret='9b482b565e25f5d48368736f85e50ac1eb09a482',
    request_token_params=None,
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

@github.authorized_handler
def github_authorized(resp):
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    session['github_user'] = me.data['login']
    session['github_email'] = me.data['email']
    session['github_userid'] = str(me.data['id'])
    
    return redirect(url_for('github_success_route'))

def github_login():
    return github.authorize(callback=url_for('github_authorized_route', _external=True))

def get_github_oauth_token():
    return session.get('github_token')

def github_success():    
    # Encode the query parameters into a JWT token
    payload = {'username': session['github_user'], 'id': session['github_userid']}
    encoded_token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    # Redirect back to Flutter app with the JWT token
    redirect_url = f'http://localhost:8080/welcome?token={encoded_token}'
    return redirect(redirect_url)
    