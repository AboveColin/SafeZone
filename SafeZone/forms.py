from flask_wtf import FlaskForm
from wtforms.validators import data_required, Email, EqualTo
from wtforms import ValidationError, StringField, PasswordField, SubmitField, SelectField

class Loginform(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[data_required()])
    password = PasswordField("Wachtwoord", validators=[data_required()])
    submit = SubmitField("Inloggen")

class Registratie(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[data_required()])
    password = PasswordField("Wachtwoord", validators=[data_required(), EqualTo("pass_confirm", message="Wachtwoorden komen niet overeen")])
    pass_confirm = PasswordField("Bevestig wachtwoord", validators=[data_required()])
    submit = SubmitField("Registreer")

