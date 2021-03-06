from django.core.files.base import ContentFile
from django.db import models
from tinymce import models as tinymce_models


class Place(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    short_description = models.TextField(
        verbose_name='Короткое описание',
        blank=True
    )

    long_description = tinymce_models.HTMLField(
        verbose_name='Полное описание',
        blank=True
    )

    lng = models.DecimalField(
        max_digits=17,
        decimal_places=15,
        verbose_name='Широта'
    )
    lat = models.DecimalField(
        max_digits=17,
        decimal_places=15,
        verbose_name='Долгота'
    )

    def add_photo(self, img_response, place):
        filename = img_response.url.split('/')[-1]
        new_photo = Photo(place=place)
        new_photo.image.save(filename,
                             ContentFile(img_response.content),
                             save=True)

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
        related_name='photos',
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
