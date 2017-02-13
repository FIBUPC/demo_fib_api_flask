import os

# Config file for Heroky environment. This binds variables to environment variables in order to make Heroku deployment easier.

# Set this to False if going to production
DEBUG = False

# Set this to random value when going to production
SECRET_KEY = os.environ['secret_key']

# App credentials lazy load configuration
# Read: https://flask-oauthlib.readthedocs.io/en/latest/client.html#lazy-configuration
# Get them: https://raco.fib.upc.edu/api/v2/o/
RACO = {
    'consumer_key': os.environ['consumer_key'],
    'consumer_secret': os.environ['consumer_secret']
}
