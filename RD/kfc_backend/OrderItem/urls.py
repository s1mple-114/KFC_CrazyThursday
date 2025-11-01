from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import orderitemViewSet

router = DefaultRouter()
router.register(r'order-items', orderitemViewSet,basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]