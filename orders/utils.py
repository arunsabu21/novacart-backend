from datetime import timedelta

def get_estimated_delivery(order_date):
    return order_date + timedelta(days=5)