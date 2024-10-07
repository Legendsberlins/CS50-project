import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///register.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Link user to account
    user_id = session["user_id"]
    name = db.execute("SELECT USERNAME FROM registrants WHERE ID = ?", user_id)
    real_name = name[0]["USERNAME"]

    # Fetch the user's record from the database
    records = db.execute("SELECT WIN, DRAW, LOSE, [WIN %], [DRAW %], [LOSE %] FROM records WHERE USER_ID = ?", user_id)

    # If no records exist for the user, initialize with zeroes
    if len(records) == 0:
        win_count = 0
        draw_count = 0
        lose_count = 0
        win_rate_rounded = 0.0
        draw_rate_rounded = 0.0
        lose_rate_rounded = 0.0
    else:
        win_count = records[0]["WIN"]
        draw_count = records[0]["DRAW"]
        lose_count = records[0]["LOSE"]
        win_rate_rounded = records[0]["WIN %"]
        draw_rate_rounded = records[0]["DRAW %"]
        lose_rate_rounded = records[0]["LOSE %"]

    return render_template("index.html",
                           win_counthtml=win_count,
                           draw_counthtml=draw_count,
                           lose_counthtml=lose_count,
                           win_ratehtml=win_rate_rounded,
                           draw_ratehtml=draw_rate_rounded,
                           lose_ratehtml=lose_rate_rounded,
                           namehtml=real_name)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # clear cookie session
    session.clear()

    # make sure user fills in all details
    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')
        password_two = request.form.get('confirmation')
        contains_special_char = any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?"
                                    for char in password)
        contains_number = any(char.isdigit() for char in password)

        if not name:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not password_two:
            return apology("Confirm password", 400)
        elif password != password_two:
            return apology("Passwords don't correspond", 400)
        elif len(password) < 8:
            return apology("Invalid password", 400)
        elif not contains_special_char:
            return apology("Invalid password", 400)
        elif not contains_number:
            return apology("Invalid password", 400)

        # make sure username doesn't exist twice
        rows = db.execute("SELECT * FROM registrants WHERE username = ?", name)
        if len(rows) != 0:
            return apology("Username already exists")

        # Use generate_password_hash to generate a hash of the password instead of plain text
        password_generator = generate_password_hash(password)
        date = datetime.datetime.now()

        # Use SQL to include the user into the users table
        db.execute("INSERT INTO registrants (USERNAME, HASH, DATE) VALUES (?,?,?)",
                   name, password_generator, date)

        rows = db.execute("SELECT * FROM registrants WHERE username = ?", name)

        # log user in using session["user_id"] = id of the user who has been added
        session["user_id"] = rows[0]["ID"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not name:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM registrants WHERE USERNAME = ?", name)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["HASH"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/result", methods=["GET", "POST"])
@login_required
def result():
    """Update user's game result"""
    user_id = session["user_id"]

    if request.method == "POST":
        result = request.form.get("result")

        # Fetch the current user's record
        records = db.execute("SELECT * FROM records WHERE USER_ID = ?", user_id)

        if len(records) == 0:
            # If no record exists, initialize
            win_count = 0
            draw_count = 0
            lose_count = 0
        else:
            win_count = records[0]["WIN"]
            draw_count = records[0]["DRAW"]
            lose_count = records[0]["LOSE"]

        # Update counts based on the result
        if result == 'win':
            win_count += 1
        elif result == 'draw':
            draw_count += 1
        elif result == 'lose':
            lose_count += 1

        total_games = win_count + draw_count + lose_count

        # Calculate percentages
        win_rate = (win_count / total_games) * 100 if total_games > 0 else 0
        draw_rate = (draw_count / total_games) * 100 if total_games > 0 else 0
        lose_rate = (lose_count / total_games) * 100 if total_games > 0 else 0

        win_rate_rounded = round(win_rate, 2)
        draw_rate_rounded = round(draw_rate, 2)
        lose_rate_rounded = round(lose_rate, 2)

        # Update or insert the user's record in the database
        if len(records) == 0:
            db.execute("INSERT INTO records (USER_ID, WIN, DRAW, LOSE, [WIN %], [DRAW %], [LOSE %]) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       user_id, win_count, draw_count, lose_count, win_rate_rounded, draw_rate_rounded, lose_rate_rounded)
        else:
            db.execute("UPDATE records SET WIN = ?, DRAW = ?, LOSE = ?, [WIN %] = ?, [DRAW %] = ?, [LOSE %] = ? WHERE USER_ID = ?",
                       win_count, draw_count, lose_count, win_rate_rounded, draw_rate_rounded, lose_rate_rounded, user_id)

        return redirect("/")

    return render_template("index.html")

@app.route("/clear", methods=["POST"])
@login_required
def clear():
    """Clear the user's game statistics"""
    user_id = session["user_id"]

    # Reset the game statistics to zero for the user
    db.execute("UPDATE records SET WIN = 0, DRAW = 0, LOSE = 0, [WIN %] = 0.0, [DRAW %] = 0.0, [LOSE %] = 0.0 WHERE USER_ID = ?", user_id)

    # Redirect back to the index page after clearing
    return redirect("/")
