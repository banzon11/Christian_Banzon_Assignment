from django.db import models

# Create your models here.

class What(models.Model):
    userId=models.IntegerField(default=1)
    title=models.CharField(default="Default Title", max_length= 200)
    body=models.TextField(default="Body of post goes here")
