"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    # return a

    flash(session)

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of all users."""

    users = User.query.all()
    return render_template("users_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_form():
    """Show users registration form."""


    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Register new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        #work on notifying user
        flash("User e-mail already exists. Please choose a new e-mail.")
    else:

        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()     

        # sql = """INSERT INTO users (email, password)
        #          VALUES (:email, :password)
        #       """

        # db.session.execute(sql,
        #                     {'email': email,
        #                     'password': password})


    return redirect("/")


@app.route("/login", methods=["GET"])
def login_form():
    """Show user login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Login user."""

   
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email, password=password).first() 

    if user:
        session['current user'] = email
        flash("You are logged in.")
        return redirect("/users/<>")

    else:
        flash("Invalid login!")
        return render_template("login.html")
        

@app.route("/logout")
def logout_process():
    """Logout user."""

    if 'current user' in session:
        del session['current user']
    flash("You are logged out.")

    return redirect("/")


# <users.user_id>

@app.route("/users/<username>")
def user_details(username):
    """Show user info."""

    user = User.query.get(username)
    
    return render_template("user_info.html", user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
