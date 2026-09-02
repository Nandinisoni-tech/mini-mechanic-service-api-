import logging

from rest_framework import viewsets
from .models import Mechanic, ServiceRequest
from .serializers import MechanicSerializer, ServiceRequestSerializer


logger = logging.getLogger(__name__)


class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

    def get_queryset(self):
        queryset = Mechanic.objects.all()

        location = self.request.query_params.get('location')
        is_open = self.request.query_params.get('is_open')
        sort = self.request.query_params.get('sort')

        if location:
            logger.info("Filtering mechanics by location: %s", location)
            queryset = queryset.filter(location__icontains=location)

        if is_open is not None:
            logger.info("Filtering mechanics by open status: %s", is_open)
            queryset = queryset.filter(is_open=is_open.lower() == 'true')

        if sort == 'rating':
            logger.info("Sorting mechanics by highest rating")
            queryset = queryset.order_by('-rating')

        elif sort == '-rating':
            logger.info("Sorting mechanics by lowest rating")
            queryset = queryset.order_by('rating')

        return queryset

    def perform_create(self, serializer):
        mechanic = serializer.save()
        logger.info(
            "Mechanic created successfully: ID=%s, name=%s",
            mechanic.id,
            mechanic.name
        )

    def perform_update(self, serializer):
        mechanic = serializer.save()
        logger.info(
            "Mechanic updated successfully: ID=%s, name=%s",
            mechanic.id,
            mechanic.name
        )

    def perform_destroy(self, instance):
        logger.info(
            "Mechanic deleted: ID=%s, name=%s",
            instance.id,
            instance.name
        )
        instance.delete()


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def perform_create(self, serializer):
        service_request = serializer.save()
        logger.info(
            "Service request created: ID=%s, customer=%s, mechanic_id=%s",
            service_request.id,
            service_request.customer_name,
            service_request.mechanic_id
        )

    def perform_update(self, serializer):
        service_request = serializer.save()
        logger.info(
            "Service request updated: ID=%s, status=%s",
            service_request.id,
            service_request.status
        )

    def perform_destroy(self, instance):
        logger.info(
            "Service request deleted: ID=%s",
            instance.id
        )
        instance.delete()