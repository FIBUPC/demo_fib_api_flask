from flask import Flask, redirect, url_for, session, request, flash, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config.from_object('config')

oauth = OAuth(app)
app_url = 'https://api.fib.upc.edu/v2/'
token_key = 'api_token'

# Registro moderno con Authlib
oauth.register(
    name='fib',
    client_id=app.config['RACO']['consumer_key'],
    client_secret=app.config['RACO']['consumer_secret'],
    access_token_url=app_url + 'o/token/',
    authorize_url=app_url + 'o/authorize/',
    api_base_url=app_url,
    client_kwargs={'scope': 'read'},
    fetch_token=lambda: session.get(token_key)
)


def get_urls():
    resp = oauth.fib.get('', headers={'Accept': 'application/json'})
    data = resp.json()
    if 'privat' not in data:
        print(f"DEBUG: API Root Response: {data}")
    return data


def render_raco_template(template, **kwargs):
    me = None
    if session.get(token_key):
        urls = get_urls()
        me = oauth.fib.get(urls['privat']['jo'], headers={'Accept': 'application/json'}).json()

    kwargs.pop('me', None)
    return render_template(template, me=me, **kwargs)


@app.route('/')
def index():
    avisos = []
    if session.get(token_key):
        urls = get_urls()
        if 'privat' in urls:
            avisos_resp = oauth.fib.get(urls['privat']['avisos'], headers={'Accept': 'application/json'})
            if avisos_resp.status_code == 200:
                avisos = avisos_resp.json().get('results', [])
            else:
                flash(f"Error cargando avisos: {avisos_resp.status_code}", category='danger')
        else:
            flash("Sesión inválida o expirada. Por favor, inicie sesión de nuevo.", category='warning')
            session.pop(token_key, None)
    return render_raco_template('home.html', avisos=avisos)


@app.route('/photo')
def photo():
    if session.get(token_key):
        urls = get_urls()
        photo_info = oauth.fib.get(urls['privat']['foto'], headers={'Accept': 'application/json'}).json()
        photo_data = oauth.fib.get(photo_info['foto']).content  # .content para binarios
        return app.response_class(photo_data, mimetype='image/jpg')
    return "Unauthorized", 401


@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return oauth.fib.authorize_redirect(redirect_uri)


@app.route('/login/authorized')
def authorized():
    token = oauth.fib.authorize_access_token()
    if token:
        session[token_key] = token
        flash('Welcome back!', category='success')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop(token_key, None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5001)