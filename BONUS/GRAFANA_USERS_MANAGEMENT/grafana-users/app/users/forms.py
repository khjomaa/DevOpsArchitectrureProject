from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    name = StringField('Name (Optional)', validators=[Optional(), Length(min=4)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Add User')
