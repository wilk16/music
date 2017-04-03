from django.contrib import admin

# Register your models here.

from .models import Band, Label, Genre, Record, Track, OwnedRecord


class RecordAdmin(admin.ModelAdmin):
    list_display=('title', 'release_date', 'label_fk')
    filter_horizontal = ('bands', 'genres',)

admin.site.register(Band)
admin.site.register(Label)
admin.site.register(Genre)
admin.site.register(Record, RecordAdmin)
admin.site.register(Track)
admin.site.register(OwnedRecord)

