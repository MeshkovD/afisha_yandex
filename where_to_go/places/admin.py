from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from places.models import Place, Photo


class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    fields = ['image', 'place_photo', 'order']
    readonly_fields = ['place_photo']
    extra = 0
    empty_value_display = 'Здесь будет превью, когда вы выберете файл'

    def place_photo(self, obj):
        return format_html('<img src="{url}" height={height}"/>',
                           url=obj.image.url,
                           height=200,
                           )

class PlaceAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'place_short_description',
    ]

    fields = ['title', 'place_short_description', 'place_long_description', 'lng', 'lat']
    inlines = [PhotoInline]
    list_per_page = 25
    search_fields = ['title']



admin.site.register(Place, PlaceAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        'place',
        'place_photo',
    ]
    fields = ['image', 'place', 'order', 'place_photo']
    raw_id_fields = ["place"]
    ordering = ['place', 'order']
    readonly_fields = ['place_photo']
    empty_value_display = 'Здесь будет превью, когда вы выберете файл'

    def place_photo(self, obj):
        return format_html('<img src="{url}" height={height}/>',
                           url=obj.image.url,
                           height=200,
                           )


admin.site.register(Photo, PhotoAdmin)
