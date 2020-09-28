from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'discount', views.DiscountViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('bill/<int:order_pk>/', views.BillView.as_view(), name='bill_detail'),
]
