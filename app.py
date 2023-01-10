from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from help import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///muziqer.db")


@app.route("/")
def index():
    return render_template("index.html")

# Registering new users


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username does not exist in db
        if len(rows) > 0:
            flash('Username already taken! Please try again.')
            return render_template("index.html")

        # Query database for email
        rows_e = db.execute("SELECT * FROM users WHERE email = ?",
                            request.form.get("email"))

        # Ensure email does not exist in db
        if len(rows_e) > 0:
            flash('Email already registered! Please try again.')
            return render_template("index.html")

        # Hash the password before saving in db
        hash_p = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        email = request.form.get("email")
        # Save user in db
        db.execute(
            "INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, hash_p)

        # Get the new user's id
        new_user_id = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username"))

        # Login the newly registered user
        session["user_id"] = new_user_id[0]["id"]

        # Redirect user to home page
        flash('Account successfully created')
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")


# Loging in existing users
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("l_password")):
            flash('Incorrect password or user does not exist!')
            return render_template("index.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")


# Loging out existing users
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Sending reset password
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Send email reset"""
    if request.method == "POST":
        flash('Email reset sent if email was registered.')
        return render_template("index.html")


# Contact page
@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    """User can contact the App owner"""

    # Get current user id
    user_id = session["user_id"]

    # Get user's username & email
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    user_name = user[0]["username"]
    user_email = user[0]["email"]

    if request.method == "POST":
        flash('Your message was successfully sent!')
        return render_template("home.html")

    return render_template("contact.html", user_name=user_name, user_email=user_email)


# Add new records
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add new records to music storage"""

    if request.method == "POST":
        # Get user data
        artist = request.form.get("artist")
        album = request.form.get("album")
        year = request.form.get("year")
        genre = request.form.get("genre")
        medium = request.form.get("medium")
        numbermedium = request.form.get("numbermedium")
        shelf = "Shelf" + " " + request.form.get("shelf")
        row = "Row" + " " + request.form.get("row")

        user_id = session["user_id"]

        # Get latest number of record in database
        number = db.execute(
            "SELECT number FROM records WHERE id = ? ORDER BY number DESC LIMIT 1", user_id)
        if not number:
            new_number = 1
        else:
            new_number = number[0]["number"] + 1

        # Add buy transaction to the transaction table
        db.execute("INSERT INTO records (id, number, artist, album, year, genre, medium, numbermedium, shelf, row, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   user_id, new_number, artist, album, year, genre, medium, numbermedium, shelf, row, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Redirect user to home page
        flash('New record successfully added!')
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")


# Search engine for types of genres
@app.route("/searchgenre")
def searchgenre():
    # Get all genres
    genres = db.execute(
        "SELECT DISTINCT(genre) FROM genres WHERE genre LIKE ?", "%" + request.args.get("q") + "%")
    return genres


# Home page
@app.route("/home")
@login_required
def home():
    """Show user's music storage"""

    # Get current user id
    user_id = session["user_id"]

    # Get username
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    user_name = user[0]["username"]

    # Get all music records
    music_records = db.execute("SELECT * FROM records WHERE id = ?", user_id)

    # Get last update date
    update = db.execute(
        "SELECT number, date FROM records WHERE id = ? ORDER BY number DESC LIMIT 1", user_id)
    if not update:
        last_update = "No recent updates"
    else:
        last_update = update[0]["date"]

    # Get number of albums
    number = db.execute("SELECT number FROM records WHERE id = ?", user_id)
    number_records = len(number)

    # Get number of record mediums
    mediums = db.execute(
        "SELECT numbermedium FROM records WHERE id = ?", user_id)
    number_mediums = 0
    for i in range(len(mediums)):
        number_mediums += mediums[i]["numbermedium"]

    return render_template("home.html", user_name=user_name, music_records=music_records, last_update=last_update, number_records=number_records, number_mediums=number_mediums)


# Remove record
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Remove records from music storage"""

    # Get current user id
    user_id = session["user_id"]

    if request.method == "POST":
        # Get user data
        number = request.form.get("delete", "")
        # Remove record from db

        db.execute("DELETE FROM records WHERE id = ? AND number = ?",
                   user_id, number)

        # Redirect user to home page
        flash('Record removed successfully!')
        return redirect("/home")
