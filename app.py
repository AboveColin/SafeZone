#!/usr/bin/python
from flask import Flask, render_template, redirect, request, jsonify, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from SafeZone import app
from SafeZone.models import *
from SafeZone.forms import *

context = ('C:\\Shares\\School\\Vakken\\p3\\\Project\\cert.crt', 'C:\\Shares\\School\\Vakken\\p3\\\Project\\key.key')

@app.route('/')
def index():
    return render_template('home.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("U bent succesvol uitgelogd")
    return redirect(url_for("index"))


# Shows the user a login form
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = Loginform()
    if form.validate_on_submit():
         # Checks if the username is registered in the database
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            # If the username or password isn't recognised, the user gets flashed a message and will be redirected to the login page.
            flash("Inloggen mislukt: gebruikersnaam/wachtwoord niet bekend.")
            return redirect(url_for("login"))
        
        login_user(user)
        flash("U bent succesvol ingelogd")
        return redirect(url_for("index"))

    return render_template("login.html", form=form)


# Shows the registration form
@app.route("/register", methods=["GET", "POST"])
def register():

    # The registration form
    form = Registratie()
    if form.validate_on_submit():

        # Checks if the E-mail or Username is already in use
        # If yes, the user gets flashed a message and will be send back to the registration page
        user_username = User.query.filter_by(username=form.username.data).first()
        if user_username:
            flash("Gebruikersnaam al in gebruik, probeer in te loggen.")
            return redirect(url_for("register"))

        user = User(username = form.username.data, password = form.password.data)
        user_db.session.add(user)
        user_db.session.commit()

        flash("Bedankt voor het registreren")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context = context)

    
