from .models import Notification
from rest_framework import serializers
from core.serializers import UserInfoSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer(read_only=True, many=False)
    receiver = UserInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Notification
        fields = '__all__'

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)
