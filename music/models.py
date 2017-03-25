from django.db import models
from django.utils import timezone

# Create your models here.

class Band(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=100)

class Label(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class Genre(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)

class Record(models.Model):
    def __str__(self):
        return self.title
    band_fk = models.ForeignKey(Band, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    label_fk= models.ForeignKey(Label, on_delete=models.CASCADE)
    genre_fk= models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_date = models.DateField()

class Track(models.Model):
    def __str__(self):
        return self.name
    record_fk = models.ForeignKey(Record, on_delete=models.CASCADE)
    name =  models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    length = models.TimeField()

class OwnedRecord(models.Model):
    def __str__(self):
        return self.record_fk.band_fk.name + ': ' + self.record_fk.title
    disc_type_choice = (
        ('vinyl', 'Vinyl Disc'),
        ('cd','CD'),
    )
    record_fk = models.ForeignKey(Record, on_delete=models.CASCADE)
    purchase_date = models.DateField(default=timezone.now)
    disc_type = models.CharField(max_length=10, choices=disc_type_choice)

