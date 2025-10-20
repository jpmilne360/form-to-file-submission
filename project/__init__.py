from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
app.debug = True
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = b'849ncr4p9ccnafhafa'
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access to the session cookie
app.config['SESSION_COOKIE_SECURE'] = True   # Ensures cookies are only sent over HTTPS

@app.errorhandler(400)
def not_found_error(error):
    return render_template('errors/400.html',  message=error.description), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html', message=error.description), 500

from project import routes

