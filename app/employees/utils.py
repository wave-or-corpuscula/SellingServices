from datetime import datetime


class OrderInfo:

    def __init__(self, order_info: dict):
        self.client_id = order_info["clientId"]
        self.service_id = order_info["serviceId"]
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

    def __init__(self, message: str, status: str, data = None, url = None):
        self.message = message
        self.status = status
        self.data = data
        self.url = url
