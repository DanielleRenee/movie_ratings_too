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
        return redirect("/users/{}".format(user.user_id))


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


@app.route("/users")
def user_list():
    """Show list of all users."""

    users = User.query.all()
    return render_template("users_list.html", users=users)


@app.route("/users/<username>")
def user_info(username):
    """Show user info."""

    user = User.query.get(username)
    
    return render_template("user_info.html", user=user)


@app.route("/movies")
def movie_list():
    """Show list of all movies."""

    movies = Movie.query.order_by("title").all()

    return render_template("movies_list.html", movies=movies)


@app.route("/movies/<movie_id>")
def movie_info(movie_id):
    """Show movie info."""

    movie = Movie.query.get(movie_id)

    return render_template("movie_info.html", movie=movie)



@app.route("/<movie_id>/add_rating", methods=["GET"])
def rating_form(movie_id):
    """Show movie rating form."""


    return render_template("add_rating.html")


@app.route("/<movie_id>/add_rating", methods=["POST"])
def rating_process(movie_id):
    """Allows user to add a new rating."""

    rating = request.form.get("rating")

    # WIP: Need to finish


    return render_template("/{}/add_rating".format(movie_id))

     

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
