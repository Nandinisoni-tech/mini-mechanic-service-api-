from rest_framework import serializers
from .models import Mechanic, ServiceRequest
import re


class MechanicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mechanic
        fields = '__all__'

    def validate_phone(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 0 and 5."
            )
        return value


class ServiceRequestSerializer(serializers.ModelSerializer):

    mechanic_id = serializers.PrimaryKeyRelatedField(
        source='mechanic',
        queryset=Mechanic.objects.all()
    )

    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'customer_name',
            'customer_phone',
            'vehicle_number',
            'mechanic_id',
            'service',
            'problem_description',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_customer_phone(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError(
                "Customer phone number must contain exactly 10 digits."
            )
        return value

    def validate_vehicle_number(self, value):
        pattern = r'^[A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{4}$'

        if not re.fullmatch(pattern, value.upper()):
            raise serializers.ValidationError(
                "Enter a valid vehicle number, e.g. MP09AB1234."
            )

        return value.upper()

    def validate(self, data):
        mechanic = data.get('mechanic')
        service = data.get('service')

        if mechanic and service:
            if service not in mechanic.services:
                raise serializers.ValidationError({
                    'service': 'This service is not offered by the selected mechanic.'
                })

        return data