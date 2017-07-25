from flask import Flask, redirect, url_for, session, request
from flask import flash
from flask import render_template
from flask_oauthlib.client import OAuth
from werkzeug import security

app = Flask(__name__)
app.config.from_object('config')
oauth = OAuth(app)
app_url = 'https://api.fib.upc.edu/v2/'


def get_random_state():
    return security.gen_salt(16)


state = get_random_state()
fib = oauth.remote_app(
    'fib',
    request_token_params={'scope': 'read', 'state': state},
    base_url=app_url,
    request_token_url=None,
    access_token_method='POST',
    access_token_url=app_url + 'o/token/',
    authorize_url=app_url + 'o/authorize/',
    app_key='RACO'
)
token_key = 'api_token'


def get_urls():
    return fib.get('', headers={'Accept': 'application/json'}).data


def render_raco_template(template, **kwargs):
    me = None
    if get_raco_token():
        urls = get_urls()
        me = fib.get(urls['privat']['jo'], headers={'Accept': 'application/json'})
        me = me.data

    kwargs.pop('me', None)
    return render_template(template, me=me, **kwargs)


@app.route('/')
def index():
    avisos = []
    if get_raco_token():
        urls = get_urls()
        avisos_resp = fib.get(urls['privat']['avisos'], headers={'Accept': 'application/json'})
        if avisos_resp.status != 200:
            flash('API Response (' + str(avisos_resp.status) + '): ' + avisos_resp.data['detail'], category='danger')
        else:
            avisos = avisos_resp.data['results']
    return render_raco_template('home.html', avisos=avisos, )


@app.route('/photo')
def photo():
    if get_raco_token():
        urls = get_urls()
        photo_url = fib.get(urls['privat']['foto'], headers={'Accept': 'application/json'})
        photo_url = photo_url.data['foto']
        photo = fib.get(photo_url)
        photo = photo.data
    return app.response_class(photo, mimetype='image/jpg')


@app.route('/login')
def login():
    return fib.authorize(callback=url_for('authorized', _external=True), approval_prompt='auto')


@app.route('/logout')
def logout():
    session.pop(token_key, None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = fib.authorized_response()
    received_state = request.args['state']
    if resp is None or resp.get('access_token') is None or received_state is None or received_state != state:
        flash('Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        ))
    else:
        flash('Welcome back!', category='success')
        session[token_key] = (resp['access_token'], '')
    return redirect(url_for('index'))


@fib.tokengetter
def get_raco_token():
    return session.get(token_key)


if __name__ == '__main__':
    app.run(port=5001)
