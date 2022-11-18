from django.db import models


# Create your models here.
class Document(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return self.name
