from datetime import date, datetime

from flask import jsonify

from flask import render_template, request, flash, redirect, url_for, Blueprint, session

from docxtpl import DocxTemplate

from app.models import *
from app.employees.utils import ResponseToJS, OrderInfo

employees = Blueprint("employees", __name__)


@employees.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee/employee_dashboard.html')

@employees.route('/view_requests')
def view_requests():
    requests = OrderRequest.query.all()
    
    return render_template('employee/employee_view_requests.html', requests=requests)

@employees.route('/create_order/<int:request_id>', methods=['GET', 'POST'])
def create_order(request_id):
    if session.get('role') not in ['employee', 'admin']:
        return redirect(url_for('users.login'))

    order_request = OrderRequest.query.get_or_404(request_id)
    service_objects = ServiceObjects.query.all()
    order_statuses = OrdersStatuses.query.all()

    if request.method == 'POST':
        request_data = request.get_json().get("orderInfo")
        request_status = request.get_json().get("status")
        # if 'check_stock' in request.form:
        #     service_object_id = request.form['service_object']
        #     count = int(request.form['count'])

        #     stock_item = StoreHouse.query.filter_by(object_id=service_object_id).first()
        #     stock_count = stock_item.count if stock_item else 0

        #     if stock_count >= count:
        #         flash('Sufficient stock available.', 'success')
        #     else:
        #         flash(f'Insufficient stock. Missing {count - stock_count} units.', 'danger')
        #     return render_template('employee/employee_create_order.html', request=order_request, service_objects=service_objects, checked=True, missing_count=count - stock_count if stock_count < count else 0)
        
        if request_status == "create_order":
            try:
                create_complete_order(request_data)
            except Exception as e:
                return jsonify(ResponseToJS(
                    message=e.args[0],
                    status="danger"
                ).__dict__)

            OrderRequest.query.filter_by(id=request_id).delete()
            db.session.commit()

            flash('Заказ успешно создан!', 'success')
            return jsonify(ResponseToJS(
                    message="Заказ успешно создан!",
                    status="success",
                    url="/view_requests"
                ).__dict__)


            # return redirect(url_for('employees.view_requests'))

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

    return render_template('employee/employee_create_order.html', 
                           request=order_request, 
                           service_objects=service_objects,
                           order_statuses=order_statuses)

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
        status = OrdersStatuses.query.get(order.status_id)
        orders_info.append({
            'id': order.id,
            'client_name': client.full_name,
            'service_name': service.service_name,
            'order_date': order.order_date,
            'status': status.status_name
        })
    
    return render_template('employee/employee_orders.html', orders=orders_info)


@employees.route("/update_order/<int:order_id>", methods=['GET', 'POST'])
def update_order(order_id: int):
    if request.method == "POST":
        request_data = request.get_json().get("orderInfo")
        
        order_to_delete = db.session.query(Orders).get(order_id)
        db.session.delete(order_to_delete)
        db.session.commit()

        try:
            create_complete_order(request_data)
        except Exception as e:
            return jsonify(ResponseToJS(
                message=e.args[0],
                status="danger"
            ).__dict__)

        flash('Заказ успешно обновлен!', 'success')
        return jsonify(ResponseToJS(
                message="Заказ успешно обновлен!",
                status="success",
                url="/employee_orders"
            ).__dict__)


@employees.route('/employee/order/<int:order_id>', methods=['GET', 'POST'])
def order_details(order_id):
    if session.get('role') != 'employee':
        return redirect(url_for('users.login'))
    order = Orders.query.get_or_404(order_id)
    ordered_objects = OrderedObjects.query.filter_by(order_id=order.id).all()
    service_objects = ServiceObjects.query.all()
    order_statuses = OrdersStatuses.query.all()
    delivery = Delivery.query.filter_by(order_id=order.id).first()

    return render_template(
        'employee/order_details.html',
        order=order,
        ordered_objects=ordered_objects,
        service_objects=service_objects,
        order_statuses=order_statuses,
        delivery=delivery
    )

@employees.route('/employee/load_categories/<int:object_id>')
def load_categories(object_id):
    object_categories = ObjectsCategories.query.filter_by(object_id=object_id).all()
    categories = []
    for obj_cat in object_categories:
        category = Categories.query.get(obj_cat.cat_id)
        categories.append({'id': category.id, 'name': category.cat_name})
    return jsonify(categories)


@employees.route('/employee/load_service_objects')
def load_service_objects():
    service_objects = ServiceObjects.query.all()
    serv_objs_list = [{'id': so.id, 'name': so.object_name, 'cost': so.cost} for so in service_objects]
    return jsonify(serv_objs_list)


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


@employees.route("/get_order_info/<int:order_id>")
def get_order_info(order_id: int):
    order = Orders.query.get_or_404(order_id)
    objects_info = []
    ordered_objects = OrderedObjects.query.filter_by(order_id=order.id)
    for obj in ordered_objects:
        ord_obj_cats = OrderedObjectCategories.query.filter_by(order_id=order.id, object_id=obj.object_id)
        
        objects_info.append({
            "object": obj.object_id, 
            "cats": [cat.cat_id for cat in ord_obj_cats], 
            "subcats": [cat.subcat_id for cat in ord_obj_cats]
            })
    
    return jsonify(objects_info)


@employees.route("/create_report/<int:order_id>")
def create_report(order_id: int):
    try:
        order = Orders.query.get(order_id)
        doc = DocxTemplate("documents/template.docx")

        objects = []
        order_cost = order.service.cost
        ordered_objs = OrderedObjects.query.filter_by(order_id=order.id)
        for ordered_obj in ordered_objs:
            object_cost = ordered_obj.object.cost
            amount = ordered_obj.count
            ord_objs_cats = OrderedObjectCategories.query.filter_by(order_id=order.id, object_id=ordered_obj.object_id)
            subcats_list = []
            for ord_obj_cats in ord_objs_cats:
                if ord_obj_cats.subcategory:
                    subcats_list.append(ord_obj_cats.subcategory.subcat_name)
                    object_cost += ord_obj_cats.subcategory.cost
            objects.append({
                "name": f"{ordered_obj.object.object_name}: {', '.join(subcats_list)}",
                "col": amount,
                "one": object_cost,
                "all": object_cost * amount
            })
            order_cost += object_cost * amount

        context = {
            "order_id": order_id,
            "order_date": order.order_date,
            "employee_name": order.employee.full_name,
            "client_name": order.client.full_name,
            "objects": objects,
            "total_price": order_cost,
            "service_name": order.service.service_name
        }

        # Рендеринг шаблона
        doc.render(context)
        doc_name = f"Отчет по заказу {order_id}.docx"
        doc.save(f"documents/{doc_name}")
        flash(f"Договор '{doc_name}' создан.", "success")
    except Exception as e:
        print(e)
        flash("Ошибка при создании отчета", "danger")

    return redirect(url_for("employees.employee_orders"))

def create_complete_order(request_data):
    order_info = OrderInfo(request_data)
    
    new_order = Orders(
        client_id=order_info.client_id,
        employee_id=session.get('user_id'),
        service_id=order_info.service_id,
        status_id=order_info.status_id,
        order_date=date.today()
    )

    db.session.add(new_order)
    db.session.commit()

    if order_info.delivery_date: 
        new_delivery = Delivery(
            order_id=new_order.id,
            delivery_date=order_info.delivery_date
        )

        db.session.add(new_delivery)
        db.session.commit()

    for ordered_object in order_info.objects:
        new_object = OrderedObjects(
            order_id=new_order.id,
            object_id=ordered_object.id,
            count=ordered_object.amount
        )

        db.session.add(new_object)
        db.session.commit()

        for cat, subcat in zip(ordered_object.cats, ordered_object.subcats):
            new_ordered_categories = OrderedObjectCategories(
                order_id=new_order.id,
                object_id=ordered_object.id,
                cat_id=cat,
                subcat_id=subcat
            )
            db.session.add(new_ordered_categories)
            db.session.commit()