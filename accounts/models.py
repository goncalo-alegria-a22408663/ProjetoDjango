from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    token = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Profile de {self.user.username}"