from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
import requests
from django.db.models import Q

from places.models import Place, Photo


def get_name(image_url):
    '''Генерирует имя картинки по переданному url'''
    return image_url.split('/')[-1]

def add_photo_to_place_model(img_response, place):
    filename = get_name(img_response.url)
    new_photo = Photo(place=place)
    new_photo.image.save(filename,
                         ContentFile(img_response.content),
                         save=True)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_url')

    def handle(self, *args, **options):
        json_url = options["json_url"]

        try:
            response = requests.get(json_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise CommandError('Страница с JSON не найдена, '
                           'проверьте отправленную команду!')
        place_raw = response.json()
        place, created = Place.objects.get_or_create(
            title=place_raw['title'],
            defaults={
                'short_description': place_raw['description_short'],
                'long_description': place_raw['description_long'],
                'lng': place_raw['coordinates']['lng'],
                'lat': place_raw['coordinates']['lat'],
            }
        )

        if created:
            photos_links = place_raw['imgs']
            for photo_link in photos_links:
                try:
                    img_response = requests.get(photo_link)
                    img_response.raise_for_status()
                except requests.exceptions.HTTPError:
                    raise CommandError('Картинка не добавлена, '
                                       'ссылка может содержать ошибку!')
                add_photo_to_place_model(img_response, place)


            self.stdout.write(self.style.SUCCESS(
                f'Successfully add place {place_raw["title"]}'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Not added. A place named '
                f'{place_raw["title"]} already exists'))


