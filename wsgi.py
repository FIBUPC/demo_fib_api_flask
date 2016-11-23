from app import app as application

# WSGI python file for easier gunicorn usage
# See: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04

if __name__ == "__main__":
    application.run()
