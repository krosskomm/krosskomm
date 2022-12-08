from .models import *
from rest_framework import serializers
from announce.serializers import AnnounceSerializer
from core.serializers import InfluenceurSerializer


class ContratSerializer(serializers.ModelSerializer):
    announce = AnnounceSerializer(read_only=True, many=False)
    destinataires = InfluenceurSerializer(read_only=True, many=True)

    class Meta:
        model = Contrat
        fields = '__all__'

    def create(self, validated_data):
        return Contrat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance
