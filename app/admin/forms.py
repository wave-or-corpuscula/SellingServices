from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import Clients, Employees, Services, OrdersStatuses, ServiceObjects, Posts

class ClientForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=150)])
    address = StringField('Адрес', validators=[DataRequired(), Length(min=2, max=150)])
    telephone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=15)])
    login = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Пароль', validators=[Length(min=6)])
    submit = SubmitField('Добавить клиента')

    def validate_login(self, login: str) -> None:
        client = Clients.query.filter_by(login=login.data).first()
        if client:
            raise ValidationError('This login is already taken. Please choose a different one.')

class EmployeeForm(FlaskForm):
    post_id = IntegerField('Post ID', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    telephone = StringField('Telephone', validators=[DataRequired(), Length(min=10, max=15)])
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[Length(min=6)])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Submit')

    def validate_login(self, login: str) -> None:
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
