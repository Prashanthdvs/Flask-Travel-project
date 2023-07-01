from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField,SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
