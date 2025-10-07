from flask import Blueprint, render_template

mainbp = Blueprint("main", __name__)

@mainbp.route("/")
def index():
    # index.html should extend base.html and show featured/upcoming events etc.
    return render_template("index.html", title="SportsZone | Home")
