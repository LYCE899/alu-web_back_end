from flask import Flask, request, g, render_template
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

# User table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    login_as = request.args.get('login_as')
    if login_as is None:
        return None
    try:
        user_id = int(login_as)
        return users.get(user_id)
    except ValueError:
        return None

@app.before_request
def before_request():
    g.user = get_user()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
