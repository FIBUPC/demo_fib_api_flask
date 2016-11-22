from flask import Flask, redirect, url_for, session, request, jsonify
from flask import render_template
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_object('config')
oauth = OAuth(app)

raco = oauth.remote_app(
    'raco',
    request_token_params={'scope': 'read'},
    base_url='https://raco.fib.upc.edu/api/v2/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://raco.fib.upc.edu/api/v2/o/token/',
    authorize_url='https://raco.fib.upc.edu/api/v2/o/authorize/',
    app_key='RACO'
)
token_key = 'raco_token'


@app.route('/')
def index():
    me = None
    avisos = None
    if token_key in session:
        me = raco.get('me.json').data
        avisos = raco.get('me/avisos.json').data['results']

    return render_template('home.html', me=me, avisos=avisos)


@app.route('/login')
def login():
    return raco.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop(token_key, None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = raco.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session[token_key] = (resp['access_token'], '')
    me = raco.get('me.json')
    return jsonify(me.data)


@raco.tokengetter
def get_raco_token():
    return session.get(token_key)


if __name__ == '__main__':
    app.run(port=5001)
