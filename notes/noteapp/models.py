from django.db import models

class UserModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

class Notes(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    time = models.DateTimeField()