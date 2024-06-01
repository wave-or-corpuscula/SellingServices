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

    post = db.relationship('Posts', backref=db.backref('Employees', lazy=True))

    def __repr__(self):
        return f"Employee('{self.full_name}', '{self.telephone}')"


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f"Post('{self.post_name}')"

class StoreHouse(db.Model):
    __tablename__ = 'StoreHouse'
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('ServiceObjects.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    service_object = db.relationship("ServiceObjects", backref=db.backref("StoreHouse", lazy=True))

    def __repr__(self):
        return f"StoreHouse('{self.object_id}', '{self.count}')"


class Services(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(150), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Service('{self.service_name}')"


class OrderRequest(db.Model):
    __tablename__ = 'OrderRequest'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'))
    order_date = db.Column(db.Date, nullable=False)

    client = db.relationship('Clients', backref=db.backref('OrderRequest', lazy=True))
    service = db.relationship('Services', backref=db.backref('OrderRequest', lazy=True))

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
    status_id = db.Column(db.Integer, db.ForeignKey('OrdersStatuses.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)

    client = db.relationship('Clients', backref=db.backref('OrderedObjects', lazy=True))
    employee = db.relationship('Employees', backref=db.backref('OrderedObjects', lazy=True))
    service = db.relationship('Services', backref=db.backref('OrderedObjects', lazy=True))
    status = db.relationship('OrdersStatuses', backref=db.backref('OrderedObjects', lazy=True))

    def __repr__(self):
        return f"Order('{self.client_id}', '{self.employee_id}', '{self.service_id}', '{self.status}', '{self.service_object_id}', '{self.order_date}', '{self.count}', '{self.price}')"


class OrderedObjects(db.Model):
    __tablename__ = 'OrderedObjects'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    object_id = db.Column(db.Integer, db.ForeignKey('ServiceObjects.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    object = db.relationship('ServiceObjects', backref=db.backref('OrderedObjects', lazy=True))


class OrderedObjectCategories(db.Model):
    __tablename__ = 'OrderedObjectCategories'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("Orders.id"), nullable=False)
    object_id = db.Column(db.Integer, db.ForeignKey("ServiceObjects.id"), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey("Categories.id"), nullable=False)
    subcat_id = db.Column(db.Integer, db.ForeignKey("SubCategories.id"))

    order = db.relationship("Orders", backref=db.backref("OrderedObjectCategories", lazy=True))
    object = db.relationship("ServiceObjects", backref=db.backref("OrderedObjectCategories", lazy=True))
    subcategory = db.relationship("SubCategories", backref=db.backref("OrderedObjectCategories", lazy=True))
    category = db.relationship("Categories", backref=db.backref("OrderedObjectCategories", lazy=True))


class Delivery(db.Model):
    __tablename__ = 'Delivery'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Delivery('{self.order_id}', '{self.delivery_date}')"
    

class Categories(db.Model):
    __tablename__ = 'Categories'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String, nullable=False)


class SubCategories(db.Model):
    __tablename__ = 'SubCategories'
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
    subcat_name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    category = db.relationship("Categories", backref=db.backref('SubCategories', lazy=True))


class ObjectsCategories(db.Model):
    __tablename__ = 'ObjectsCategories'
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('ServiceObjects.id'), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)

    object = db.relationship("ServiceObjects", backref=db.backref("ObjectsCategories", lazy=True))
    category = db.relationship("Categories", backref=db.backref("ObjectsCategories", lazy=True))


class ServiceObjects(db.Model):
    __tablename__ = 'ServiceObjects'
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(150), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"ServiceObject('{self.object_name}')"
