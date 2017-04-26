from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField)

from music.models import Band, Label, Genre, Record, Track


class BandCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Band
        fields = ('name', 'origin',)

class BandDetailSerializer(ModelSerializer):
    create_by = SerializerMethodField()
    record_list = SerializerMethodField()

    class Meta:
        model = Band
        fields = ('id',
                  'name',
                 'origin',
                 'record_list',
                 'create_by',
                 'create_date')
        read_only_fields = ('id', 'create_by', 'create_date')

    def get_create_by(self, obj):
        return str(obj.create_by.username)
    def get_record_list(self, obj):
        rec_list = [record.title for record in obj.record_set.all()]
        return str(', '.join(rec_list))

class BandListSerializer(ModelSerializer):
    class Meta:
        model = Band
        fields = ('name',
                  'origin')

class LabelCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ('name', 'country', 'city', 'website')

class LabelDetailSerializer(ModelSerializer):
    create_by = SerializerMethodField()
    class Meta:
        model = Label
        fields = ('id', 'name', 'country', 'city', 'website',
                 'create_by', 'create_date')
        read_only_fields = ('id', 'create_date', 'create_date')

    def get_create_by(self, obj):
        return str(obj.create_by.username)

class LabelListSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ('name', 'country', 'city', 'website')


class GenreCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'description', 'source')

class GenreDetailSerializer(ModelSerializer):
    create_by = SerializerMethodField()
    class Meta:
        model = Genre
        fields = ('id', 'name', 'description', 'source',
                 'create_by', 'create_date')
        read_only_fields = ('id', 'create_date', 'create_by')

    def get_create_by(self, obj):
        return str(obj.create_by.username)


class GenreListSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'description', 'source')

"""
class RecordCreateUpdateSerializer(ModelSerializer):
    label = SerializerMethodField()
    genres = SerializerMethodField()
    bands = SerializerMethodField()

    class Meta:
        model = Record
        fields = ('title', 'bands', 'release_date', 'label', 'genres')

    def get_label(self, obj):
        return str(obj.label_fk.name)

    def get_genres(self, obj):
        genre_list = [genre.name for genre in obj.genres.all()]
        return str(', '.join(genre_list))

    def get_bands(self, obj):
        band_list = [band.name for band in obj.bands.all()]
        return str(', '.join(band_list))
"""



class RecordDetailSerializer(ModelSerializer):
    create_by = SerializerMethodField()
    label = SerializerMethodField()
    genres = SerializerMethodField()
    bands = SerializerMethodField()

    class Meta:
        model = Record
        fields = ('id', 'title', 'bands', 'release_date', 'label', 'genres',
                 'create_by', 'create_date')
        read_only_fields = ('id', 'create_date', 'create_by')

    def get_create_by(self, obj):
        return str(obj.create_by.username)

    def get_label(self, obj):
        return str(obj.label_fk.name)

    def get_genres(self, obj):
        genre_list = [genre.name for genre in obj.genres.all()]
        return str(', '.join(genre_list))

    def get_bands(self, obj):
        band_list = [band.name for band in obj.bands.all()]
        return str(', '.join(band_list))



class RecordListSerializer(ModelSerializer):
    label = SerializerMethodField()
    genres = SerializerMethodField()
    bands = SerializerMethodField()

    class Meta:
        model = Record
        fields = ('title', 'bands', 'release_date', 'label', 'genres')

    def get_label(self, obj):
        return str(obj.label_fk.name)

    def get_genres(self, obj):
        genre_list = [genre.name for genre in obj.genres.all()]
        return str(', '.join(genre_list))

    def get_bands(self, obj):
        band_list = [band.name for band in obj.bands.all()]
        return str(', '.join(band_list))




