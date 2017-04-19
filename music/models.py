from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg


class Band(models.Model):
    """
    Model implementing band instance. Default sort: name
    """
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
    slug = models.SlugField(max_length=50, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Band, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Label(models.Model):
    """
    Model implementing label instance.Default sort name
    """
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
    slug = models.SlugField(max_length=50, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Label, self).save(*args, **kwargs)

    def get_related_records(self):
        """
        Return a list of 10 records from this label
        """
        try:
            result_set = self.record_set.all()[0:10]
        except:
            result_set = None
        return result_set

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    """
    Model implementing genre instance. Default sort name
    """
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
    slug = models.SlugField(max_length=50, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)


    def get_related_records(self):
        """
        Return a list of 10 records of selected genre
        """
        try:
            result_set = self.record_set.all()[0:10]
        except:
            result_set = None

        return result_set

    class Meta:
        ordering = ['name']


class Record(models.Model):
    """
    Model implementing record instance. Default sort -release_date
    """
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
    slug = models.SlugField(max_length=50, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Record, self).save(*args, **kwargs)

    def get_avg_score(self):
        """
        Return average score of an album or '-' if there are no reviews
        """
        avg_score = self.review_set.all().aggregate(Avg('score'))['score__avg']
        if avg_score:
            return avg_score
        else:
            return '-'

    def get_related_tracks(self):
        """
        return a list of tracks from the record
        """
        return self.track_set.all()

    def get_user_review(self, user):
        """
        return current user's review of this record
        """
        try:
            if user.is_authenticated():
                return self.review_set.get(create_by = user)
            else:
                return None
        except Review.DoesNotExist:
            return None
        except:
            return None

    def get_related_reviews(self, user):
        """
        Return list of 10 latest reviews written by other users
        """
        if user.is_authenticated():
            return self.review_set.all().exclude(create_by=user)[0:10]
        else:
            return self.review_set.all()[0:10]

    def get_bands_other_records(self):
        """
        Return a list of 10 latest other records of bands responsible for
        current record
        """
        record_list = []
        for band in self.bands.all():
            for record in band.record_set.exclude(id = self.id):
                record_list.append(record)
        return record_list


    class Meta:
        ordering = ['-release_date']


class Track(models.Model):
    """
    Model implementing track instance, default sort number
    """

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
    slug = models.SlugField(max_length=50, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Track, self).save(*args, **kwargs)
    class Meta:
        ordering = ['number']


class OwnedRecord(models.Model):
    """
    Model implementing record owned by user. Default sort -purchase_date
    """

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

    def get_recent_records(user):
        """
        Return a list of 10 latest bought records by current user
        """
        if user.is_authenticated():
            return OwnedRecords.objects.filter(purchase_date__lte=\
                            timezone.now()).filter(user_fk = user)[0:10]

        else:
            return []

    class Meta:
        ordering = ['-purchase_date']


class Review(models.Model):
    """
    Model implementing review of records. Default sort -modify_date
    """

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
    slug = models.SlugField(max_length=50, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.review_text[0:50])
        super(Review, self).save(*args, **kwargs)
    class Meta:
        ordering = ['-modify_date']



