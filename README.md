# RACO API 2.0 - Python example

## Install

Requirements `python 2.7` or `python 3.5`.
```
pip install -r requirements.txt
```

## Configuration

- Copy `config.py.sample` to `config.py`: `cp config.py.sample config.py`
- Create Raco API Application [here](https://api.fib.upc.edu/v2/o/applications/register/), with redirect url `http://localhost:5001/login/authorized` (or whatever url your server is running in)
- Replace _client secret_ and _client id_ in `config.py`

### Production

- Set DEBUG to False in config.py
- Create a random secret key. 
    - Optional: You can create a random key by using the following python code
    
``` python
import os
os.urandom(24)
```

## Deployment
You can easily start the server with `python app.py`.

In production, you should use something like [Gunicorn](http://gunicorn.org/) to serve this. You can run the app with `gunicorn -b :<PORT> -w <number of workers> wsgi`.
