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
        pass