from app import db


class Clients(db.Model):
    __tablename__ = 'Clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    telephone = db.Column(db.String(50), unique=True, nullable=False)
    login = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Client('{self.full_name}', '{self.address}', '{self.telephone}')"


class Employees(db.Model):
    __tablename__ = 'Employees'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    telephone = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Employee('{self.full_name}', '{self.telephone}')"


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f"Post('{self.post_name}')"


class ServiceObjects(db.Model):
    __tablename__ = 'ServiceObjects'
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"ServiceObject('{self.object_name}')"


class StoreHouse(db.Model):
    __tablename__ = 'StoreHouse'
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('ServiceObjects.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"StoreHouse('{self.object_id}', '{self.count}')"


class Services(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Service('{self.service_name}')"


class OrderRequest(db.Model):
    __tablename__ = 'OrderRequest'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)

    client = db.relationship('Clients', backref=db.backref('order_requests', lazy=True))
    service = db.relationship('Services', backref=db.backref('order_requests', lazy=True))

    def __repr__(self):
        return f"OrderRequest('{self.client_id}', '{self.service_id}', '{self.order_date}')"


class OrdersStatuses(db.Model):
    __tablename__ = 'OrdersStatuses'
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"OrderStatus('{self.status_name}')"


class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employees.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('OrdersStatuses.id'), nullable=False)
    service_object_id = db.Column(db.Integer, db.ForeignKey('ServiceObjects.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order('{self.client_id}', '{self.employee_id}', '{self.service_id}', '{self.status}', '{self.service_object_id}', '{self.order_date}', '{self.count}', '{self.price}')"


class Delivery(db.Model):
    __tablename__ = 'Delivery'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Delivery('{self.order_id}', '{self.delivery_date}')"

