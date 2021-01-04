from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
import requests

from places.models import Place, Photo


def get_name(image_url):
    '''Генерирует имя картинки по переданному url'''
    return image_url.split('/')[-1]


def add_photo_to_place_model(response):
    for photo_link in response.json()['imgs']:
        try:
            img_response = requests.get(photo_link)
            img_response.raise_for_status()
            filename = get_name(img_response.url)
            place_obj, created = Place.objects.get_or_create(
                title=response.json()['title'])
            new_photo = Photo(place=place_obj)
            new_photo.image.save(filename,
                                 ContentFile(img_response.content),
                                 save=True)

        except requests.exceptions.HTTPError:
            raise CommandError('Ссылка на картинку в переданном JSON'
            'может содержать ошибку, проверьте отправленную команду!')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_url')

    def handle(self, *args, **options):
        json_url = f'{options["json_url"]}'

        try:
            response = requests.get(json_url)
            response.raise_for_status()

            place, created = Place.objects.get_or_create(
                title=response.json()['title'],
                description_short=response.json()['description_short'],
                description_long=response.json()['description_long'],
                lng=response.json()['coordinates']['lng'],
                lat=response.json()['coordinates']['lat'],
            )

            if created:
                add_photo_to_place_model(response)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully add place {response.json()["title"]}'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Not added. A place named '
                    f'{response.json()["title"]} already exists'))

        except requests.exceptions.HTTPError:
            raise CommandError('Страница с JSON не найдена, '
                               'проверьте отправленную команду!')
