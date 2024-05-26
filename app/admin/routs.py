from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from app.models import db, Clients, Employees, Services, OrdersStatuses, ServiceObjects, Posts
from app.admin.forms import ClientForm, EmployeeForm, ServiceForm, StatusForm, ServiceObjectForm, PostForm
from werkzeug.security import generate_password_hash

admin = Blueprint("admin", __name__)

# Admin dashboard
@admin.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    return render_template('admin/dashboard.html')

# Manage Clients
@admin.route('/admin/clients')
def manage_clients():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    clients = Clients.query.all()
    return render_template('admin/clients.html', clients=clients)

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

@admin.route('/admin/client/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    client = Clients.query.get_or_404(id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.full_name = form.full_name.data
        client.address = form.address.data
        client.telephone = form.telephone.data
        client.login = form.login.data
        if form.password.data:
            client.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('admin.manage_clients'))
    return render_template('admin/edit_client.html', form=form, client=client)

@admin.route('/admin/client/delete/<int:id>')
def delete_client(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    client = Clients.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully!', 'success')
    return redirect(url_for('admin.manage_clients'))

# Manage Employees
@admin.route('/admin/employees')
def manage_employees():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employees = Employees.query.all()
    return render_template('admin/manage_employees.html', employees=employees)

@admin.route('/admin/employee/add', methods=['GET', 'POST'])
def add_employee():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    form = EmployeeForm()
    form.post_id.choices = [(post.id, post.post_name) for post in Posts.query.all()]
    if form.validate_on_submit():
        employee = Employees(
            full_name=form.full_name.data,
            telephone=form.telephone.data,
            login=form.login.data,
            password=generate_password_hash(form.password.data),
            post_id=form.post_id.data,
            is_admin=form.is_admin.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('admin.manage_employees'))
    return render_template('admin/add_employee.html', form=form)

@admin.route('/admin/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employee = Employees.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    form.post_id.choices = [(post.id, post.post_name) for post in Posts.query.all()]
    if form.validate_on_submit():
        employee.full_name = form.full_name.data
        employee.telephone = form.telephone.data
        employee.login = form.login.data
        if form.password.data:
            employee.password = generate_password_hash(form.password.data)
        employee.post_id = form.post_id.data
        employee.is_admin = form.is_admin.data
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('admin.manage_employees'))
    return render_template('admin/edit_employee.html', form=form, employee=employee)

@admin.route('/admin/employee/delete/<int:id>')
def delete_employee(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    employee = Employees.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('admin.manage_employees'))

# Manage Services
@admin.route('/admin/services')
def manage_services():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    services = Services.query.all()
    return render_template('admin/manage_services.html', services=services)

@admin.route('/admin/service/add', methods=['GET', 'POST'])
def add_service():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    form = ServiceForm()
    if form.validate_on_submit():
        service = Services(service_name=form.service_name.data)
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin.manage_services'))
    return render_template('admin/add_service.html', form=form)

@admin.route('/admin/service/edit/<int:id>', methods=['GET', 'POST'])
def edit_service(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service = Services.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.service_name = form.service_name.data
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin.manage_services'))
    return render_template('admin/edit_service.html', form=form, service=service)

@admin.route('/admin/service/delete/<int:id>')
def delete_service(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service = Services.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin.manage_services'))

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

# Manage Service Objects
@admin.route('/admin/service_objects')
def manage_service_objects():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_objects = ServiceObjects.query.all()
    return render_template('admin/manage_service_objects.html', service_objects=service_objects)

@admin.route('/admin/service_object/add', methods=['GET', 'POST'])
def add_service_object():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    form = ServiceObjectForm()
    if form.validate_on_submit():
        service_object = ServiceObjects(object_name=form.object_name.data)
        db.session.add(service_object)
        db.session.commit()
        flash('Service object added successfully!', 'success')
        return redirect(url_for('admin.manage_service_objects'))
    return render_template('admin/add_service_object.html', form=form)

@admin.route('/admin/service_object/edit/<int:id>', methods=['GET', 'POST'])
def edit_service_object(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_object = ServiceObjects.query.get_or_404(id)
    form = ServiceObjectForm(obj=service_object)
    if form.validate_on_submit():
        service_object.object_name = form.object_name.data
        db.session.commit()
        flash('Service object updated successfully!', 'success')
        return redirect(url_for('admin.manage_service_objects'))
    return render_template('admin/edit_service_object.html', form=form, service_object=service_object)

@admin.route('/admin/service_object/delete/<int:id>')
def delete_service_object(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    service_object = ServiceObjects.query.get_or_404(id)
    db.session.delete(service_object)
    db.session.commit()
    flash('Service object deleted successfully!', 'success')
    return redirect(url_for('admin.manage_service_objects'))

# Manage Posts
@admin.route('/admin/posts')
def manage_posts():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    posts = Posts.query.all()
    return render_template('admin/manage_posts.html', posts=posts)

@admin.route('/admin/post/add', methods=['GET', 'POST'])
def add_post():
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(post_name=form.post_name.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect(url_for('admin.manage_posts'))
    return render_template('admin/add_post.html', form=form)

@admin.route('/admin/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post = Posts.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.post_name = form.post_name.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin.manage_posts'))
    return render_template('admin/edit_post.html', form=form, post=post)

@admin.route('/admin/post/delete/<int:id>')
def delete_post(id):
    if session.get('role') != 'admin':
        return redirect(url_for('users.login'))
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin.manage_posts'))
