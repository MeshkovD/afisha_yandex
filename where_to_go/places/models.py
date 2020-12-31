from django.db import models

class Place(models.Model):
    title = models.CharField(
        max_length=200
    )
    description_short = models.TextField(
        max_length=1000
    )
    description_long = models.TextField(
        max_length=5000
    )
    lng = models.DecimalField(
        max_digits=17,
        decimal_places=13
    )
    lat = models.DecimalField(
        max_digits=17,
        decimal_places=13
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Photo(models.Model):
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Иллюстрация к месту'
    )
    place = models.ForeignKey(
        Place,
        default=0,
        on_delete=models.CASCADE,
        verbose_name='Место'
    )
    order = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name='Порядок показа'
    )

    def __str__(self):
        place = self.place.title
        ordering_number = self.order
        return f"{ordering_number} Photo of - {place}"

    class Meta:
        ordering = ['order']
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"