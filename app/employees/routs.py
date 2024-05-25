from datetime import date

from flask import render_template, request, flash, redirect, url_for, Blueprint, session

from app.models import db, OrderRequest, Orders, Delivery, Services, OrdersStatuses, Employees, ServiceObjects

employees = Blueprint("employees", __name__)


@employees.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')

@employees.route('/view_requests')
def view_requests():
    requests = OrderRequest.query.all()
    
    return render_template('employee_view_requests.html', requests=requests)

@employees.route('/view_orders')
def view_orders():
    if session.get('role') not in ['employee', 'admin']:
        return redirect(url_for('users.login'))
    # Логика для получения и отображения заказов
    return render_template('employee_view_orders.html')