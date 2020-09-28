from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, Order, Discount
from .serializers import (ProductSerializer, OrderSerializer,
                          OrderWithDiscountSerializer, DiscountSerializer)
from .permissions import (OrderCreate, OrderFilter, OrderChangeStatus,
                          GetBill, ACCOUNTANT)

from services.bill_creation import Bill
from datetime import datetime


class ProductViewSet(viewsets.ModelViewSet):
    """Viewset to work with Product model."""
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Viewset to work with Order model.
    Has custom create and list functionality.
    Look permission classes.
    """

    permission_classes = [IsAuthenticated,
                          OrderCreate,
                          OrderFilter,
                          OrderChangeStatus]

    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Return queryset extended with product discount
        data if request.user in Accountant group.
        """
        if self.action == 'list' and \
                self.request.user.groups.filter(name=ACCOUNTANT).exists():
            return OrderWithDiscountSerializer
        return OrderSerializer

    def get_queryset(self):
        """
        Returning queryset by filter parameters.
        """

        queryset = self.queryset
        order_status = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        finish_date = self.request.query_params.get('finish_date')

        if order_status:
            queryset = queryset.filter(status=order_status)
        if start_date:
            start_date = datetime.strptime(start_date, '%d.%m.%Y')
            queryset = queryset.filter(date_of_creation__gte=start_date)
        if finish_date:
            finish_date = datetime.strptime(finish_date, '%d.%m.%Y')
            queryset = queryset.filter(date_of_creation__lte=finish_date)

        return queryset


class DiscountViewSet(viewsets.ModelViewSet):
    """Viewset to work with Discount model."""
    permission_classes = [IsAuthenticated]
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class BillView(RetrieveModelMixin, GenericAPIView):
    """API-endpoint to get Bill for an Order object."""
    permission_classes = [IsAuthenticated, GetBill]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        order_pk = kwargs['order_pk']

        if Order.objects.filter(pk=order_pk).exists():
            order = Order.objects.select_related('product').get(pk=order_pk)
            bill = Bill(order)
            return Response(data=bill.get(), status=status.HTTP_200_OK)
