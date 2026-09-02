from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Mechanic, ServiceRequest


class MechanicAPITest(APITestCase):

    def setUp(self):
        self.mechanic = Mechanic.objects.create(
            name="Test Mechanic",
            phone="9876543210",
            location="Indore",
            rating=4.5,
            is_open=True,
            services=["Oil Change", "Brake Repair"]
        )

    def test_get_mechanics(self):
        response = self.client.get("/api/mechanics/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_location(self):
        response = self.client.get("/api/mechanics/?location=Indore")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_open_status(self):
        response = self.client.get("/api/mechanics/?is_open=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_sort_by_rating(self):
        response = self.client.get("/api/mechanics/?sort=rating")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["rating"], "4.5")


class ServiceRequestTest(APITestCase):

    def setUp(self):
        self.mechanic = Mechanic.objects.create(
            name="Test Mechanic",
            phone="9876543210",
            location="Indore",
            rating=4.5,
            is_open=True,
            services=["Oil Change", "Brake Repair"]
        )

    def test_create_service_request(self):
        data = {
            "customer_name": "Test Customer",
            "customer_phone": "9123456789",
            "vehicle_number": "MP09AB1234",
            "mechanic_id": self.mechanic.id,
            "service": "Oil Change",
            "problem_description": "Engine making noise."
        }

        response = self.client.post(
            "/api/service-requests/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "PENDING")

    def test_invalid_phone(self):
        data = {
            "customer_name": "Test Customer",
            "customer_phone": "12345",
            "vehicle_number": "MP09AB1234",
            "mechanic_id": self.mechanic.id,
            "service": "Oil Change",
            "problem_description": "Engine problem."
        }

        response = self.client.post(
            "/api/service-requests/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_invalid_mechanic_id(self):
        data = {
            "customer_name": "Test Customer",
            "customer_phone": "9123456789",
            "vehicle_number": "MP09AB1234",
            "mechanic_id": 9999,
            "service": "Oil Change",
            "problem_description": "Engine problem."
        }

        response = self.client.post(
            "/api/service-requests/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )