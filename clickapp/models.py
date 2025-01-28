# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Click(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.count}"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    button_text = models.CharField(max_length=100, default='Click Me!')

    def __str__(self):
        return self.user.username

