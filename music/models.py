from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Band(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=100)
    create_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='band_create_by')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='band_modify_by')
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

class Label(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    website = models.URLField(null=True)
    create_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='label_create_by')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='label_modify_by')
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

class Genre(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    source = models.URLField(null=True)
    create_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='gener_create_by')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='genre_modify_by')
    modify_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, allow_unicode=True,
                           default = '')
    class Meta:
        ordering = ['name']

class Record(models.Model):
    def __str__(self):
        return self.title

    bands = models.ManyToManyField(Band)
    title = models.CharField(max_length=200)
    label_fk= models.ForeignKey(Label, on_delete=models.CASCADE)
    genres= models.ManyToManyField(Genre)
    release_date = models.DateField()
    create_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='record_create_by')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='record_modify_by')
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_date']

class Track(models.Model):
    def __str__(self):
        return self.record_fk.title + ' - ' + self.name

    record_fk = models.ForeignKey(Record, on_delete=models.CASCADE)
    name =  models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    length = models.TimeField()
    feat = models.ManyToManyField(Band, blank=True)
    create_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='track_create_by')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='track_modify_by')
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

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
    user_fk = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-purchase_date']

class Review(models.Model):
    def __str__(self):
        return "(" +str(self.create_date)[0:10] + ") - " +\
                self.create_by.username + ": "+ self.review_text[0:100]

    record_fk = models.ForeignKey(Record, on_delete=models.CASCADE)
    review_text = models.TextField()
    like_counter = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    create_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='review_create_by')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User, default = 1,
                                  on_delete=models.CASCADE,
                                 related_name='review_modify_by')
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modify_date']


