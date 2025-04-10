from django.db import models
from django.contrib.auth.models import User # If you need user-specific relations later

class Publication(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    # Add image field if needed: image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"