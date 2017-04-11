from django import forms
from music.models import Review


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_text', 'score')

    def clean_score(self):
        score = int(self.cleaned_data['score'])

        if 0 <= score <=5:
            return score
        else:
            raise forms.ValidationError('Score must be between 0 and 5')
