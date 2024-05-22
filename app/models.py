from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    telephone = db.Column(db.String(50), unique=True, nullable=False)
    login = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    telephone = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(150), unique=True, nullable=False)


class TypeOfService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_type_name = db.Column(db.String(150), unique=True, nullable=False)


class Purveyor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_info = db.Column(db.Text, nullable=False)


class StoreHouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeofservice_id = db.Column(db.Integer, db.ForeignKey('type_of_service.id'), nullable=False)
    purveyor_id = db.Column(db.Integer, db.ForeignKey('purveyor.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeofservice_id = db.Column(db.Integer, db.ForeignKey('type_of_service.id'), nullable=False)
    service_name = db.Column(db.String(150), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)


class OrderStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    status_name = db.Column(db.String(150), nullable=False)


class GeneratedOrder(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
