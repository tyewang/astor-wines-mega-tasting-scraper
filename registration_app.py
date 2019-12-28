import os
import dill

from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import redis


redis_instance = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "/register"

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

blueprint = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=["https://www.googleapis.com/auth/calendar.events"],
    offline=True,
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def serve_google_oauth():
    if not google.authorized:
        return redirect(url_for("google.login"))

    redis_instance.sadd("google.credentials", dill.dumps(google))
    return "You're in! Astor Wines mega tastings will now start appearing on your Google calendar."
