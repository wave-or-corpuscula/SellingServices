from datetime import date, datetime

from flask import render_template, request, flash, redirect, url_for, Blueprint, session

from app.models import *

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

@employees.route('/create_order/<int:request_id>', methods=['GET', 'POST'])
def create_order(request_id):
    if session.get('role') not in ['employee', 'admin']:
        return redirect(url_for('users.login'))

    order_request = OrderRequest.query.get_or_404(request_id)
    service_objects = ServiceObjects.query.all()

    if request.method == 'POST':
        if 'check_stock' in request.form:
            service_object_id = request.form['service_object']
            count = int(request.form['count'])

            stock_item = StoreHouse.query.filter_by(object_id=service_object_id).first()
            stock_count = stock_item.count if stock_item else 0

            if stock_count >= count:
                flash('Sufficient stock available.', 'success')
            else:
                flash(f'Insufficient stock. Missing {count - stock_count} units.', 'danger')
            return render_template('employee_create_order.html', request=order_request, service_objects=service_objects, checked=True, missing_count=count - stock_count if stock_count < count else 0)

        elif 'create_order' in request.form:
            service_object_id = request.form['service_object']
            count = request.form['count']
            price = request.form['price']
            delivery_date = request.form['delivery_date']

            new_order = Orders(
                client_id=order_request.client_id,
                employee_id=session.get('user_id'),
                service_id=order_request.service_id,
                status=1,  # Assuming 1 is the initial status for a new order
                service_object_id=service_object_id,
                order_date=date.today(),
                count=count,
                price=price
            )

            db.session.add(new_order)
            db.session.commit()

            if delivery_date: 
                new_delivery = Delivery(
                    order_id=new_order.id,
                    delivery_date=datetime.strptime(delivery_date, "%Y-%m-%d").date()
                )

                db.session.add(new_delivery)
                db.session.commit()

            OrderRequest.query.filter_by(id=request_id).delete()
            db.session.commit()

            flash('Order created successfully!', 'success')
            return redirect(url_for('employees.view_requests'))

        elif 'create_request_for_missing_stock' in request.form:
            service_object_id = request.form['service_object']
            missing_count = int(request.form['missing_count'])

            new_stock_request = StoreHouse(
                object_id=service_object_id,
                count=missing_count
            )

            db.session.add(new_stock_request)
            db.session.commit()

            # TODO: Сделать формирование word-документа на дополнительный товар

            flash('Request for missing stock created successfully!', 'success')
            return redirect(url_for('employees.view_requests'))

    return render_template('employee_create_order.html', request=order_request, service_objects=service_objects)

@employees.route('/employee_orders')
def employee_orders():
    if session.get('role') not in ['employee', 'admin']:
        return redirect(url_for('users.login'))

    employee_id = session.get('user_id')
    orders = Orders.query.filter_by(employee_id=employee_id).all()
    
    orders_info = []
    for order in orders:
        client = Clients.query.get(order.client_id)
        service = Services.query.get(order.service_id)
        service_object = ServiceObjects.query.get(order.service_object_id)
        status = OrdersStatuses.query.get(order.status)
        orders_info.append({
            'id': order.id,
            'client_name': client.full_name,
            'service_name': service.service_name,
            'service_object_name': service_object.object_name,
            'order_date': order.order_date,
            'status': status.status_name
        })
    
    return render_template('employee_orders.html', orders=orders_info)

@employees.route('/order/<int:order_id>', methods=['GET', 'POST'])
def view_order(order_id):
    if session.get('role') not in ['employee', 'admin']:
        return redirect(url_for('users.login'))

    order = Orders.query.get_or_404(order_id)
    client = Clients.query.get(order.client_id)
    service = Services.query.get(order.service_id)
    service_objects = ServiceObjects.query.all()
    statuses = OrdersStatuses.query.all()
    delivery = Delivery.query.filter_by(order_id=order_id).first()

    if request.method == 'POST':
        new_status = request.form['status']
        new_delivery_date = request.form['delivery_date']
        new_count = request.form['count']
        new_price = request.form['price']
        new_service_object_id = request.form['service_object_id']
        
        order.status = new_status
        order.count = new_count
        order.price = new_price
        order.service_object_id = new_service_object_id

        if new_delivery_date:
            new_delivery_date = datetime.strptime(new_delivery_date, "%Y-%m-%d").date()
            if delivery:
                delivery.delivery_date = new_delivery_date
            else:
                new_delivery = Delivery(order_id=order_id, delivery_date=new_delivery_date)
                db.session.add(new_delivery)
        
        db.session.commit()
        flash('Order details updated successfully!', 'success')
        return redirect(url_for('employees.view_order', order_id=order_id))

    return render_template('employee_order_detail.html', order=order, client=client, service=service, service_objects=service_objects, statuses=statuses, delivery=delivery)