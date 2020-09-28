from django.contrib import admin
from .models import Product, Order, Discount


# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Discount)
