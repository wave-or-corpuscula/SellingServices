from flask import jsonify

from datetime import date, datetime

from flask import render_template, request, flash, redirect, url_for, Blueprint, session

from app.models import *

employees = Blueprint("employees", __name__)


@employees.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee/employee_dashboard.html')

@employees.route('/view_requests')
def view_requests():
    requests = OrderRequest.query.all()
    
    return render_template('employee/employee_view_requests.html', requests=requests)

@employees.route('/view_orders')
def view_orders():
    if session.get('role') not in ['employee', 'admin']:
        return redirect(url_for('users.login'))
    # Логика для получения и отображения заказов
    return render_template('employee/employee_view_orders.html')

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
            return render_template('employee/employee_create_order.html', request=order_request, service_objects=service_objects, checked=True, missing_count=count - stock_count if stock_count < count else 0)

        elif 'create_order' in request.form:
            count = request.form['count']
            price = request.form['price']
            delivery_date = request.form['delivery_date']

            new_order = Orders(
                client_id=order_request.client_id,
                employee_id=session.get('user_id'),
                service_id=order_request.service_id,
                status=1,  # Assuming 1 is the initial status for a new order
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

    return render_template('employee/employee_create_order.html', request=order_request, service_objects=service_objects)

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
        status = OrdersStatuses.query.get(order.status)
        orders_info.append({
            'id': order.id,
            'client_name': client.full_name,
            'service_name': service.service_name,
            'order_date': order.order_date,
            'status': status.status_name
        })
    
    return render_template('employee/employee_orders.html', orders=orders_info)


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

    return render_template('employee/employee_order_detail.html', order=order, client=client, service=service, service_objects=service_objects, statuses=statuses, delivery=delivery)


@employees.route('/employee/order/<int:order_id>', methods=['GET', 'POST'])
def order_details(order_id):
    if session.get('role') != 'employee':
        return redirect(url_for('users.login'))
    order = Orders.query.get_or_404(order_id)
    ordered_objects = OrderedObjects.query.filter_by(order_id=order.id).all()
    service_objects = ServiceObjects.query.all()
    order_statuses = OrdersStatuses.query.all()
    
    if request.method == 'POST':
        order.status = request.form['status']
        order.order_date = request.form['order_date']
        db.session.commit()

        OrderedObjects.query.filter_by(order_id=order.id).delete()
        
        object_ids = request.form.getlist('object_id')
        cat_ids = request.form.getlist('cat_id')
        sub_cat_ids = request.form.getlist('sub_cat_id')
        counts = request.form.getlist('count')
        prices = request.form.getlist('price')

        for i in range(len(object_ids)):
            new_ordered_object = OrderedObjects(
                order_id=order.id,
                object_id=int(object_ids[i]),
                cat_id=int(cat_ids[i]),
                sub_cat_id=int(sub_cat_ids[i]),
                count=int(counts[i]),
                price=int(prices[i])
            )
            db.session.add(new_ordered_object)
        db.session.commit()
        
        flash('Order updated successfully!', 'success')
        return redirect(url_for('employee.order_details', order_id=order.id))

    return render_template(
        'employee/order_details.html',
        order=order,
        ordered_objects=ordered_objects,
        service_objects=service_objects,
        order_statuses=order_statuses
    )

@employees.route('/employee/load_categories/<int:object_id>')
def load_categories(object_id):
    object_categories = ObjectsCategories.query.filter_by(object_id=object_id).all()
    categories = []
    for obj_cat in object_categories:
        category = Categories.query.get(obj_cat.cat_id)
        categories.append({'id': category.id, 'name': category.cat_name})
    return jsonify(categories)

@employees.route('/employee/load_subcategories/<int:category_id>')
def load_subcategories(category_id):
    subcategories = SubCategories.query.filter_by(cat_id=category_id).all()
    subcat_list = [{'id': subcat.id, 'name': subcat.subcat_name} for subcat in subcategories]
    return jsonify(subcat_list)

@employees.route('/employee/load_service_objects')
def load_service_objects():
    service_objects = ServiceObjects.query.all()
    serv_objs_list = [{'id': so.id, 'name': so.object_name, 'cost': so.cost} for so in service_objects]
    return jsonify(serv_objs_list)

@employees.route('/get_service_objects_list')
def get_service_objects_list():
    so = ServiceObjects.query.all()
    return jsonify({"html": render_template("employee/service_objects_list.html", service_objects=so)})


@employees.route("/get_object_categories/")
def get_object_categories_void():
    return jsonify({"object_categories": [], "category_subcategories": []}) 


@employees.route("/get_object_categories/<int:object_id>")
def get_object_categories(object_id):
    if object_id == "":
        object_categories = []    
        category_subcats = []
    else:
        obj_cats = ObjectsCategories.query.filter_by(object_id=object_id)
        object_categories = [{"id": oc.id, "name": oc.category.cat_name} for oc in obj_cats]
        category_subcats = []
        for cat in obj_cats:
            cat_subcats = SubCategories.query.filter_by(cat_id=cat.id)
            category_subcats.append([{"id": cs.id, "name": cs.subcat_name, "cost": cs.cost} for cs in cat_subcats])
    return jsonify({"object_categories": object_categories, "category_subcategories": category_subcats}) 

@employees.route("/get_service_object_item/<int:object_index>")
def get_service_object_item(object_index: int):
    return render_template("employee/service_object_item.html", service_object_id=object_index)

