from django.db import models

class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField(max_length=1000)
    description_long = models.TextField(max_length=5000)
    lng = models.DecimalField(max_digits=20, decimal_places=16)
    lat = models.DecimalField(max_digits=20, decimal_places=16)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
