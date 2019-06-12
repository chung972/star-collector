from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
VISIBILITY = (
    ('C', 'Clear'),
    ('P', 'Partial'),
    ('O', 'Obscured')
)


class Star(models.Model):
    name = models.CharField(max_length=100)
    type_of_star = models.CharField(max_length=100)
    distance = models.FloatField()
    mass = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'star_id': self.id})


class Observatory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('observatories_detail', kwargs={'pk': self.id})


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
