import os

import matplotlib.pyplot as plt
from app.models import *

from sqlalchemy import func


def create_service_rating_chart():
    service_counts = db.session.query(Services.service_name, func.count(Orders.service_id))\
        .join(Orders, Services.id == Orders.service_id)\
        .group_by(Services.service_name)\
        .order_by(func.count(Orders.service_id))\
        .all()

    service_names = [service[0] for service in service_counts]
    service_frequencies = [service[1] for service in service_counts]

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.barh(service_names, service_frequencies, color='skyblue')
    plt.xlabel('Количество заказов')
    plt.ylabel('Услуга')
    plt.title('Частота использования услуг')
    plt.grid(True)

    # Сохранение графика
    img_path = os.path.join('app', 'static', 'img', 'service_frequency.png')
    plt.savefig(img_path)
    plt.close()


def generate_employee_statistics_chart(start_date, end_date):
    # Запрос данных из базы данных
    employee_counts = db.session.query(Employees.full_name, func.count(Orders.id))\
        .join(Orders, Employees.id == Orders.employee_id)\
        .filter(Orders.order_date >= start_date, Orders.order_date <= end_date)\
        .group_by(Employees.full_name)\
        .order_by(func.count(Orders.id).desc())\
        .all()

    employee_names = [employee[0] for employee in employee_counts]
    order_counts = [employee[1] for employee in employee_counts]
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.bar(employee_names, order_counts, color='skyblue')
    plt.xlabel('Сотрудник')
    plt.ylabel('Количество заказов')
    plt.title(f"Количество заказов по сотрудникам\nс {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Сохранение графика
    img_path = os.path.join('app', 'static', 'img', 'employee_statistics.png')
    plt.savefig(img_path)
    plt.close()

    return img_path
