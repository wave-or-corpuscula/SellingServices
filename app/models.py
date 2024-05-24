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
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"Employee('{self.full_name}', '{self.telephone}')"


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f"Post('{self.post_name}')"


class TypesOfService(db.Model):
    __tablename__ = 'TypesOfService'
    id = db.Column(db.Integer, primary_key=True)
    service_type_name = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f"Service type('{self.service_type_name}')"


class Purveyors(db.Model):
    __tablename__ = 'Purveyors'
    id = db.Column(db.Integer, primary_key=True)
    contact_info = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Purveyor('{self.contact_info}')"


class StoreHouse(db.Model):
    __tablename__ = 'StoreHouse'
    id = db.Column(db.Integer, primary_key=True)
    typeofservice_id = db.Column(db.Integer, db.ForeignKey('TypesOfService.id'), nullable=False)
    purveyor_id = db.Column(db.Integer, db.ForeignKey('Purveyors.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class Services(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True)
    typeofservice_id = db.Column(db.Integer, db.ForeignKey('TypesOfService.id'), nullable=False)
    service_name = db.Column(db.String(150), nullable=False)


class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)


class Delivery(db.Model):
    __tablename__ = 'Delivery'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)


class OrderStatuses(db.Model):
    __tablename__ = 'OrderStatuses'
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('Delivery.id'), nullable=False)
    status_name = db.Column(db.String(150), nullable=False)


class GeneratedOrders(db.Model):
    __tablename__ = 'GeneratedOrders'
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employees.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('Services.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

