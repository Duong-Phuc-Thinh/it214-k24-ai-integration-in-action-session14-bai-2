import time
from datetime import datetime, timedelta

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.status = "PENDING"
        self.updated_at = datetime.now()

class OrderRepository:
    def __init__(self):
        self.orders = {}

    def save(self, order):
        order.updated_at = datetime.now()
        self.orders[order.order_id] = order

    def find_by_id(self, order_id):
        return self.orders.get(order_id)

    def find_pending_orders_older_than(self, minutes):
        threshold = datetime.now() - timedelta(minutes=minutes)
        return [order for order in self.orders.values() if order.status == "PENDING" and order.updated_at < threshold]

class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def handle_payment_response(self, event):
        order = self.repository.find_by_id(event['order_id'])
        if not order:
            print(f"Order {event['order_id']} not found!")
            return

        status = event.get('status')
        if status == "SUCCESS":
            order.status = "PAID"
            print(f"Order {order.order_id} status updated to PAID")
        elif status in ["REJECTED", "FAILED"]:
            order.status = "CANCELED" if status == "REJECTED" else "FAILED"
            print(f"Order {order.order_id} status updated to {order.status}")
        else:
            order.status = "UNKNOWN"
            print(f"Order {order.order_id} status updated to UNKNOWN")

        self.repository.save(order)

    def check_timeout_orders(self, timeout_minutes=5):
        pending_orders = self.repository.find_pending_orders_older_than(timeout_minutes)
        for order in pending_orders:
            order.status = "FAILED"
            self.repository.save(order)
            print(f"[Timeout Job] Order {order.order_id} timed out and marked as FAILED")

if __name__ == "__main__":
    repo = OrderRepository()
    service = OrderService(repo)

    # Tao don hang moi
    order1 = Order("ORD123")
    repo.save(order1)
    print(f"Created order {order1.order_id} with status {order1.status}")

    # Gia lap nhan su kien thanh toan thanh cong
    event = {"order_id": "ORD123", "status": "SUCCESS"}
    service.handle_payment_response(event)

    # Tao don hang bi lac loi (pending qua han)
    order2 = Order(
        "ORD999"
    )
    order2.updated_at = datetime.now() - timedelta(minutes=10)
    repo.save(order2)
    print(f"Created expired pending order {order2.order_id}")

    # Chay job kiem tra timeout
    service.check_timeout_orders(timeout_minutes=5)
