from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Band, Record, Track, OwnedRecord
from django.views import generic
from django.utils import timezone

# Create your views here.

class BandListView(generic.ListView):
    template_name = 'music/band_list.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]

    def get_context_data(self, **kwargs):
        context = super(BandListView, self).get_context_data(**kwargs)
        context['objects'] = Band.objects.all().order_by('name')
        context['object_type'] = 'Bands'
        return context


class IndexView(generic.ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['records'] = Record.objects.all()[:10]
        context['ordered_bands'] = Band.objects.order_by('name')[:15]
        return context

class BandView(generic.DetailView):
    model = Band
    template_name = 'music/band.html'

class RecordView(generic.DetailView):
    model = Record
    template_name = 'music/record.html'

    def get_context_data(self, **kwargs):
        context = super(RecordView, self).get_context_data(**kwargs)
        context['tracks'] = Track.objects.filter(
            record_fk = self.kwargs.get('pk'))
        band_id = Record.objects.get(pk=self.kwargs.get('pk')).band_fk.id
        context['band_records'] = Record.objects.filter(band_fk=band_id).exclude(id = self.kwargs.get('pk'))
        return context

class UserPanelView(generic.ListView):
    model = OwnedRecord
    template_name = 'music/userPanel.html'

    def get_context_data(self, **kwargs):
        context = super(UserPanelView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['recent_records'] = OwnedRecord.objects.filter(purchase_date__lte=timezone.now()).filter(user_fk = self.request.user)
        else:
            context['recent_records'] = []
        return context
