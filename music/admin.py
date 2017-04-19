from django.contrib import admin

# Register your models here.

from .models import Band, Label, Genre, Record, Track, OwnedRecord, Review


class RecordAdmin(admin.ModelAdmin):
    list_display=('title', 'release_date', 'label_fk')
    filter_horizontal = ('bands', 'genres',)
    list_filter=('release_date',)
    fields = ('title', 'bands', 'release_date', 'label_fk', 'genres')


class TrackAdmin(admin.ModelAdmin):
    list_display=('name', 'record_fk', 'number')
    search_fields=('name', 'record_fk')
    ordering=('record_fk', 'number')
    filter_horizontal=('feat',)

admin.site.register(Band)
admin.site.register(Label)
admin.site.register(Genre)
admin.site.register(Record, RecordAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(OwnedRecord)
admin.site.register(Review)
