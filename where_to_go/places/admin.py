from django.contrib import admin

from places.models import Place, Photo


class PhotoInline(admin.TabularInline):
    model = Photo


class PlaceAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description_short',
    ]
    inlines = [PhotoInline]


admin.site.register(Place, PlaceAdmin)


class PhotoAdmin(admin.ModelAdmin):
    ordering = ['place', 'order']


admin.site.register(Photo, PhotoAdmin)
