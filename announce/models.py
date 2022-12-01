from django.db import models
from django.conf import settings
from core.models import (
    Entreprise,
    Pays, TypeInfluenceur,
    Reseaux, Reputation
    )

# Create your models here.
class ProfilAnnonce(models.Model):
    pays = models.ManyToManyField(Pays)
    type_influenceur = models.ManyToManyField(TypeInfluenceur)
    reseaux = models.ManyToManyField(Reseaux)
    reputation = models.ManyToManyField(Reputation)


class Announce(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(null=True)
    auteur = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="announces", null=True, blank=True)
    profil_recherche = models.OneToOneField(ProfilAnnonce, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    Solicitations = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Solicitation",
                                           related_name="solicitations")
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.titre


class Solicitation(models.Model):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_solicitation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.email) + ' : ' + str(self.announce.titre)
