from rest_framework.routers import DefaultRouter
from .views import MechanicViewSet, ServiceRequestViewSet

router = DefaultRouter()

router.register('mechanics', MechanicViewSet)
router.register('service-requests', ServiceRequestViewSet)

urlpatterns = router.urls