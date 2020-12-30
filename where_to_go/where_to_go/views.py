from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from places.models import Place


def index(request):
    places = Place.objects.all()
    obj_list = []
    for place in places:
        obj = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": "static/places/moscow_legends.json"
            }
        }
        obj_list.append(obj)

    list_of_all_places = {
      "type": "FeatureCollection",
      "features": obj_list
    }

    context = {'list_of_all_places': list_of_all_places}
    return render(request, 'index.html', context)


def get_object_in_json_for_id(request, id):
    place = get_object_or_404(Place, id=id)
    list_photos_urls = []
    for photo in place.photo_set.all():
        url_of_photo = photo.image.url
        list_photos_urls.append(url_of_photo)
    obj = {
        "title": place.title,
        "imgs": list_photos_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lat": place.lat,
            "lng": place.lng
        }
    }
    return JsonResponse(obj,safe=False, json_dumps_params={'ensure_ascii': False, 'indent':4})
