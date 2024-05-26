from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import Clients, Employees, Services, OrdersStatuses, ServiceObjects, Posts

class ClientForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    telephone = StringField('Telephone', validators=[DataRequired(), Length(min=10, max=15)])
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    submit = SubmitField('Submit')

    def validate_login(self, login):
        client = Clients.query.filter_by(login=login.data).first()
        if client:
            raise ValidationError('This login is already taken. Please choose a different one.')

class EmployeeForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    telephone = StringField('Telephone', validators=[DataRequired(), Length(min=10, max=15)])
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    post_id = SelectField('Post', coerce=int, validators=[DataRequired()])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Submit')

    def validate_login(self, login):
        employee = Employees.query.filter_by(login=login.data).first()
        if employee:
            raise ValidationError('This login is already taken. Please choose a different one.')

class ServiceForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')

class StatusForm(FlaskForm):
    status_name = StringField('Status Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')

class ServiceObjectForm(FlaskForm):
    object_name = StringField('Object Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post_name = StringField('Post Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')
