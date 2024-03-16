# github_auth.py
from flask import redirect, session, url_for
from flask_oauthlib.client import OAuth

oauth = OAuth()

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

def github_login():
    return github.authorize(callback=url_for('github_authorized_route', _external=True))

def get_github_oauth_token():
    return session.get('github_token')

def github_authorized():
    response = github.authorized_response()

    if response is None or response.get('access_token') is None:
        return redirect(url_for('welcome'))

    session['github_token'] = (response['access_token'], '')

    user_info = github.get('user')
    session['github_user'] = user_info.data['login']

    return redirect(url_for('github_success_route'))

def github_success():
    return f"Hello {session['github_user']}! <br/> <a href='/logout'><button>Logout</button></a>"
