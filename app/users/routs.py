from flask import render_template, request, flash, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash


users = Blueprint("users", __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        phone = request.form['phone']
        address = request.form['address']

        print(username, password, fullname, phone, address)

        # TODO: Сделать проверку, есть ли уже такой пользователь, и если есть, то выдать flash об ошибке
        
        # hashed_password = generate_password_hash(password, method='sha256')
        # new_user = User(username=username, password=hashed_password, fullname=fullname, phone=phone, address=address)
        
        # db.session.add(new_user)
        # db.session.commit()
        
        flash('Registration successful! You can now log in.', "success")
        return redirect(url_for('login'))
    return render_template('auth_register.html')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username, password)
        # user = User.query.filter_by(username=username).first()
        # if user and check_password_hash(user.password, password):
        #     login_user(user)
        # return redirect(url_for('dashboard'))
        # else:
        #     flash('Invalid username or password')
    return render_template('auth_login.html')
