from django import forms
from .models import Rating, Genre
from django.utils import timezone


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rate', 'review')


class FilterMovieForm(forms.Form):
    filter_rate = forms.DecimalField(
            min_value=0,
            max_value=5,
            decimal_places=1,
            max_digits=2,
            required=False,
            label='Movies with the rate greater than:',
            widget=forms.TextInput(attrs={'placeholder': 'Between(0-5) Ex. 3.8'}))
    genre = forms.ChoiceField(required=False)
    release_year = forms.ChoiceField(
            choices= [('', 'All Years')] + [(i, i) for i in range(1950, timezone.now().year + 1)],
            required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['genre'].choices =  [('', 'All Genres')] + [(g.id, g.title) for g in Genre.objects.all()]
        except:
            self.fields['genre'] = []