from django.shortcuts import render

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

