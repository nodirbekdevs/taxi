from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, DriverViewSet, OrderViewSet, LocationViewSet, UserViewSet, VehicleViewSet


router = DefaultRouter()
router.register('client', ClientViewSet, basename='client')
router.register('driver', DriverViewSet, basename='driver')
router.register('order', OrderViewSet, basename='ride')
router.register('location', LocationViewSet, basename='location')
router.register('user', UserViewSet, basename='user')
router.register('vehicle', VehicleViewSet, basename='vehicle')
