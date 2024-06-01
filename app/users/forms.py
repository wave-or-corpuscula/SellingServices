from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp


class RegistrationForm(FlaskForm):

    full_name = StringField('ФИО', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[
        DataRequired(), 
        Regexp(r'^[\d\s()+]+$', message="Невалидный телефон.")])
    address = StringField('Адрес', validators=[DataRequired(message="Обязательное поле")])
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):

    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField("Войти")