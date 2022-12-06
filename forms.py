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

class AdminForm(FlaskForm):
    id = StringField("User ID: ")
    username = StringField("Username: ")
    newusername = StringField("New username: ")
    newresult = StringField("New result: ")
    newpassword = StringField("New password: ")
    add = BooleanField("Add", default=False)
    remove = BooleanField("Remove", default=False)
    changename = BooleanField("Change username", default=False)
    changepass = BooleanField("Change password", default=False)
    changeresult = BooleanField("Change result", default=False)
    setadmin = BooleanField("Set admin", default=False)
    removeadmin = BooleanField("Remove admin", default=False)
    submit = SubmitField("Submit")
