from flask import redirect, session, url_for, request
from flask_oauthlib.client import OAuth

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


def linkedin_authorized():
    resp = linkedin.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['linkedin_token'] = (resp['access_token'], '')

    # Fetch user information using v2 API
    me = linkedin.get('https://api.linkedin.com/v2/userinfo')
    print(me.data)
    name = me.data.get('name', '')
    session['linkedin_user'] = f"{name}"
    
    return redirect(url_for('linkedin_success_route'))

def linkedin_success():
    print(f"Linkedin user: {session['linkedin_user']}")
    return f"Hello {session['linkedin_user']}! <br/> <a href='/logout'><button>Logout</button></a>"
