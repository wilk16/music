from django.test import TestCase, Client
from music.models import Band, Record, Genre, Label, Track
from django.urls import reverse
from django.utils import timezone
import datetime

class RecordModelTests(TestCase):
    """
    Test for record model
    """
    def test_record_title(self):
        """
        """
        sband = Band('myBand', 'Testland')
        slabel = Label('Test_music', 'Testcity',
                            'testcountry', 'testaddr')
        sgenre = Genre('testgenre')
        srecord = Record(band_fk = sband, title='test_title',
                              label_fk = slabel,
                              genre_fk = sgenre,
                             release_date = timezone.now())
        self.assertEqual(srecord.title, "test_title")

class RecordViewTests(TestCase):
    """
    Test for Record view
    """
    def setUp(self):
        """
        Set up basic record objectsView
        """
        self.band = Band(name='myBand', origin='Testland')
        self.label = Label(name='Test_music', city='Testcity',
                        country='testcountry', address='testaddr')
        self.genre = Genre(name='testgenre')
        self.band.save()
        self.label.save()
        self.genre.save()
        self.record = Record(band_fk = self.band, title='mytitle',
                          label_fk = self.label,
                          genre_fk = self.genre,
                          release_date = '2017-02-03')

        self.record.save()
        self.c = Client()

    def test_setup(self):
        """
        Simple sanity check
        """
        self.assertEqual(self.record.title, 'mytitle', 'bad record title')
        self.assertEqual(self.band.name, 'myBand', 'bad band name')
        self.assertEqual(self.label.name, 'Test_music', 'band label name')

    def test_if_record_page_exists(self):
        """
        Test if page for test record from setup stage exists
        """
        response = self.c.get(reverse('music:record', args=(self.record.id,)))
        self.assertEqual(response.status_code, 200)

    def test_if_other_records_are_skipped(self):
        """
        If band has only one record, section with other records should be
        replaced with sufficient info
        """
        response = self.c.get(reverse('music:record', args=(self.record.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['band_records'], [])

    def test_if_no_tracks_in_record(self):
        """
        Test if there are no tracks on album
        """
        response = self.c.get(reverse('music:record', args=(self.record.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['tracks'], [])

    def test_two_tracks_in_record(self):
        """
        Create two tracks on test album
        """
        self.t1=Track(name='t1', number=1, length='00:12:45',
                      record_fk =self.record)
        self.t1.save()
        self.t2=Track(name='t2', number=2, length='00:03:13',
                      record_fk =self.record)
        self.t2.save()
        response = self.c.get(reverse('music:record', args=(self.record.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tracks'].count(), 2)
        self.assertEqual(response.context['tracks'][0].name, 't1')
        self.assertEqual(response.context['tracks'][1].length,
                         datetime.time(0,3,13))


