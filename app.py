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

win_count = 0
draw_count = 0
lose_count = 0
total_games = win_count + draw_count + lose_count

win_rate = (win_count / total_games) * 100 if total_games > 0 else 0.0
draw_rate = (draw_count / total_games) * 100 if total_games > 0 else 0.0
lose_rate = (lose_count / total_games) * 100 if total_games > 0 else 0.0

win_rate_rounded = round(win_rate, 2)
draw_rate_rounded = round(draw_rate, 2)
lose_rate_rounded = round(lose_rate, 2)



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

    #records = db.execute("SELECT WIN, DRAW, LOSE, [WIN %], [DRAW %], [LOSE %] FROM records WHERE user_id = ?", user_id)
    global win_count, draw_count, lose_count, win_rate_rounded, draw_rate_rounded, lose_rate_rounded

    return render_template("index.html", win_counthtml = win_count, draw_counthtml = draw_count, lose_counthtml = lose_count, win_ratehtml = win_rate_rounded, draw_ratehtml = draw_rate_rounded, lose_ratehtml = lose_rate_rounded, namehtml = real_name) #recordshtml=records


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
        contains_special_char = any(char for char in password if char in "!@#$%^&*()-_=+[{]};:'\",<.>/?")
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
        db.execute("INSERT INTO registrants (USERNAME, HASH, DATE) VALUES (?,?,?)", name, password_generator, date)
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

    # User reached route via POST (as by submitting a form via POST)
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

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/result", methods = ["GET","POST"])
@login_required
def result():
    user_id = session["user_id"]
    name = db.execute("SELECT USERNAME FROM registrants WHERE ID = ?", user_id)
    name[0]["USERNAME"]
    if request.method == 'POST':
        global win_count, draw_count, lose_count, win_rate, draw_rate, lose_rate, win_rate_rounded, draw_rate_rounded, lose_rate_rounded

        db.execute("INSERT INTO records (USER_ID, WIN, DRAW, LOSE, [WIN %], [DRAW %], [LOSE %]) VALUES (?,?,?,?,?,?,?)", user_id, win_count, draw_count, lose_count, win_rate, draw_rate, lose_rate)

        result = request.form.get("result")

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

        db.execute("UPDATE records SET WIN = ?, DRAW = ?, LOSE = ?, [WIN %] = ?, [DRAW %] = ?, [LOSE %] = ? WHERE USER_ID = ?", win_count, draw_count, lose_count, win_rate_rounded, draw_rate_rounded, lose_rate_rounded, user_id)

        return redirect("/")

    return render_template('index.html')

'''@app.route("/clear", methods = ["POST"])
@login_required
def clear():
    user_id = session["user_id"]
    name = db.execute("SELECT USERNAME FROM registrants WHERE ID = ?", user_id)
    real_name = name[0]["USERNAME"]
    clear = request.form.get("clear")

    if clear == 'clear':
        db.execute("UPDATE records SET WIN = ?, DRAW = ?, LOSE = ?, [WIN %] = ?, [DRAW %] = ?, [LOSE %] = ? WHERE USER_ID = ?", 0,0,0,0.0,0.0,0.0, user_id)
        return redirect("/")

@app.route("/result", methods = ["POST"])
@login_required
def result():
    user_id = session["user_id"]
    name = db.execute("SELECT USERNAME FROM registrants WHERE ID = ?", user_id)
    real_name = name[0]["USERNAME"]

    global win_count, draw_count, lose_count

    result = request.form.get("result")

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

    db.execute("INSERT INTO records ("USER_ID, WIN, DRAW, LOSE, [WIN %], [DRAW %], [LOSE %]) VALUES (?,?,?,?,?,?,?)", user_id, win_count, draw_count, lose_count, win_rate_rounded, draw_rate_rounded, lose_rate_rounded)

    return render_template('index.html', resulthtml = result, namehtml = real_name, win_counthtml=win_count, draw_counthtml=draw_count, lose_counthtml=lose_count, win_ratehtml=win_rate_rounded, draw_ratehtml=draw_rate_rounded, lose_ratehtml=lose_rate_rounded) '''

'''@app.route("/result", methods = ["GET","POST"])
@login_required
def result():
    user_id = session["user_id"]
    name = db.execute("SELECT USERNAME FROM registrants WHERE ID = ?", user_id)
    real_name = name[0]["USERNAME"]

    if request.method == 'POST':
        global win_count, draw_count, lose_count, win_rate, draw_rate, lose_rate

        db.execute("INSERT INTO records (USER_ID, WIN, DRAW, LOSE, [WIN %], [DRAW %], [LOSE %]) VALUES (?,?,?,?,?,?,?)", user_id, win_count, draw_count, lose_count, win_rate, draw_rate, lose_rate)
        database = db.execute("SELECT * FROM records")

        result = request.form.get("result")

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

        db.execute("UPDATE records SET WIN = ?, DRAW = ?, LOSE = ?, [WIN %] = ?, [DRAW %] = ?, [LOSE %] = ? WHERE USER_ID = ?", win_count, draw_count, lose_count, win_rate_rounded, draw_rate_rounded, lose_rate_rounded, user_id)

        return render_template("index.html", databasehtml = database, namehtml = real_name, win_counthtml=win_count, draw_counthtml=draw_count, lose_counthtml=lose_count, win_ratehtml=win_rate_rounded, draw_ratehtml=draw_rate_rounded, lose_ratehtml=lose_rate_rounded)

    return redirect('/')'''



