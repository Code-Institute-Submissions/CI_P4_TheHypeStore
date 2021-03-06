from django.db import models
from pyuploadcare.dj.models import ImageField

# Create your models here.
class Product(models.Model):
    name = models.CharField(blank=False, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, blank=True)
    image = ImageField(blank=True, manual_crop="")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return self.category_name

