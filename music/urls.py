from django.conf.urls import url
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^band/(?P<slug>[-\w]+)/$', views.BandView.as_view(), name='band'),
        url(r'^record/(?P<slug>[-\w]+)/$', views.RecordView.as_view(),
            name='record'),
        url(r'^genre/(?P<slug>[-\w]+)/$', views.GenreView.as_view(), name='genre'),

        url(r'^label/(?P<slug>[-\w]+)/$', views.LabelView.as_view(), name='label'),
        url(r'^userPanel/$', views.UserPanelView.as_view(), name='userPanel'),

        url(r'^band_list/(?P<page_nb>[0-9]+)/$', views.BandListView.as_view(),
            name='band_list'),

        url(r'^label_list/(?P<page_nb>[0-9]+)/$', views.LabelListView.as_view(),
            name='label_list'),
        url(r'^genre_list/(?P<page_nb>[0-9]+)/$', views.GenreListView.as_view(),
            name='genre_list'),
        url(r'^record_list/(?P<page_nb>[0-9]+)/$', views.RecordListView.as_view(),
            name='record_list'),
        url(r'^contact/$', views.contact, name='contact'),
        url(r'^record/(?P<rec_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
        url(r'^edit_review/(?P<review_id>[0-9]+)/$', views.edit_review,
            name='edit_review'),
        url(r'^delete_review/(?P<review_id>[0-9]+)/$', views.delete_review,
            name='delete_review'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
