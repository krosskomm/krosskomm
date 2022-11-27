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


class SecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecteurActivite
        fields = ['id', 'designation']


class ReseauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseaux
        fields = ['designation', 'classicon']


class ReseauxSociauxSerializer(serializers.ModelSerializer):

    reseau_social = ReseauSerializer(read_only=True, many=False)

    class Meta:
        model = ReseauxSociaux
        exclude = ['influenceur']


class ReputationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reputation
        fields = ['id', 'designation']


class InfluenceurProfilSerializer(serializers.ModelSerializer):
    reputation = ReputationSerializer(read_only=True, many=False)
    pays = PaysSerializer(read_only=True, many=True)
    type_influenceur = TypeInfluenceurSerializer(read_only=True, many=True)
    reseaux_sociaux = serializers.SerializerMethodField('get_reseaux')

    @staticmethod
    def get_reseaux(influenceur):
        qs = ReseauxSociaux.objects.filter(influenceur=influenceur, active=True)
        serializer = ReseauxSociauxSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Influenceur
        fields = ['id', 'user', 'compte', 'date_naissance', 'sexe', 'pays',
                  'type_influenceur', 'reseaux_sociaux', 'reputation']

    def create(self, validated_data):
        influenceur = Influenceur.objects.create(**validated_data)
        influenceur.save()
        countries = self.initial_data.get('pays')
        type_influenceurs = self.initial_data.get('type_influenceur')
        if len(countries) > 0:
            for pays_id in countries:
                try:
                    pays = Pays.objects.get(pk=int(pays_id))
                except Pays.DoesNotExist:
                    pays = None
                if pays is not None:
                    influenceur.pays.add(pays)
        if len(type_influenceurs) > 0:
            for type_id in type_influenceurs:
                try:
                    type_influenceur = TypeInfluenceur.objects.get(pk=int(type_id))
                except TypeInfluenceur.DoesNotExist:
                    type_influenceur = None
                if type_influenceur is not None:
                    influenceur.type_influenceur.add(type_influenceur)
        return influenceur
        pass

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        reseaux_sociaux = self.initial_data.get('reseaux_sociaux')
        reputation = self.initial_data.get('reputation', None)
        countries = self.initial_data.get('pays')
        type_influenceurs = self.initial_data.get('type_influenceur')
        if len(countries) > 0:
            instance.pays.clear()
            for pays_id in countries:
                try:
                    pays = Pays.objects.get(pk=int(pays_id))
                except Pays.DoesNotExist:
                    pays = None
                if pays is not None:
                    instance.pays.add(pays)
        if len(type_influenceurs) > 0:
            instance.type_influenceur.clear()
            for type_id in type_influenceurs:
                try:
                    type_influenceur = TypeInfluenceur.objects.get(pk=int(type_id))
                except TypeInfluenceur.DoesNotExist:
                    type_influenceur = None
                if type_influenceur is not None:
                    instance.type_influenceur.add(type_influenceur)
        if len(reseaux_sociaux) > 0:
            ReseauxSociaux.objects.filter(influenceur=instance).delete()
            for reseaux in reseaux_sociaux:
                try:
                    reseau = Reseaux.objects.get(pk=int(reseaux['reseau']))
                except Reseaux.DoesNotExist:
                    reseau = None
                if reseau is not None:
                    ReseauxSociaux.objects.create(influenceur=instance, reseau_social=reseau, lien_url=reseaux['lien'])

        if reputation is not None:
            try:
                reput = Reputation.objects.get(pk=int(reputation))
            except Reputation.DoesNotExist:
                reput = None
            if reput is not None:
                instance.reputation = reput
                instance.save()
        return instance


class EnterpriseProfileSerializer(serializers.ModelSerializer):
    forme_juridique = FormeJuridiqueSerializer(read_only=True, many=False)
    secteur_activite = SecteurSerializer(read_only=True, many=True)
    pays = PaysSerializer(read_only=True, many=True)

    class Meta:
        model = Entreprise
        fields = ['id', 'user', 'compte', 'entite',
                  'denomination_sociale', 'forme_juridique',
                  'numero_entreprise', 'adresse_siege', 'numero', 'code_postale', 'pays', 'secteur_activite']

    def create(self, validated_data):
        entreprise = Entreprise.objects.create(**validated_data)
        entreprise.save()
        secteurs = self.initial_data.get('secteur_activite')
        countries = self.initial_data.get('pays')
        if len(countries) > 0:
            for pays_id in countries:
                try:
                    pays = Pays.objects.get(pk=int(pays_id))
                except Pays.DoesNotExist:
                    pays = None
                if pays is not None:
                    entreprise.pays.add(pays)
        if len(secteurs) > 0:
            for secteur in secteurs:
                try:
                    secteur_act = SecteurActivite.objects.get(pk=int(secteur))
                except SecteurActivite.DoesNotExist:
                    secteur_act = None
                if secteur_act is not None:
                    entreprise.secteur_activite.add(secteur_act)
        return entreprise

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        secteurs = self.initial_data.get('secteur_activite')
        countries = self.initial_data.get('pays')
        if len(countries) > 0:
            instance.pays.clear()
            for pays_id in countries:
                try:
                    pays = Pays.objects.get(pk=int(pays_id))
                except Pays.DoesNotExist:
                    pays = None
                if pays is not None:
                    instance.pays.add(pays)
        if len(secteurs) > 0:
            instance.secteur_activite.clear()
            for secteur in secteurs:
                try:
                    secteur_act = SecteurActivite.objects.get(pk=int(secteur))
                except SecteurActivite.DoesNotExist:
                    secteur_act = None
                if secteur_act is not None:
                    instance.secteur_activite.add(secteur_act)
        return instance



class UserInfoSerializer(serializers.ModelSerializer):

    influenceur = InfluenceurProfilSerializer(many=False)
    entreprise = EnterpriseProfileSerializer(many=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_active', 'influenceur', 'entreprise']
