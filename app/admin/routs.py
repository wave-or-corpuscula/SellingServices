from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from app.models import *
from app.admin.forms import *
from werkzeug.security import generate_password_hash

admin = Blueprint("admin", __name__)

# Admin dashboard
@admin.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    return render_template('admin/dashboard.html')

##########   CLIENT ROUTS    ##########

@admin.route('/admin/clients')
def manage_clients():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    clients = Clients.query.all()
    return render_template('admin/manage_clients.html', clients=clients)

@admin.route('/admin/client/add', methods=['GET', 'POST'])
def add_client():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    form = ClientForm()
    if form.validate_on_submit():
        client = Clients(
            full_name=form.full_name.data,
            address=form.address.data,
            telephone=form.telephone.data,
            login=form.login.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('admin.manage_clients'))
    return render_template('admin/add_client.html', form=form)

@admin.route('/admin/client_edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    client = Clients.query.get_or_404(id)
    form = ClientForm(obj=client)
    return render_template('admin/edit_client.html', form=form, client=client)

@admin.route('/admin/client_update/<int:id>', methods=['GET', 'POST'])
def update_client(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    client = Clients.query.get_or_404(id)
    form = ClientForm(obj=client)
    client.full_name = form.full_name.data
    client.address = form.address.data
    client.telephone = form.telephone.data
    client.login = form.login.data
    if form.password.data:
        client.password = generate_password_hash(form.password.data)
    db.session.commit()
    flash('Client updated successfully!', 'success')
    return redirect(url_for('admin.manage_clients'))

@admin.route('/admin/client/delete/<int:id>')
def delete_client(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    client = Clients.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully!', 'success')
    return redirect(url_for('admin.manage_clients'))

##########   CLIENT ROUTS    ##########

##########   EMPLOYEE ROUTS    ##########

@admin.route('/admin/employees')
def manage_employees():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employees = Employees.query.all()
    return render_template('admin/manage_employees.html', employees=employees)

@admin.route('/admin/add_employee', methods=['GET'])
def add_employee_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    posts = Posts.query.all()
    return render_template('admin/add_employee.html', posts=posts)

@admin.route('/admin/add_employee', methods=['POST'])
def add_employee():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post_id = request.form.get('post_id')
    full_name = request.form.get('full_name')
    telephone = request.form.get('telephone')
    login = request.form.get('login')
    password = generate_password_hash(request.form.get('password'))
    is_admin = bool(request.form.get('is_admin'))
    new_employee = Employees(post_id=post_id, full_name=full_name, telephone=telephone, login=login, password=password, is_admin=is_admin)
    db.session.add(new_employee)
    db.session.commit()
    flash('Сотрудник успешно добавлен!', 'success')
    return redirect(url_for('admin.manage_employees'))

@admin.route('/admin/edit_employee/<int:employee_id>', methods=['GET'])
def edit_employee_form(employee_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employee = Employees.query.get_or_404(employee_id)
    posts = Posts.query.all()
    return render_template('admin/edit_employee.html', employee=employee, posts=posts)

@admin.route('/admin/update_employee/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employee = Employees.query.get_or_404(employee_id)
    employee.post_id = request.form.get('post_id')
    employee.full_name = request.form.get('full_name')
    employee.telephone = request.form.get('telephone')
    employee.login = request.form.get('login')
    if request.form.get('password'):
        employee.password = generate_password_hash(request.form.get('password'))
    employee.is_admin = bool(request.form.get('is_admin'))
    db.session.commit()
    flash('Сотрудник успешно обновлен!', 'success')
    return redirect(url_for('admin.manage_employees'))

@admin.route('/admin/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employee = Employees.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Сотрудник успешно удален!', 'success')
    return redirect(url_for('admin.manage_employees'))

##########   EMPLOYEE ROUTS    ##########

##########   SERVICES ROUTS    ##########

@admin.route('/admin/services')
def manage_services():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    services = Services.query.all()
    return render_template('admin/manage_services.html', services=services)

@admin.route('/admin/add_service', methods=['GET'])
def add_service_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    return render_template('admin/add_service.html')

@admin.route('/admin/add_service', methods=['POST'])
def add_service():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_name = request.form.get('service_name')
    new_service = Services(service_name=service_name)
    db.session.add(new_service)
    db.session.commit()
    flash('Сервис успешно добавлен!', 'success')
    return redirect(url_for('admin.manage_services'))

@admin.route('/admin/edit_service/<int:service_id>', methods=['GET'])
def edit_service_form(service_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service = Services.query.get_or_404(service_id)
    return render_template('admin/edit_service.html', service=service)

@admin.route('/admin/update_service/<int:service_id>', methods=['POST'])
def update_service(service_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service = Services.query.get_or_404(service_id)
    service.service_name = request.form.get('service_name')
    db.session.commit()
    flash('Сервис успешно обновлен!', 'success')
    return redirect(url_for('admin.manage_services'))

@admin.route('/admin/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service = Services.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Сервис успешно удален!', 'success')
    return redirect(url_for('admin.manage_services'))

##########   SERVICES ROUTS    ##########

# Manage Order Statuses
@admin.route('/admin/statuses')
def manage_statuses():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    statuses = OrdersStatuses.query.all()
    return render_template('admin/manage_statuses.html', statuses=statuses)

@admin.route('/admin/status/add', methods=['GET', 'POST'])
def add_status():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    form = StatusForm()
    if form.validate_on_submit():
        status = OrdersStatuses(status_name=form.status_name.data)
        db.session.add(status)
        db.session.commit()
        flash('Status added successfully!', 'success')
        return redirect(url_for('admin.manage_statuses'))
    return render_template('admin/add_status.html', form=form)

@admin.route('/admin/status/edit/<int:id>', methods=['GET', 'POST'])
def edit_status(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    status = OrdersStatuses.query.get_or_404(id)
    form = StatusForm(obj=status)
    if form.validate_on_submit():
        status.status_name = form.status_name.data
        db.session.commit()
        flash('Status updated successfully!', 'success')
        return redirect(url_for('admin.manage_statuses'))
    return render_template('admin/edit_status.html', form=form, status=status)

@admin.route('/admin/status/delete/<int:id>')
def delete_status(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    status = OrdersStatuses.query.get_or_404(id)
    db.session.delete(status)
    db.session.commit()
    flash('Status deleted successfully!', 'success')
    return redirect(url_for('admin.manage_statuses'))


##########   SERVICE OBJECTS ROUTS    ##########

# Управление объектами сервисов
@admin.route('/admin/service_objects')
def manage_service_objects():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_objects = ServiceObjects.query.all()
    return render_template('admin/manage_service_objects.html', service_objects=service_objects)

# Форма добавления объекта сервиса
@admin.route('/admin/add_service_object', methods=['GET'])
def add_service_object_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    return render_template('admin/add_service_object.html')

# Добавление объекта сервиса
@admin.route('/admin/add_service_object', methods=['POST'])
def add_service_object():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    object_name = request.form.get('object_name')
    new_service_object = ServiceObjects(object_name=object_name)
    db.session.add(new_service_object)
    db.session.commit()
    flash('Объект сервиса успешно добавлен!', 'success')
    return redirect(url_for('admin.manage_service_objects'))

# Форма изменения объекта сервиса
@admin.route('/admin/edit_service_object/<int:service_object_id>', methods=['GET'])
def edit_service_object_form(service_object_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_object = ServiceObjects.query.get_or_404(service_object_id)
    return render_template('admin/edit_service_object.html', service_object=service_object)

# Изменение объекта сервиса
@admin.route('/admin/update_service_object/<int:service_object_id>', methods=['POST'])
def update_service_object(service_object_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_object = ServiceObjects.query.get_or_404(service_object_id)
    service_object.object_name = request.form.get('object_name')
    db.session.commit()
    flash('Объект сервиса успешно обновлен!', 'success')
    return redirect(url_for('admin.manage_service_objects'))

# Удаление объекта сервиса
@admin.route('/admin/delete_service_object/<int:service_object_id>', methods=['POST'])
def delete_service_object(service_object_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_object = ServiceObjects.query.get_or_404(service_object_id)
    db.session.delete(service_object)
    db.session.commit()
    flash('Объект сервиса успешно удален!', 'success')
    return redirect(url_for('admin.manage_service_objects'))


##########   SERVICE OBJECTS ROUTS    ##########


##########   POSTS ROUTS   ##########

# Управление постами
@admin.route('/admin/posts')
def manage_posts():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    posts = Posts.query.all()
    return render_template('admin/manage_posts.html', posts=posts)

# Форма добавления поста
@admin.route('/admin/add_post', methods=['GET'])
def add_post_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    return render_template('admin/add_post.html')

# Добавление поста
@admin.route('/admin/add_post', methods=['POST'])
def add_post():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post_name = request.form.get('post_name')
    new_post = Posts(post_name=post_name)
    db.session.add(new_post)
    db.session.commit()
    flash('Пост успешно добавлен!', 'success')
    return redirect(url_for('admin.manage_posts'))

# Форма изменения поста
@admin.route('/admin/edit_post/<int:post_id>', methods=['GET'])
def edit_post_form(post_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post = Posts.query.get_or_404(post_id)
    return render_template('admin/edit_post.html', post=post)

# Изменение поста
@admin.route('/admin/update_post/<int:post_id>', methods=['POST'])
def update_post(post_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post = Posts.query.get_or_404(post_id)
    post.post_name = request.form.get('post_name')
    db.session.commit()
    flash('Пост успешно обновлен!', 'success')
    return redirect(url_for('admin.manage_posts'))

# Удаление поста
@admin.route('/admin/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост успешно удален!', 'success')
    return redirect(url_for('admin.manage_posts'))

##########   POSTS ROUTS   ##########

######### CATEGORIES ROUTS #########

@admin.route('/admin/categories')
def manage_categories():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    categories = Categories.query.all()
    return render_template('admin/manage_categories.html', categories=categories)

@admin.route('/admin/add_category', methods=['POST'])
def add_category():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    cat_name = request.form.get('cat_name')
    new_category = Categories(cat_name=cat_name)
    db.session.add(new_category)
    db.session.commit()
    flash('Category added successfully!', 'success')
    return redirect(url_for('admin.manage_categories'))

@admin.route('/admin/edit_category/<int:category_id>')
def edit_category(category_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    category = Categories.query.get_or_404(category_id)
    return render_template('admin/edit_category.html', category=category)

@admin.route('/admin/update_category/<int:category_id>', methods=['POST'])
def update_category(category_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    category = Categories.query.get_or_404(category_id)
    category.cat_name = request.form.get('cat_name')
    db.session.commit()
    flash('Category updated successfully!', 'success')
    return redirect(url_for('admin.manage_categories'))

@admin.route('/admin/delete_category/<int:category_id>')
def delete_category(category_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    category = Categories.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.manage_categories'))

######### CATEGORIES ROUTS #########

######### SOTREHOUSE ROUTS #########

# Управление объектами на складе
@admin.route('/admin/storehouse')
def manage_storehouse():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    storehouse_items = StoreHouse.query.all()
    return render_template('admin/manage_storehouse.html', storehouse_items=storehouse_items)

# Форма добавления объекта на склад
@admin.route('/admin/add_storehouse_item', methods=['GET'])
def add_storehouse_item_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_objects = ServiceObjects.query.all()
    return render_template('admin/add_storehouse_item.html', service_objects=service_objects)

# Добавление объекта на склад
@admin.route('/admin/add_storehouse_item', methods=['POST'])
def add_storehouse_item():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    object_id = request.form.get('object_id')
    count = request.form.get('count')
    new_storehouse_item = StoreHouse(object_id=object_id, count=count)
    db.session.add(new_storehouse_item)
    db.session.commit()
    flash('Объект успешно добавлен на склад!', 'success')
    return redirect(url_for('admin.manage_storehouse'))

# Форма изменения объекта на складе
@admin.route('/admin/edit_storehouse_item/<int:storehouse_id>', methods=['GET'])
def edit_storehouse_item_form(storehouse_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    storehouse_item = StoreHouse.query.get_or_404(storehouse_id)
    service_objects = ServiceObjects.query.all()
    return render_template('admin/edit_storehouse_item.html', storehouse_item=storehouse_item, service_objects=service_objects)

# Изменение объекта на складе
@admin.route('/admin/update_storehouse_item/<int:storehouse_id>', methods=['POST'])
def update_storehouse_item(storehouse_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    storehouse_item = StoreHouse.query.get_or_404(storehouse_id)
    storehouse_item.object_id = request.form.get('object_id')
    storehouse_item.count = request.form.get('count')
    db.session.commit()
    flash('Объект на складе успешно обновлен!', 'success')
    return redirect(url_for('admin.manage_storehouse'))

# Удаление объекта со склада
@admin.route('/admin/delete_storehouse_item/<int:storehouse_id>', methods=['POST'])
def delete_storehouse_item(storehouse_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    storehouse_item = StoreHouse.query.get_or_404(storehouse_id)
    db.session.delete(storehouse_item)
    db.session.commit()
    flash('Объект со склада успешно удален!', 'success')
    return redirect(url_for('admin.manage_storehouse'))

######### SOTREHOUSE ROUTS #########

######### ORDER STATUSES ROUTS #########

# Управление статусами заказов
@admin.route('/admin/order_statuses')
def manage_order_statuses():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    order_statuses = OrdersStatuses.query.all()
    return render_template('admin/manage_order_statuses.html', order_statuses=order_statuses)

# Форма добавления статуса заказа
@admin.route('/admin/add_order_status', methods=['GET'])
def add_order_status_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    return render_template('admin/add_order_status.html')

# Добавление статуса заказа
@admin.route('/admin/add_order_status', methods=['POST'])
def add_order_status():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    status_name = request.form.get('status_name')
    new_order_status = OrdersStatuses(status_name=status_name)
    db.session.add(new_order_status)
    db.session.commit()
    flash('Статус заказа успешно добавлен!', 'success')
    return redirect(url_for('admin.manage_order_statuses'))

# Форма изменения статуса заказа
@admin.route('/admin/edit_order_status/<int:status_id>', methods=['GET'])
def edit_order_status_form(status_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    order_status = OrdersStatuses.query.get_or_404(status_id)
    return render_template('admin/edit_order_status.html', order_status=order_status)

# Изменение статуса заказа
@admin.route('/admin/update_order_status/<int:status_id>', methods=['POST'])
def update_order_status(status_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    order_status = OrdersStatuses.query.get_or_404(status_id)
    order_status.status_name = request.form.get('status_name')
    db.session.commit()
    flash('Статус заказа успешно обновлен!', 'success')
    return redirect(url_for('admin.manage_order_statuses'))

# Удаление статуса заказа
@admin.route('/admin/delete_order_status/<int:status_id>', methods=['POST'])
def delete_order_status(status_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    order_status = OrdersStatuses.query.get_or_404(status_id)
    db.session.delete(order_status)
    db.session.commit()
    flash('Статус заказа успешно удален!', 'success')
    return redirect(url_for('admin.manage_order_statuses'))

######### ORDER STATUSES ROUTS #########

######### SUB CATOGORIES ROUTS #########

# Управление подкатегориями
@admin.route('/admin/subcategories')
def manage_subcategories():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    subcategories = SubCategories.query.order_by(SubCategories.cat_id)
    return render_template('admin/manage_subcategories.html', subcategories=subcategories)

# Форма добавления подкатегории
@admin.route('/admin/add_subcategory', methods=['GET'])
def add_subcategory_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    categories = Categories.query.all()
    return render_template('admin/add_subcategory.html', categories=categories)

# Добавление подкатегории
@admin.route('/admin/add_subcategory', methods=['POST'])
def add_subcategory():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    subcat_name = request.form.get('subcat_name')
    cat_id = request.form.get('cat_id')
    new_subcategory = SubCategories(subcat_name=subcat_name, cat_id=cat_id)
    db.session.add(new_subcategory)
    db.session.commit()
    flash('Подкатегория успешно добавлена!', 'success')
    return redirect(url_for('admin.manage_subcategories'))

# Форма изменения подкатегории
@admin.route('/admin/edit_subcategory/<int:subcat_id>', methods=['GET'])
def edit_subcategory_form(subcat_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    subcategory = SubCategories.query.get_or_404(subcat_id)
    categories = Categories.query.all()
    return render_template('admin/edit_subcategory.html', subcategory=subcategory, categories=categories)

# Изменение подкатегории
@admin.route('/admin/update_subcategory/<int:subcat_id>', methods=['POST'])
def update_subcategory(subcat_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    subcategory = SubCategories.query.get_or_404(subcat_id)
    subcategory.subcat_name = request.form.get('subcat_name')
    subcategory.cat_id = request.form.get('cat_id')
    db.session.commit()
    flash('Подкатегория успешно обновлена!', 'success')
    return redirect(url_for('admin.manage_subcategories'))

# Удаление подкатегории
@admin.route('/admin/delete_subcategory/<int:subcat_id>', methods=['POST'])
def delete_subcategory(subcat_id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    subcategory = SubCategories.query.get_or_404(subcat_id)
    db.session.delete(subcategory)
    db.session.commit()
    flash('Подкатегория успешно удалена!', 'success')
    return redirect(url_for('admin.manage_subcategories'))

######### SUB CATOGORIES ROUTS #########

######### OBJECT CATOGORIES ROUTS #########

# Управление присвоением объектов к категориям
@admin.route('/admin/objectscategories')
def manage_objectscategories():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    objectscategories = ObjectsCategories.query.order_by(ObjectsCategories.object_id)
    objects = ServiceObjects.query.all()
    categories = Categories.query.all()
    return render_template('admin/manage_objectscategories.html', objectscategories=objectscategories, objects=objects, categories=categories)

# Форма добавления присвоения объекта к категории
@admin.route('/admin/add_objectcategory', methods=['GET'])
def add_objectcategory_form():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    objects = ServiceObjects.query.all()
    categories = Categories.query.all()
    return render_template('admin/add_objectcategory.html', objects=objects, categories=categories)

# Добавление присвоения объекта к категории
@admin.route('/admin/add_objectcategory', methods=['POST'])
def add_objectcategory():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    object_id = request.form.get('object_id')
    cat_id = request.form.get('cat_id')
    new_objectcategory = ObjectsCategories(object_id=object_id, cat_id=cat_id)
    db.session.add(new_objectcategory)
    db.session.commit()
    flash('Объект успешно присвоен категории!', 'success')
    return redirect(url_for('admin.manage_objectscategories'))

# Форма изменения присвоения объекта к категории
@admin.route('/admin/edit_objectcategory/<int:id>', methods=['GET'])
def edit_objectcategory_form(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    objectcategory = ObjectsCategories.query.get_or_404(id)
    objects = ServiceObjects.query.all()
    categories = Categories.query.all()
    return render_template('admin/edit_objectcategory.html', objectcategory=objectcategory, objects=objects, categories=categories)

# Изменение присвоения объекта к категории
@admin.route('/admin/update_objectcategory/<int:id>', methods=['POST'])
def update_objectcategory(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    objectcategory = ObjectsCategories.query.get_or_404(id)
    objectcategory.object_id = request.form.get('object_id')
    objectcategory.cat_id = request.form.get('cat_id')
    db.session.commit()
    flash('Присвоение объекта к категории успешно обновлено!', 'success')
    return redirect(url_for('admin.manage_objectscategories'))

# Удаление присвоения объекта к категории
@admin.route('/admin/delete_objectcategory/<int:id>', methods=['POST'])
def delete_objectcategory(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    objectcategory = ObjectsCategories.query.get_or_404(id)
    db.session.delete(objectcategory)
    db.session.commit()
    flash('Присвоение объекта к категории успешно удалено!', 'success')
    return redirect(url_for('admin.manage_objectscategories'))

######### OBJECT CATOGORIES ROUTS #########
