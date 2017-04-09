from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from music.models import Band, Record, Track, OwnedRecord, Genre, Label, Review
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from music.forms import ContactForm, ReviewForm
from django.core.mail import send_mail



def add_review(request, rec_id):
    record = Record.objects.get(id=rec_id)
    reviews= Record.objects.get(pk=rec_id).review_set.\
            order_by('-modify_date')[0:10]

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.create_by = request.user
            review.modify_by = request.user
            review.hidden = False
            review.like_counter = 0;
            review.record_fk = record
            review.save()
            return redirect('music:record', pk=record.id)
    else:
        form = ReviewForm()

    context = {'form':form, 'record':record, 'reviews':reviews}

    return render(request, 'music/add_review.html', context)



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(cd['subject'],
                      cd['message'],
                      (cd['email']),
                      ('srampampam@gmail.com',))
            return HttpResponseRedirect('/music/')
    else:
        form = ContactForm()
    return render(request, 'music/contact_form.html', {'form':form})



class LabelView(generic.DetailView):
    model = Label
    template_name = 'music/label.html'

    def get_context_data(self, **kwargs):
        context = super(LabelView, self).get_context_data(**kwargs)
        context['label_records'] = Label.objects.get(pk=self.kwargs.get('pk')).record_set.all()[0:10]
        return context






class RecordListView(generic.ListView):
    template_name = 'music/record_list.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        paginator = Paginator(Record.objects.all().order_by('title'), 15)
        page = self.kwargs['page_nb']
        try:
            context['objects'] = paginator.page(page)
        except PageNotAnInteger:
            context['objects'] = paginator.page(1)
        except EmptyPage:
            context['objects'] = paginator.page(paginator.num_pages)

        context['object_type'] = 'Records'
        return context



class LabelListView(generic.ListView):
    template_name = 'music/label_list.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]

    def get_context_data(self, **kwargs):
        context = super(LabelListView, self).get_context_data(**kwargs)
        paginator = Paginator(Label.objects.all().order_by('name'), 15)
        page = self.kwargs['page_nb']
        try:
            context['objects'] = paginator.page(page)
        except PageNotAnInteger:
            context['objects'] = paginator.page(1)
        except EmptyPage:
            context['objects'] = paginator.page(paginator.num_pages)

        context['object_type'] = 'Labels'
        return context



class GenreListView(generic.ListView):
    template_name = 'music/genre_list.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]


    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        paginator = Paginator(Genre.objects.all().order_by('name'), 15)
        page = self.kwargs['page_nb']
        try:
            context['objects'] = paginator.page(page)
        except PageNotAnInteger:
            context['objects'] = paginator.page(1)
        except EmptyPage:
            context['objects'] = paginator.page(paginator.num_pages)

        context['object_type'] = 'Genres'
        return context



class BandListView(generic.ListView):
    template_name = 'music/band_list.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]


    def get_context_data(self, **kwargs):
        context = super(BandListView, self).get_context_data(**kwargs)
        paginator = Paginator(Band.objects.all().order_by('name'), 15)
        page = self.kwargs['page_nb']
        try:
            context['objects'] = paginator.page(page)
        except PageNotAnInteger:
            context['objects'] = paginator.page(1)
        except EmptyPage:
            context['objects'] = paginator.page(paginator.num_pages)

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
        band_records= []
        r = Record.objects.get(pk=self.kwargs.get('pk'))
        for band in r.bands.all():
            for rec in band.record_set.all().exclude(id=r.id):
                band_records.append(rec)
        context['reviews'] = Record.objects.get(pk=self.kwargs.get('pk')).review_set.order_by('-modify_date')[0:10]
        context['band_records'] = band_records
        return context

class GenreView(generic.DetailView):
    model = Genre
    template_name = 'music/genre.html'

    def get_context_data(self, **kwargs):
        context = super(GenreView, self).get_context_data(**kwargs)
        context['genre_records'] = Genre.objects.get(pk=self.kwargs.get('pk')).record_set.all()[0:10]
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
