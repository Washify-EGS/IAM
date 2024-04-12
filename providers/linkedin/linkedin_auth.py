from flask import redirect, session, url_for, request
from flask_oauthlib.client import OAuth
from db import insert_user

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
    session['linkedin_user'] = f"{name}"
    session['linkedin_email'] = me.data.get('email', '')
    
    return redirect(url_for('linkedin_success_route'))

def linkedin_success():
    print(f"Linkedin user: {session['linkedin_user']}")
    # print linkedin user token or id
    linkedin_token = session['linkedin_token'][0][:41]  
    print(f"Linkedin token: {linkedin_token}")
    print(f"Linkedin email: {session['linkedin_email']}")
    
    # insert Linkedin user into the database
    # insert_user(session['linkedin_user'], linkedin_id=linkedin_token, email=session['linkedin_email'])
    return f"Hello {session['linkedin_user']}! <br/> <a href='/logout'><button>Logout</button></a>"

# get user information
def get_user_info():
    return {
        "name": session["linkedin_user"],
        "email": session["linkedin_email"],
        "linkedin_id": session["linkedin_token"][0]
    }


