from typing import Any

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from order.models import Order, OrderImages


class OrderImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImages
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        file_fields = kwargs.pop("file_fields", None)
        super().__init__(*args, **kwargs)
        if file_fields:
            field_update_dict = {
                field: serializers.ImageField(required=False, write_only=True)
                for field in file_fields
            }
            self.fields.update(**field_update_dict)

    def create(self, validated_data):
        validated_data_copy = validated_data.copy()
        validated_files = []
        for key, value in validated_data_copy.items():
            if isinstance(value, InMemoryUploadedFile):
                validated_files.append(value)
                validated_data.pop(key)
        order_instance = super().create(validated_data)
        for file in validated_files:
            OrderImages.objects.create(order=order_instance, file=file)
        return order_instance

    class Meta:
        model = Order
        # fields = "__all__"
        exclude = ["jobs"]
