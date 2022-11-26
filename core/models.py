from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from utils.manager import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    accept_terms = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.pk) + ' : ' + str(self.email)


class Pays(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length = 10, null=True, blank=True)

    def __str__(self):
        return self.nom


class Profil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    compte = models.CharField(max_length=25, null=False)
    pays = models.ManyToManyField(Pays)

    class Meta:
        abstract = True


class SecteurActivite(models.Model):
    designation = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.designation


class FormeJuridique(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nom

class Entreprise(Profil):
    entite = models.CharField(max_length=200)
    denomination_sociale = models.CharField(max_length=200)
    forme_juridique = models.ForeignKey(FormeJuridique, on_delete=models.CASCADE)
    numero_entreprise = models.CharField(max_length=100, null=True)
    secteur_activite = models.ManyToManyField(SecteurActivite)
    adresse_siege = models.TextField(null=True)
    numero = models.CharField(max_length=100, null=True)
    code_postale = models.CharField(max_length=250, null=True)
    ville = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.denomination_sociale


class TypeInfluenceur(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nom


class Reseaux(models.Model):
    designation = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    classicon = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.designation


class Reputation(models.Model):
    designation = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.designation


class Influenceur(Profil):
    date_naissance = models.DateField(null=False)
    sexe = models.CharField(max_length=25, null=False)
    type_influenceur = models.ManyToManyField(TypeInfluenceur)
    reputation = models.ForeignKey(Reputation, on_delete=models.DO_NOTHING, null=True, blank=True)
    reseaux_sociaux = models.ManyToManyField(Reseaux, through="ReseauxSociaux", related_name="reseauxsociaux")

    def __str__(self):
        return str(self.user.email)


class ReseauxSociaux(models.Model):
    influenceur = models.ForeignKey(Influenceur, on_delete=models.CASCADE)
    reseau_social = models.ForeignKey(Reseaux, on_delete=models.CASCADE, related_name='reseau_social')
    lien_url = models.URLField(max_length=255, null=True, blank=True)
    followers = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)
