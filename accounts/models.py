from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
	user = models.OneToOneField(User, related_name='details', on_delete=models.CASCADE)
	dark_mode = models.BooleanField(default=False)
