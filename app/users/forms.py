from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp


class RegistrationForm(FlaskForm):

    full_name = StringField('Full name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[
        DataRequired(), 
        Regexp(r'^[\d\s()+]+$', message="Invalid phone number.")]) # TODO: Make phone validation
    address = StringField('Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")