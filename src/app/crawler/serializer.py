from rest_framework import serializers


class ProductLoadRequestSerializer(serializers.Serializer):
    bucket_name = serializers.CharField(max_length=255)
    object_name = serializers.CharField(max_length=255)
