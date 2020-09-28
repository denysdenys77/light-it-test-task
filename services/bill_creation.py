from django.utils import timezone
from store_app.models import Discount


class Bill:
    """
    A class for creating an Bill object.
    """

    def __init__(self, order):
        self.order = order

    def get(self):
        """
        Getting all data about order and product.
        """

        bill = {
            'product': {
                'name': self.order.product.name,
                'price': self.order.product.price
            },
            'order_date_of_creation': self.order.date_of_creation,
            'bill_date_of_creation': timezone.now(),
            'discounts': [],
            'total': self.order.product.price
        }

        return self.add_discount(bill)

    def add_discount(self, bill):
        """
        Adding data about product discounts to a bill dictionary.
        """

        discounts_queryset = Discount.objects.prefetch_related('product')

        total_discount = 0

        for discount in discounts_queryset:
            discount_products = discount.product.all()
            if self.order.product in discount_products:
                bill['discounts'].append({'discount_title': discount.title,
                                          'discount_size': discount.size})

                total_discount += discount.size
                if total_discount > 100:
                    total_discount = 100

            bill['total'] = bill['total'] - bill['total'] / 100 * total_discount

        return bill
