from django.test import TestCase, Client
from music.models import Band, Record, Genre, Label, Track, OwnedRecord
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime



class RecordListViewTests(TestCase):
    """
    Tests for RecordList view
    """
    def setUp(self):
        self.user = User.objects.create(username='tester')
        self.c = Client()

    def test_no_label(self):
        """
        Behavior when there are no records in DB
        """
        response = self.c.get(reverse('music:record_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['objects'], [])


    def test_one_label(self):
        """
        Behavior when there is a record to display
        """
        self.band = Band.objects.create(name='myBand', origin='USA',
                                       create_by=self.user, modify_by=self.user)
        self.label = Label.objects.create(name='Test_music', city='Testcity',
                            country='testcountry', website='www.mywebsite.pl',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.genre = Genre.objects.create(name='testgenre',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record = Record.objects.create(title='mytitle',
                          label_fk = self.label,
                          release_date = '2017-02-03',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record.bands.add(self.band)
        self.record.genres.add(self.genre)

        response = self.c.get(reverse('music:label_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['objects'].paginator.count, 1)






class LabelListViewTests(TestCase):
    """
    Tests for LabelList view
    """
    def setUp(self):
        self.user = User.objects.create(username='tester')
        self.c = Client()

    def test_no_label(self):
        """
        Behavior when there are no labels in DB
        """
        response = self.c.get(reverse('music:label_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['objects'], [])


    def test_one_label(self):
        """
        Behavior when there is a label to display
        """
        self.label = Label.objects.create(name='myLabel', city='testCity',
                                          country='mycountry',
                                          website='www.mywebsite.pl',
                                          create_by=self.user, modify_by=self.user)
        response = self.c.get(reverse('music:label_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['objects'].paginator.count, 1)





class GenreListViewTests(TestCase):
    """
    Tests for GenreList view
    """
    def setUp(self):
        self.user = User.objects.create(username='tester')
        self.c = Client()

    def test_no_genre(self):
        """
        Behavior when there are no genres in DB (for some reason?)
        """
        response = self.c.get(reverse('music:genre_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['objects'], [])


    def test_one_genre(self):
        """
        Behavior when there is a genre to display
        """
        self.genre = Genre.objects.create(name='myGenre',
                                          create_by=self.user, modify_by=self.user)
        response = self.c.get(reverse('music:genre_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['objects'].paginator.count, 1)





class BandListViewTests(TestCase):
    """
    Tests for BandList view
    """
    def setUp(self):
        self.user = User.objects.create(username='tester')
        self.c = Client()

    def test_no_bands(self):
        """
        Behavior when there are no bands in DB (for some reason?)
        """
        response = self.c.get(reverse('music:band_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['objects'], [])


    def test_one_band(self):
        """
        Behavior when there is a band to display
        """
        self.band = Band.objects.create(name='myBand', origin='USA',
                                       create_by=self.user, modify_by=self.user)
        response = self.c.get(reverse('music:band_list', kwargs={'page_nb':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['objects'].paginator.count, 1)



class OwnedRecordModelTests(TestCase):
    """
    Tests for OwnedRecords model
    """
    def setUp(self):
        self.user = User.objects.create(username='tester')
        self.band = Band.objects.create(name='myBand', origin='USA',
                                       create_by=self.user, modify_by=self.user)
        self.label = Label.objects.create(name='Test_music', city='Testcity',
                            country='testcountry', website='www.mysite.pl',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.genre = Genre.objects.create(name='testgenre',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record = Record.objects.create(title='mytitle',
                          label_fk = self.label,
                          release_date = '2017-02-03',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record.bands.add(self.band)
        self.record.genres.add(self.genre)

    def test_OwnedRecord_create(self):
        """
        Check if created OwnedRecord has required attributes
        """
        self.owned_record = OwnedRecord.objects.create(disc_type='vinyl',
                                               record_fk=self.record,
                                               user_fk=self.user,
                                               purchase_date=timezone.now())

        self.assertEqual(self.owned_record.record_fk.title, 'mytitle')
        self.assertEqual(self.owned_record.user_fk.username, 'tester')



class BandModelTests(TestCase):
    """
    Tests for band model
    """
    def setUp(self):
        """
        Initial setup of one band object
        """
        self.user= User.objects.create(username='tester')
        self.band = Band.objects.create(name='myBand', origin='USA',
                                       create_by=self.user, modify_by=self.user)

    def test_simple_band(self):
        """
        Test basic scenarios: band name, origin and create_by
        """
        self.assertEqual(self.band.name, 'myBand')
        self.assertEqual(self.band.origin, 'USA')
        self.assertEqual(self.band.create_by, self.user)
        self.assertTrue(timezone.now()- timezone.timedelta(days=1) < self.band.create_date<=timezone.now())

    def test_create_and_modify_user(self):
        """
        test create_by and modify_by fields behavior
        """
        self.user2 = User.objects.create(username='modifier')
        self.assertEqual(self.band.create_by, self.user,
                        'wrong create_by before update')
        self.band.name = 'new_band'
        self.band.modify_by = self.user2
        self.band.save()
        self.assertEqual(self.band.create_by, self.user,
                        'wrong create_by after update')
        self.assertEqual(self.band.modify_by, self.user2,
                        'wrong modify_by')
        self.assertEqual(self.band.name, 'new_band', 'band name not modified')
        self.assertEqual(self.band.origin, 'USA', 'band origin changed')
        self.band.delete()
        self.user.delete()
        self.user2.delete()




class RecordModelTests(TestCase):
    """
    Test for record model
    """
    def test_record_title(self):
        """
        test if setting up a record works by checking the title
        """
        self.user = User.objects.create(username = 'tester')
        self.band = Band.objects.create(name='myBand', origin='Testland',
                                       create_by=self.user, modify_by=self.user)
        self.label = Label.objects.create(name='Test_music', city='Testcity',
                            country='testcountry', website='www.mysite.pl',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.genre = Genre.objects.create(name='testgenre',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record = Record.objects.create(title='mytitle',
                          label_fk = self.label,
                          release_date = '2017-02-03',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record.bands.add(self.band)
        self.record.genres.add(self.genre)
        self.assertEqual(self.record.title, "mytitle")


class RecordViewTests(TestCase):
    """
    Test for Record view
    """
    def setUp(self):
        """
        Set up basic record objectsView
        """
        self.user = User.objects.create(username = 'test')
        self.band = Band.objects.create(name='myBand', origin='Testland',
                                        create_by = self.user,
                                        modify_by = self.user)
        self.label = Label.objects.create(name='Test_music', city='Testcity',
                        country='testcountry', website='www.mysite.pl',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.genre = Genre.objects.create(name='testgenre',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record = Record.objects.create(title='mytitle',
                          label_fk = self.label,
                          release_date = '2017-02-03',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record.bands.add(self.band)
        self.record.genres.add(self.genre)
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
        self.t1=Track.objects.create(name='t1', number=1, length='00:12:45',
                      record_fk =self.record, create_by=self.user,
                                         modify_by=self.user)
        self.t2=Track.objects.create(name='t2', number=2, length='00:03:13',
                      record_fk =self.record, create_by=self.user,
                                         modify_by=self.user)
        response = self.c.get(reverse('music:record', args=(self.record.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tracks'].count(), 2)
        self.assertEqual(response.context['tracks'][0].name, 't1')
        self.assertEqual(response.context['tracks'][1].length,
                          datetime.time(0,3,13))

    def test_display_for_featured_track(self):
        """
        Check if featured artist will be seen from recordView
        """
        self.t1=Track.objects.create(name='t1', number=1, length='00:12:45',
                      record_fk =self.record, create_by=self.user,
                                         modify_by=self.user)
        self.band_feat = Band.objects.create(name='featBand', origin='Testland',
                                        create_by = self.user,
                                        modify_by = self.user)
        self.t1.feat.add(self.band_feat)
        self.assertEqual(self.t1.feat.all().count(), 1)



class UserPanelViewTests(TestCase):
    """
    Testing of user panel view
    """
    def setUp(self):
        """
        Set up basic record objectsView
        """
        self.user = User.objects.create(username = 'test')
        self.band = Band.objects.create(name='myBand', origin='Testland',
                                        create_by = self.user,
                                        modify_by = self.user)
        self.label = Label.objects.create(name='Test_music', city='Testcity',
                        country='testcountry', website='www.mysite.pl',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.genre = Genre.objects.create(name='testgenre',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record = Record.objects.create(title='mytitle',
                          label_fk = self.label,
                          release_date = '2017-02-03',
                                         create_by=self.user,
                                         modify_by=self.user)
        self.record.bands.add(self.band)
        self.record.genres.add(self.genre)
        self.c = Client()
        self.c.post('/login/', {'username':'test', 'password':'qwerasdf'})

    def test_display_last_records_with_no_records(self):
        """
        Check if context list is empty
        """
        response = self.c.get(reverse('music:userPanel'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['recent_records'], [])

    def test_display_last_records_with_record_from_past(self):
        """
        Check if record bought in past is displayed
        """
        self.ownedRec = OwnedRecord.objects.create(record_fk=self.record,
                                purchase_date = timezone.now() + datetime.timedelta(days=-2),
                                disc_type = 'vinyl', user_fk=self.user)
        response = self.c.get(reverse('music:userPanel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recent_records'], [])

    def test_display_last_records_with_record_from_future(self):
        """
        Check if record bought with future_date(preorder?) will not be
        displayed
        """
        self.ownedRec = OwnedRecord.objects.create(record_fk=self.record,
                                purchase_date = timezone.now() + datetime.timedelta(days=2),
                                disc_type = 'vinyl', user_fk=self.user)
        response = self.c.get(reverse('music:userPanel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recent_records'], [])




