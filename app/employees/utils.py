from datetime import datetime, date

from flask import session

from app.models import *


class OrderInfo:

    def __init__(self, order_info: dict):
        self.client_id = order_info["clientId"]
        self.service_id = order_info["serviceId"]
        self.status_id = order_info["statusId"]
        self.delivery_date = datetime.strptime(order_info["deliveryDate"], "%Y-%m-%d").date() if order_info["deliveryDate"] else None
        self.objects = [ObjectInfo(object_inf) for object_inf in order_info["objects"]]

    def __str__(self):
        objects_str = '\n'.join(list(map(str, self.objects)))
        return f"OrderInfo(client: {self.client_id}, service: {self.service_id}, delivery: {self.delivery_date})\n{objects_str}"

class ObjectInfo:

    def __init__(self, object_dict: dict):
        try:
            self.amount = int(object_dict["objectAmount"])
        except:
            raise Exception("Количество товара должно быть целым числом!")
        if not object_dict["objectId"]:
            raise Exception("Необходимо выбора тип услуги!")
        self.id = object_dict["objectId"]
        self.cats = object_dict["objectCategories"]
        self.subcats = object_dict["objectSubCategories"]

    def __str__(self):
        return f"Object(id: {self.id}, amount: {self.amount}, cats: {self.cats}, subcats: {self.subcats})"
    

class ResponseToJS:

    def __init__(self, message: str = None, status: str = None, data = None, url = None):
        self.message = message
        self.status = status
        self.data = data
        self.url = url


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