from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

wca = oauth.remote_app ('wca',
                        base_url='https://www.worldcubeassociation.org/api/v0/',
                        request_token_url= None,
                        access_token_url='https://www.worldcubeassociation.org/oauth/token',
                        authorize_url='https://www.worldcubeassociation.org/oauth/authorize',
                        consumer_key='ac5da98d8c8d0ea070939d65cbb0d29a49606d20c8f035719158bd9eee6c6cd6',
                        consumer_secret='f531e05fdc0cf5acf8205c4788e8dc668ef04f0aeca47704897b5f09842759e7',
                        request_token_method='POST',
                        request_token_params={'scope': 'public email dob'}
                        )


@app.route('/')
def index():
    if 'wca_token' in session:
        me = wca.get('user')
        return "You are logged in!!!"
    return """
    <h1>Welcome to this OAuth Test Page</h1>
    <p>Please add '/login' to the end of the URL to login using your WCA Account</p>
    """


@app.route('/login')
def login():
    return wca.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('wca_token', None)
    return "You have been logged out!"


@app.route('/login/authorized')
def authorized():
    resp = wca.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['wca_token'] = (resp['access_token'], '')
    me = wca.get('me')
    return jsonify(me.data)


@wca.tokengetter
def get_wca_oauth_token():
    return session.get('wca_token')


if __name__ == '__main__':
    app.run()