from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
VISIBILITY = (
    ('C', 'Clear'),
    ('P', 'Partial'),
    ('O', 'Obscured')
)


class Observatory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('observatories_detail', kwargs={'pk': self.id})


class Star(models.Model):
    name = models.CharField(max_length=100)
    type_of_star = models.CharField(max_length=100)
    distance = models.FloatField()
    mass = models.FloatField()
    observatories = models.ManyToManyField(Observatory)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'star_id': self.id})


class Viewing(models.Model):
    date = models.DateField("Viewing date")
    time = models.TimeField(
        blank=True,
        null=True
    )
    visibility = models.CharField(
        max_length=1,
        choices=VISIBILITY,
        default=VISIBILITY[0][0]
    )

    star = models.ForeignKey(Star, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_visibility_display()} on {self.date} at {self.time}"
    
    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    star = models.ForeignKey(Star, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for star_id: {self.star_id}@{self.url}"