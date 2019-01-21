#!/opt/python27/bin python
from app.main import app
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run("0.0.0.0")
