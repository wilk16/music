from django.contrib import admin

# Register your models here.

from .models import Band, Label, Genre, Record, Track, OwnedRecord

admin.site.register(Band)
admin.site.register(Label)
admin.site.register(Genre)
admin.site.register(Record)
admin.site.register(Track)
admin.site.register(OwnedRecord)

