from datetime import date

from flask import render_template, request, flash, redirect, url_for, Blueprint, session

from app.models import db, OrderRequest, Orders, Delivery, Services, OrdersStatuses, Employees, ServiceObjects
from app.clients.utils import get_order_total_cost

clients = Blueprint("clients", __name__)


@clients.route('/view_client_orders')
def view_client_orders():
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    
    client_id = session.get('user_id')
    orders = Orders.query.filter_by(client_id=client_id).all()
    
    orders_with_details = []
    for order in orders:
        service = Services.query.get(order.service_id)
        status = OrdersStatuses.query.get(order.status_id)
        delivery = Delivery.query.filter_by(order_id=order.id).first()
        delivery_date = delivery.delivery_date if delivery else None
        employee = Employees.query.get(order.employee_id)
        
        orders_with_details.append({
            'id': order.id,
            'service_name': service.service_name,
            'order_date': order.order_date,
            'status_name': status.status_name,
            'delivery_date': delivery_date,
            'total_price': str(get_order_total_cost(order.id)),
            'employee_telephone': employee.telephone if employee else 'N/A',
        })
    
    return render_template('client/view_orders.html', orders=orders_with_details)

@clients.route('/new_client_request', methods=['GET', 'POST'])
def new_client_request():
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    
    if request.method == 'POST':
        service_id = request.form['service_id']
        client_id = session.get('user_id')
        order_date = date.today()
        
        new_order_request = OrderRequest(
            client_id=client_id,
            service_id=service_id,
            order_date=order_date
        )
        
        db.session.add(new_order_request)
        db.session.commit()
        
        flash('Заявка успешно создана!', 'success')
        return redirect(url_for('clients.new_client_request'))
    
    services = Services.query.all()
    return render_template('client/new_request.html', services=services)

@clients.route('/view_client_requests')
def view_client_requests():
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    client_id = session.get('user_id')
    orders = OrderRequest.query.filter_by(client_id=client_id).all()
    return render_template('client/view_requests.html', orders=orders)

@clients.route('/delete_request/<int:request_id>', methods=['POST', 'DELETE'])
def delete_request(request_id):
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    
    # Проверяем, существует ли такая заявка
    order = OrderRequest.query.get(request_id)
    if not order:
        flash('Запрос не найден.', 'danger')
        return redirect(url_for('clients.view_client_requests'))
    
    # Удаляем заявку
    db.session.delete(order)
    db.session.commit()
    
    flash('Заявка удалена.', 'success')
    return redirect(url_for('clients.view_client_requests'))