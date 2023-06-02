from django.db import models

class Dialog(models.Model):
    username = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    context = models.TextField()

    def __str__(self):
        return self.username

class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.content
# Create your models here.
