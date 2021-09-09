from django.db import models

# Create your models here.
class Restaurant(models.Model):
    restaurantName = models.CharField(max_length=50)
    restaurantType = models.CharField(max_length=100)
    
    def __str__(self):
        return self.restaurantName