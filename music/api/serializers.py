from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField)

from music.models import Band, Label, Genre


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
        read_only_fields = ('id', 'create_date', 'create_date')

    def get_create_by(self, obj):
        return str(obj.create_by.username)


class GenreListSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'description', 'source')
