from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from places.models import Place


def index(request):
    places = Place.objects.all()
    raw_places = []
    for place in places:
        raw_place = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse(
                    get_detail_raw_place,
                    kwargs={'id': place.id}
                )
            }
        }
        raw_places.append(raw_place)

    response_payload = {
      "type": "FeatureCollection",
      "features": raw_places
    }

    context = {'response_payload': response_payload}
    return render(request, 'index.html', context)


def get_detail_raw_place(request, id):
    place = get_object_or_404(Place, id=id)
    urls_photos = [photo.image.url for photo in place.photos.all()]
    detail_raw_place = {
        "title": place.title,
        "imgs": urls_photos,
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lat": place.lat,
            "lng": place.lng
        }
    }
    return JsonResponse(detail_raw_place,
                        safe=False,
                        json_dumps_params={'ensure_ascii': False, 'indent': 4}
                        )
