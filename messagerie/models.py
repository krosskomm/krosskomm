from django.db import models
from django.conf import settings


# Create your models here.

class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(null=True, blank=True)
    date_notification = models.DateTimeField(auto_now_add=True)
    id_chat = models.IntegerField(default=0)
    type_notif = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=True)
    version = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return  str(self.sender.email) + ' ' + str(self.receiver.email)
