from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=5, max=100)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=5, max=100)])
    confirm_password = PasswordField("Confirm password: ", validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField("Sign Up")