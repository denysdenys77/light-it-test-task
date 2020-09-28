import datetime
from store_project.celery_app import app
from .models import Product, Discount, ProductDiscount
from django.utils import timezone


@app.task(name="store_project.tasks.add_discounts")
def add_discounts():
    """
    Celery task to check and edit product discounts regulary.
    """

    products = Product.objects.all()

    now = timezone.localtime()
    thirty_day_period = datetime.timedelta(days=30)

    for product in products:
        period = now - product.date_of_creation
        if period > thirty_day_period:
            thirty_day_period_discount = Discount.objects.filter(
                title='older than 30 days').last()
            ProductDiscount.objects.get_or_create(
                product=product,
                discount=thirty_day_period_discount)
