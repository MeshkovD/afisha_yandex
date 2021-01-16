from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
import requests
from django.db.models import Q

from places.models import Place, Photo


def get_name(image_url):
    '''Генерирует имя картинки по переданному url'''
    return image_url.split('/')[-1]

def add_photo_to_place_model(response, place):
    json_response = response.json()
    for photo_link in json_response['imgs']:
        try:
            img_response = requests.get(photo_link)
            img_response.raise_for_status()
            filename = get_name(img_response.url)
            new_photo = Photo(place=place)
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
        json_url = options["json_url"]

        try:
            response = requests.get(json_url)
            response.raise_for_status()
            json_response = response.json()
            place, created = Place.objects.get_or_create(
                title=json_response['title'],
                defaults={
                    'short_description': json_response['description_short'],
                    'long_description': json_response['description_long'],
                    'lng': json_response['coordinates']['lng'],
                    'lat': json_response['coordinates']['lat'],
                }
            )

            if created:
                add_photo_to_place_model(response, place)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully add place {json_response["title"]}'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Not added. A place named '
                    f'{json_response["title"]} already exists'))

        except requests.exceptions.HTTPError:
            raise CommandError('Страница с JSON не найдена, '
                               'проверьте отправленную команду!')
