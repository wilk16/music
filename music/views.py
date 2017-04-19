from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from music.models import Band, Record, Track, OwnedRecord, Genre, Label, Review
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from music.forms import ContactForm, ReviewForm
from django.core.mail import send_mail
from django.db.models import Avg


def delete_review(request, review_id):
    """
    View for deleting reviews
    """
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.create_by:
        return HttpResponseForbidden()
    record = review.record_fk
    if request.method == "POST":
        review.delete()
        return redirect('music:record', pk=record.id)

    context = {'record':record, 'review':review}

    return render(request, 'music/delete_review.html', context)


def edit_review(request, review_id):
    """
    View for editing reviews
    """
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.create_by:
        return HttpResponseForbidden()
    record = review.record_fk
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect('music:record', pk=review.record_fk_id)
    else:
        form = ReviewForm(instance=review)
    context = {'form':form, 'record':record, 'review':review}

    return render(request, 'music/edit_review.html', context)


def add_review(request, rec_id):
    """
    View for adding reviews
    """
    record = Record.objects.get(id=rec_id)
    reviews= Record.objects.get(pk=rec_id).review_set.\
            order_by('-modify_date')[0:10]

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            review = form.save(commit=False)
            review.score = cd['score']
            review.create_by = request.user
            review.modify_by = request.user
            review.hidden = False
            review.like_counter = 0;
            review.record_fk = record
            review.save()
            return redirect('music:record', pk=record.id)
        else:
            form = ReviewForm()
    else:
        form = ReviewForm()

    context = {'form':form, 'record':record, 'reviews':reviews}

    return render(request, 'music/add_review.html', context)


def contact(request):
    """
    View for sending contact messages
    """
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
    """
    View for displaying label details
    """
    model = Label
    template_name = 'music/label.html'


class RecordListView(generic.ListView):
    """
    View for displaying list of Records
    """

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
        return context


class LabelListView(generic.ListView):
    """
    View for displaying list of Labels
    """

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

        return context


class GenreListView(generic.ListView):
    """
    View for displaying list of genre
    """


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

        return context


class BandListView(generic.ListView):
    """
    view for displaying list of bands
    """

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
        return context


class IndexView(generic.ListView):
    """
    View for displaying home page.
    """
    template_name = 'music/index.html'

    def get_queryset(self):
        """
        It seems that I must have a get_queryset method...
        """
        return [1]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['records'] = Record.objects.all()[:10]
        context['ordered_bands'] = Band.objects.order_by('name')[:15]
        return context


class BandView(generic.DetailView):
    """
    View for displaying band details
    """

    model = Band
    template_name = 'music/band.html'


class RecordView(generic.DetailView):
    """
    View for displaying record details
    """

    model = Record
    template_name = 'music/record.html'

    def get_context_data(self, **kwargs):
        context = super(RecordView, self).get_context_data(**kwargs)
        context['related_reviews'] = self.get_object().get_related_reviews\
                    (self.request.user)
        context['user_review'] = self.get_object().get_user_review\
                (self.request.user)
        return context


class GenreView(generic.DetailView):
    """
    View for displaying genre details
    """

    model = Genre
    template_name = 'music/genre.html'



class UserPanelView(generic.ListView):
    """
    View for displaying user's site
    """

    model = OwnedRecord
    template_name = 'music/userPanel.html'

    def get_context_data(self, **kwargs):
        context = super(UserPanelView, self).get_context_data(**kwargs)
        #context['recent_records'] = OwnedRecord.get_recent_records(self.request.user)

        return context

