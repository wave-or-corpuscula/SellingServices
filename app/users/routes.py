from flask import render_template, request, flash, redirect, url_for, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.users.forms import LoginForm, RegistrationForm
from app.models import db, Clients, Employees


users = Blueprint("users", __name__)


@users.route("/home")
def home():
    return render_template("home.html")

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        address = form.address.data
        telephone = form.phone.data
        password = form.password.data
        username = form.username.data

        # Проверка на существующего пользователя
        existing_user = Clients.query.filter((Clients.login == username) | (Clients.telephone == telephone)).first()
        existing_employee = Employees.query.filter((Employees.login == username) | (Employees.telephone == telephone)).first()
        if existing_user or existing_employee:
            flash('Имя пользователя или телефон уже существуют', 'danger')
            return redirect(url_for('users.register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = Clients(full_name=full_name, address=address, telephone=telephone, login=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь можете войти', "success")
        return redirect(url_for('users.login'))
    return render_template('auth_register.html', form=form)

@users.route("/")
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        client = Clients.query.filter_by(login=username).first()
        employee = Employees.query.filter_by(login=username).first()

        if client and check_password_hash(client.password, password):
            session['user_id'] = client.id
            session['role'] = 'client'
            return redirect(url_for('users.client_dashboard'))
        elif employee and check_password_hash(employee.password, password):
            session['user_id'] = employee.id
            session['role'] = 'admin' if employee.is_admin else 'employee'
            return redirect(url_for('users.employee_dashboard'))
        else:
            flash('Вход не удался. Проверьте имя пользователя или пароль', 'danger')
    return render_template('auth_login.html', form=form)

@users.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@users.route('/client_dashboard')
def client_dashboard():
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    return render_template('dashboard_client.html')

@users.route('/employee_dashboard')
def employee_dashboard():
    if session.get('role') == 'employee':
        return render_template('employee/dashboard_employee.html')
    elif session.get('role') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))#('admin/admin_dashboard.html')
    return redirect(url_for('users.login'))
