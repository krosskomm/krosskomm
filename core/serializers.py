from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'accept_terms', 'is_active']

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(self.initial_data.get('password'))
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['id', 'nom']


class TypeInfluenceurSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeInfluenceur
        fields = ['id', 'nom']


class FormeJuridiqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormeJuridique
        fields = "__all__"


class ReseauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseaux
        fields = ['designation', 'classicon']


class ReseauxSociauxSerializer(serializers.ModelSerializer):

    reseau_social = ReseauSerializer(read_only=True, many=False)

    class Meta:
        model = ReseauxSociaux
        exclude = ['influenceur']


class InfluenceurProfilSerializer(serializers.ModelSerializer):
    pays = PaysSerializer(read_only=True, many=True)
    type_influenceur = TypeInfluenceurSerializer(read_only=True, many=True)
    reseaux_sociaux = serializers.SerializerMethodField('get_reseaux')

    def get_reseaux(self, influenceur):
        qs = ReseauxSociaux.objects.filter(influenceur=influenceur, active=True)
        serializer = ReseauxSociauxSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Influenceur
        fields = ['id', 'user', 'compte', 'date_naissance', 'sexe', 'pays', 'type_influenceur', 'reseaux_sociaux']


class EnterpriseProfileSerializer(serializers.ModelSerializer):
    forme_juridique = FormeJuridiqueSerializer(read_only=True, many=False)
    class Meta:
        model = Entreprise
        fields = ['id', 'user', 'compte', 'entite',
                  'denomination_sociale', 'forme_juridique',
                  'numero_entreprise', 'adresse_siege', 'numero', 'code_postale']


class UserInfoSerializer(serializers.ModelSerializer):

    influenceur = InfluenceurProfilSerializer(many=False)
    entreprise = EnterpriseProfileSerializer(many=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_active', 'influenceur', 'entreprise']