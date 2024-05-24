from datetime import date

from flask import render_template, request, flash, redirect, url_for, Blueprint, session

from app.models import db, OrderRequest, Orders, Delivery, Services, OrdersStatuses


clients = Blueprint("clients", __name__)


@clients.route('/new_order')
def new_order():
    if session.get('role') != 'client':
        return redirect(url_for('login'))
    services = Services.query.all()
    return render_template('new_order.html', services=services)

@clients.route('/view_orders')
def view_orders():
    if session.get('role') != 'client':
        return redirect(url_for('login'))
    orders = Orders.query.filter_by(client_id=session.get('user_id')).all()
    orders_with_status = []
    for order in orders:
        delivery = Delivery.query.filter_by(order_id=order.id).first()
        status = OrdersStatuses.query.filter_by(delivery_id=delivery.id).first() if delivery else None
        orders_with_status.append({
            'id': order.id,
            'service': Services.query.get(order.service_id).service_name,
            'order_date': order.order_date,
            'status': status
        })
    return render_template('view_orders.html', orders=orders_with_status)

@clients.route('/create_order', methods=['POST'])
def create_order():
    if session.get('role') != 'client':
        return redirect(url_for('login'))
    
    service_id = request.form['service']
    
    new_order = Orders(
        client_id=session.get('user_id'),
        service_id=service_id,
        order_date=date.today()
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    flash('Order created successfully!', 'success')
    return redirect(url_for('view_orders'))

@clients.route('/view_requests')
def view_requests():
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    client_id = session.get('user_id')
    orders = OrderRequest.query.filter_by(client_id=client_id).all()
    return render_template('view_requests.html', orders=orders)

@clients.route('/delete_request/<int:request_id>', methods=['POST', 'DELETE'])
def delete_request(request_id):
    if session.get('role') != 'client':
        return redirect(url_for('users.login'))
    
    # Проверяем, существует ли такая заявка
    order = OrderRequest.query.get(request_id)
    if not order:
        flash('Request not found.', 'danger')
        return redirect(url_for('clients.view_requests'))
    
    # Удаляем заявку
    db.session.delete(order)
    db.session.commit()
    
    flash('Request deleted successfully.', 'success')
    return redirect(url_for('clients.view_requests'))