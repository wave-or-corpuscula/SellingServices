from app.models import *


def get_order_total_cost(order_id: int):
    order = Orders.query.get(order_id)
    order_cost = order.service.cost
    ordered_objs = OrderedObjects.query.filter_by(order_id=order.id)
    for ordered_obj in ordered_objs:
        object_cost = ordered_obj.object.cost
        amount = ordered_obj.count
        ord_objs_cats = OrderedObjectCategories.query.filter_by(order_id=order.id, object_id=ordered_obj.object_id)
        for ord_obj_cats in ord_objs_cats:
            if ord_obj_cats.subcategory:
                object_cost += ord_obj_cats.subcategory.cost
        order_cost += object_cost * amount
    return order_cost
