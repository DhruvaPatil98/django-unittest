from rest_framework import serializers

from apps.core.serializer import BaseSerializer


class IDSerializer(BaseSerializer):
    id = serializers.UUIDField(required=True)
