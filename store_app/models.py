from django.db import models
from django.utils import timezone


class Product(models.Model):
    """
    Model to represent Product instance.
    """

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    date_of_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}: {str(self.price)}'


class Order(models.Model):
    """
    Model to represent Order instance.
    """

    WAITING = 1
    DONE = 2
    PAID = 3

    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (DONE, 'Done'),
        (PAID, 'Paid'),
    )

    product = models.ForeignKey(Product, related_name='orders', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=WAITING)
    date_of_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{str(self.pk)}: {self.status}'


class Discount(models.Model):
    """
    Model to represent Discount instance.
    """

    title = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    product = models.ManyToManyField(Product, through='ProductDiscount')

    def __str__(self):
        return f'{self.title}: {str(self.size)}'


class ProductDiscount(models.Model):
    """
    Additional model to create Product-Discount M2M relation.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
