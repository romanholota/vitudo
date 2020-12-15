from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class UserDetails(models.Model):
	user = models.OneToOneField(User, related_name='details', on_delete=models.CASCADE)
	account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
	is_manager = models.BooleanField(default=False)
	dark_mode = models.BooleanField(default=False)
