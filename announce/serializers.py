from .models import *
from django.db import transaction
from rest_framework import serializers
from core.serializers import UserInfoSerializer, UserSerializer
from core.models import Entreprise


class AuteurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Entreprise
        exclude = ['pays', 'secteur_activite', 'forme_juridique', 'badge', 'compte']


class AnnounceSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True, many=False)

    class Meta:
        model = Announce
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        return Announce.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class SolicitationSerializer(serializers.ModelSerializer):

    user = UserInfoSerializer(read_only=True, many=False)

    class Meta:
        model = Solicitation
        fields = ['user', 'date_solicitation']


class AnnounceDetailSerializer(serializers.ModelSerializer):

    Solicitations = serializers.SerializerMethodField('get_solicitations')

    class Meta:
        model = Announce
        fields = '__all__'

    @staticmethod
    def get_solicitations(announce):
        qs = Solicitation.objects.filter(announce=announce)
        serializer = SolicitationSerializer(instance=qs, many=True)
        return serializer.data