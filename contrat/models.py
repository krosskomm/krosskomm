from django.db import models
from core.models import (
    Influenceur
)
from announce.models import Announce


# Create your models here.
class Contrat(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField()
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)
    destinataires = models.ManyToManyField(Influenceur)
    document = models.FileField(upload_to="contrat", null=True, blank=True)
    send_notification = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + ' ' + str(self.announce.titre)
