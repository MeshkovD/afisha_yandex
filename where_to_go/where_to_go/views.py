from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from places.models import Place


def index(request):
    places = Place.objects.all()
    json_places = []
    for place in places:
        json_place = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse(
                    get_object_in_json_for_id,
                    kwargs={'id': place.id}
                )
            }
        }
        json_places.append(json_place)

    geo_json_places = {
      "type": "FeatureCollection",
      "features": json_places
    }

    context = {'geo_json_places': geo_json_places}
    return render(request, 'index.html', context)


def get_object_in_json_for_id(request, id):
    place = get_object_or_404(Place, id=id)
    urls_photos = []
    for photo in place.photo.all():
        url_photo = photo.image.url
        urls_photos.append(url_photo)
    obj = {
        "title": place.title,
        "imgs": urls_photos,
        "description_short": place.place_short_description,
        "description_long": place.place_long_description,
        "coordinates": {
            "lat": place.lat,
            "lng": place.lng
        }
    }
    return JsonResponse(obj,
                        safe=False,
                        json_dumps_params={'ensure_ascii': False, 'indent': 4}
                        )
