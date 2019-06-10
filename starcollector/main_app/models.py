from django.db import models

# Create your models here.


class Star(models.Model):
    name = models.CharField(max_length=100)
    type_of_star = models.CharField(max_length=100)
    distance = models.FloatField()
    mass = models.FloatField()

    def __str__(self):
        return self.name