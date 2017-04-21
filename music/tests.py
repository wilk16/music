from django.test import TestCase, Client
from music.models import Band, Record, Genre, Label, Track, OwnedRecord, Review
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime
from django.utils.text import slugify

##----------------------Default Generators
def create_user(_username = 'tester', _password = 'aaaaaaaa'):
    return User.objects.create(username = _username, password = _password)

def create_band(_user, _name = 'sample_band', _origin='testLand'):
    return Band.objects.create(name = _name, origin = _origin,\
                              create_by = _user, modify_by = _user)

def create_label(_user, _name = 'TestLabel', _city = 'TestCity',\
                 _country = 'TestCountry', _website = 'test.abc.pl'):
    return Label.objects.create(name = _name, city = _city, country = _country,
                               website = _website, create_by = _user,
                               modify_by = _user )

def create_genre(_user, _name = 'TestGenre', _description = 'SomeText',\
                 _source = 'test.src.pl'):
    return Genre.objects.create(name = _name, description = _description,
                               source = _source,
                               create_by = _user, modify_by = _user)

def create_record(_user, _label, _title = 'TestTitle', _bands = [],\
                  _genres = [], _release_date = timezone.now()):
    r = Record.objects.create(title = _title, release_date = _release_date,
                                label_fk = _label,\
                                create_by = _user, modify_by = _user)
    for band in _bands:
        r.bands.add(band)

    for genre in _genres:
        r.genres.add(genre)
    r.save()
    return r

def create_review(_user, _record, _review_text = 'TestReview', _score = 3):
    return Review.objects.create(review_text = _review_text, score = _score,\
                                 record_fk = _record,\
                                 create_by = _user, modify_by = _user)

def create_track(_user, _record, _feat, _name = 'TestTrack', _number = 1,\
                 _length = '00:03:15'):
    t = Track.objects.create(name = _name, number = _number, length = _length,
                                 record_fk = _record,
                                 create_by = _user, modify_by = _user)
    for band in _feat:
        t.feat.add(band)
    t.save()
    return t


def create_ownedrecord(_user, _record, _purchase_date = timezone.now(),
                       _disc_type = 'cd'):
    return OwnedRecord.objects.create(record_fk = _record, user_fk = _user,
                                     purchase_date = _purchase_date,
                                     disc_type = _disc_type)

##-----------------------Model Tests



class BandModelTests(TestCase):
    """
    Tests for band model
    """

    def setUp(self):
        """
        Initial setup of one band object
        """
        self.user= create_user()
        self.band = create_band(_user = self.user)

    def test_band_basic_properties(self):
        """
        Test basic scenarios: band name, origin and create_by
        """
        self.assertEqual(self.band.name, 'sample_band', 'wrong band name')
        self.assertEqual(self.band.origin, 'testLand', 'wrong band origin')
        self.assertEqual(self.band.create_by, self.user, 'wrong user')
        self.assertTrue(timezone.now()- timezone.timedelta(days=1) <
                        self.band.create_date<=timezone.now())

    def test_create_and_modify_user(self):
        """
        test create_by and modify_by fields behavior
        """
        self.user2 = create_user(_username = 'user2')
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
        self.assertEqual(self.band.origin, 'testLand', 'band origin changed')


class LabelModelTests(TestCase):
    """
    Test for label model
    """

    def setUp(self):
        self.user = create_user()
        self.label = create_label(_user = self.user)

    def test_label_basic_properties(self):
        """
        Test if basic fields are properly filled
        """
        self.assertEqual(self.label.name, 'TestLabel', 'wrong label name')
        self.assertEqual(self.label.city , 'TestCity', 'wrong label city')

    def test_get_related_records_with_no_records(self):
        """
        Should return empty queryset
        """

        self.assertFalse(self.label.get_related_records())


    def test_get_related_records_with_records(self):
        """
        Should return some records
        """
        self.genre = create_genre(_user = self.user)
        self.band = create_band(_user = self.user)
        self.record = create_record(_user = self.user, _bands = [self.band],
                                   _genres = [self.genre], _label = self.label)

        self.assertQuerysetEqual(self.label.get_related_records(),\
                             ['<Record: TestTitle>'])


class GenreModelTests(TestCase):
    """
    Test for genre model
    """

    def setUp(self):
        self.user = create_user()
        self.genre = create_genre(_user = self.user)

    def test_genre_basic_properties(self):
        """
        Test if basic fields are properly filled
        """
        self.assertEqual(self.genre.name, 'TestGenre', 'wrong genre name')
        self.assertEqual(self.genre.source , 'test.src.pl', 'wrong genre source')

    def test_get_related_records_with_no_records(self):
        """
        Should return empty queryset
        """

        self.assertFalse(self.genre.get_related_records())


    def test_get_related_records_with_records(self):
        """
        Should return some records
        """
        self.label = create_label(_user = self.user)
        self.band = create_band(_user = self.user)
        self.record = create_record(_user = self.user, _bands = [self.band],
                                   _genres = [self.genre], _label = self.label)

        self.assertQuerysetEqual(self.genre.get_related_records(),\
                             ['<Record: TestTitle>'])


class RecordModelTests(TestCase):
    """
    Test for record model
    """
    def setUp(self):
        self.user = create_user()
        self.genre = create_genre(_user = self.user)
        self.label = create_label(_user = self.user)
        self.band = create_band(_user = self.user)
        self.record = create_record(_user = self.user, _bands = [self.band],
                                   _label = self.label, _genres = [self.genre])

    def test_record_basic_properties(self):
        """
        Test if basic fields are properly filled
        """
        self.assertEqual(self.record.title, 'TestTitle', 'wrong record title')
        self.assertQuerysetEqual(self.record.bands.all(),
                                 ['<Band: sample_band>'])
        self.assertEqual(self.record.label_fk.name, 'TestLabel',
                         'wrong record label')

    def test_get_avg_score_with_no_reviews(self):
        """
        Method should return '-' when there are no reviews
        """
        self.assertEqual(self.record.get_avg_score(), '-')

    def test_get_avg_score_with_reviews(self):
        """
        Method should return an average scores
        """
        self.review = create_review(_user = self.user, _record = self.record,
                                    _review_text='Text1')

        self.assertEqual(self.record.get_avg_score(), 3.0)
        self.review2 = create_review(_user = self.user, _record = self.record,\
                                    _score = 5, _review_text = 'text2')
        self.assertEqual(self.record.get_avg_score(), 4.0)

    def test_get_related_tracks_with_no_tracks(self):
        """
        Method should return empty queryset
        """
        self.assertFalse(self.record.get_related_tracks())

    def test_get_related_tracks_with_tracks(self):
        """
        Method should return tracks from this record
        """
        self.track = create_track(_user = self.user, _record = self.record,\
                                 _feat = [])
        self.assertQuerysetEqual(self.record.get_related_tracks(),\
                                 ['<Track: TestTitle - TestTrack>'])

    def test_get_user_review_with_no_review(self):
        """
        Method should return None
        """
        self.client = Client()
        self.client.login(username = self.user.username,
                     password = self.user.password)
        self.assertFalse(self.record.get_user_review(self.user))

    def test_get_user_review_with_review_when_not_authenticated(self):
        """
        Method should return None for unknown users
        """
        ######fixit
        pass
        
        #self.user2 = create_user(_username = 't2', _password = 'zzzzzzzz')
        #self.review = create_review(_user = self.user, _record = self.record,
        #                           _review_text = 'text3')
        #self.client.login(username = self.user2.username,
        #                 password = self.user2.password)
        #self.assertFalse(self.client.)

        #self.assertFalse(self.record.get_user_review(self.user))


    def test_get_user_review_with_review_when_authenticated(self):
        """
        Method should return user's review
        """
        self.review = create_review(_user = self.user, _record = self.record,
                                   _review_text = 'text4')
        self.client.login(username = self.user.username,
                     password = self.user.password)

        self.assertEqual(self.record.get_user_review(self.user),
                         self.review)

    def test_get_related_reviews_when_not_authenticated(self):
        """
        Should return last 10 reviews
        """
        ######fixit
        self.u2 = create_user(_username = 'u2')

        self.review = create_review(_user = self.u2, _record = self.record)
        self.review2 = create_review(_user = self.u2, _record = self.record)

        self.assertEqual(self.record.get_related_reviews(self.user).count(),
                         2)

    def test_get_related_reviews_with_no_reviews(self):
        """
        Should return empty queryset
        """
        self.assertFalse(self.record.get_related_reviews(self.user))

    def test_get_related_reviews_when_user_wrote_review(self):
        """
        Should return queryset without user's review
        """
        self.u2 = create_user(_username = 'u2')
        self.review = create_review(_user = self.user, _record = self.record)
        self.review2 = create_review(_user = self.u2, _record = self.record)
        self.review3 = create_review(_user = self.u2, _record = self.record)

        self.assertEqual(self.record.get_related_reviews(self.user).count(),
                         2)

    def test_get_bands_other_records_when_no_other_records(self):
        """
        Should return an empty list
        """
        self.assertFalse(self.record.get_bands_other_records())

    def test_get_bands_other_records_with_other_records(self):
        """
        Should return a list of max 10 records
        """
        self.r2 = create_record(_user = self.user, _bands = [self.band],
                                   _label = self.label, _genres = [self.genre])
        self.assertEqual(self.record.get_bands_other_records(), [self.r2])

    def test_get_bands_other_records_on_collab_record(self):
        """
        Should return a list of albums of all collaborating artists
        """
        self.b2 = create_band(_user = self.user, _name = 'Other_band')
        self.r2 = create_record(_user = self.user, _bands = [self.b2],
                                   _label = self.label, _genres = [self.genre])
        self.r3 = create_record(_user = self.user, _label = self.label,
                                    _bands = [self.band, self.b2],
                                    _genres = [self.genre])
        self.assertEqual(len(self.r3.get_bands_other_records()), 2)


class TrackModelTests(TestCase):
    """
    Tests for track model
    """
    def setUp(self):
        self.user = create_user()
        self.genre = create_genre(_user = self.user)
        self.label = create_label(_user = self.user)
        self.band = create_band(_user = self.user)
        self.record = create_record(_user = self.user, _bands = [self.band],
                                   _label = self.label, _genres = [self.genre])
        self.track = create_track(_user = self.user, _record = self.record,
                                 _feat = [])

    def test_track_basic_properties(self):
        """
        Test if fields are properly filled
        """
        self.assertEqual(self.track.name, 'TestTrack')
        self.b2 = create_band(_user = self.user)
        self.track.feat.add(self.b2)
        self.track.save()
        self.assertEqual(self.track.feat.all().count(), 1)


class OwnedRecordModelTests(TestCase):
    """
    Test for OwnedRecord model
    """
    def setUp(self):
        self.user = create_user()
        self.genre = create_genre(_user = self.user)
        self.label = create_label(_user = self.user)
        self.band = create_band(_user = self.user)
        self.record = create_record(_user = self.user, _bands = [self.band],
                                   _label = self.label, _genres = [self.genre])

    def test_basic_properties(self):
        """
        Test if fields are properly filled
        """
        self.ownedrecord = create_ownedrecord(_user = self.user,
                                              _record = self.record)
        self.assertEqual(self.ownedrecord.disc_type, 'cd')
        self.assertEqual(self.ownedrecord.user_fk, self.user)

    def test_get_recent_records_when_not_authorized(self):
        """
        Should return empty list
        """
        #self.ownedrecord = create_ownedrecord(_user = self.user,
        #                                     _record = self.record)
        #self.assertEqual(self.ownedrecord.get_recent_records(self.user), [])

    def test_get_recent_records_when_no_records(self):
        """
        Should return empty list
        """
        self.ownedrecord = create_ownedrecord(_user = self.user,
                                             _record = self.record)
        self.u2 = create_user(_username = 'u2')

        self.assertEqual(self.ownedrecord.get_recent_records(self.u2).count(),
                        0)

    def test_get_recent_records_with_from_past_and_future(self):
        """
        Should return a list of records bought in the past
        """
        self.ownedrecord = create_ownedrecord(_user = self.user,
                                             _record = self.record)
        self.ownedrecord2 = create_ownedrecord(_user = self.user,
                                             _record = self.record,
                                            _purchase_date = timezone.now() +
                                                datetime.timedelta(days = 1))

        self.assertEqual(self.ownedrecord.get_recent_records(self.user).count()
                         , 1)



class ReviewModelTests(TestCase):
    """
    Test for Review model
    """
    def setUp(self):
        self.user = create_user()
        self.genre = create_genre(_user = self.user)
        self.label = create_label(_user = self.user)
        self.band = create_band(_user = self.user)
        self.record = create_record(_user = self.user, _bands = [self.band],
                                   _label = self.label, _genres = [self.genre])

    def test_basic_properties(self):
        """
        Test if fields are properly filled
        """
        self.review = create_review(_user = self.user, _record = self.record)
        self.assertEqual(self.review.review_text, 'TestReview')
        self.assertEqual(self.review.record_fk, self.record)


##-----------------------View Tests



class RecordListViewTests(TestCase):
    """
    Tests for RecordList view
    """
    def setUp(self):
        self.user = create_user()
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




