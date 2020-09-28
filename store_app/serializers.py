from rest_framework import serializers
from .models import Product, Order, Discount


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class to convert Product instances.
    """

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'date_of_creation']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class to convert Order instances.
    """

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'product', 'status', 'date_of_creation']


class OrderWithDiscountSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class to convert Order instances.
    Extended with info about product discounts -
    accountant functionality.
    """

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    discounts = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'status', 'date_of_creation', 'discounts']

    def get_discounts(self, obj):
        """
        returns product discount info
        """
        discounts_set = Discount.objects.filter(product=obj.product)
        discounts = {discount.title: discount.size for discount in discounts_set}
        return discounts


class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class to convert Discount instances.
    """

    product = serializers.HyperlinkedIdentityField(many=True, view_name='discount-detail', read_only=True)

    class Meta:
        model = Discount
        fields = ['id', 'title', 'size', 'product']


