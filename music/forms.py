from django import forms
from music.models import Review


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_text', )
        #widgets = {
        #    'review_text': Textarea(attrs={'colls':80, 'rows':20}),
        #}

