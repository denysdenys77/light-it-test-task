from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product, Order
import base64


class CashierFlowTests(TestCase):
    """
    Test class for chacking Cashier functionality.
    """

    def setUp(self):

        self.product = Product.objects.create(name='TV', price=1000)

        self.group = Group(name="Cashier")
        self.group.save()

        self.client = APIClient()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + base64.b64encode(b'test:test').decode("ascii")

        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def tearDown(self):
        Order.objects.all().delete()
        self.user.delete()
        self.group.delete()
        self.product.delete()

    def test_create_order(self):
        """only cashier can create an order"""

        response = self.client.post("/order/", {'product': 1})
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.post("/order/", {'product': 1})
        self.assertEqual(response.status_code, 201)

    def test_list_of_done_orders(self):
        """only cashier can view list of done orders"""

        response = self.client.get("/order/", {'status': 2})
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.get("/order/", {'status': 2})
        self.assertEqual(response.status_code, 200)

    def test_set_paid_order_status(self):
        """only cashier can set order status to 'paid'"""

        Order.objects.create(product=self.product)

        response = self.client.patch("/order/1/", {'status': 3})
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.patch("/order/1/", {'status': 3})
        self.assertEqual(response.status_code, 200)

    def test_get_order_bill(self):
        """only cashier can get order bill"""

        Order.objects.create(product=self.product)

        response = self.client.get("/bill/1/")
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.get("/bill/1/")
        self.assertEqual(response.status_code, 200)


class ConsultantFlowTests(TestCase):
    """
    Test class for chacking Consultant functionality.
    """

    def setUp(self):

        self.product = Product.objects.create(name='TV', price=1000)
        self.order = Order.objects.create(product=self.product)

        self.group = Group(name="Consultant")
        self.group.save()

        self.client = APIClient()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + base64.b64encode(b'test:test').decode("ascii")

        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def tearDown(self):
        Order.objects.all().delete()
        self.user.delete()
        self.group.delete()
        self.product.delete()

    def test_get_waiting_orders_list(self):
        """only consultant can view list of waiting orders"""

        response = self.client.get("/order/", {'status': 1})
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.get("/order/", {'status': 1})
        self.assertEqual(response.status_code, 200)

    def test_set_done_order_status(self):
        """only consultant can set order status to 'done'"""

        response = self.client.patch("/order/1/", {'status': 2})
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.patch("/order/1/", {'status': 2})
        self.assertEqual(response.status_code, 200)


class AccountantFlowTests(TestCase):
    """
    Test class for Accountant Consultant functionality.
    """

    def setUp(self):
        self.product = Product.objects.create(name='TV', price=1000)
        self.order = Order.objects.create(product=self.product)

        self.group = Group(name="Accountant")
        self.group.save()

        self.client = APIClient()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + base64.b64encode(b'test:test').decode("ascii")

        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def tearDown(self):
        Order.objects.all().delete()
        self.user.delete()
        self.group.delete()
        self.product.delete()

    def test_get_orders_list_by_date_filter(self):
        """only accountant can view list of orders filtered by date"""

        response = self.client.get("/order/", {'start_date': '01.01.2019',
                                               'finish_date': '24.12.2020'})
        self.assertEqual(response.status_code, 403)

        self.user.groups.add(self.group)
        self.user.save()

        response = self.client.get("/order/", {'start_date': '01.01.2019',
                                               'finish_date': '24.12.2020'})
        self.assertEqual(response.status_code, 200)
