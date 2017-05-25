from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.
class SessionWithDate(models.Model):
	"""
	Model to save the client date and the current session.
	"""
	sess = models.ForeignKey(Session)
	date = models.TextField(max_length=10, default="")