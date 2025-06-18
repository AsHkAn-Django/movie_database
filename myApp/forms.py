from django import forms
from .models import Rating
from django.core.validators import MinValueValidator, MaxValueValidator



class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rate', 'review')
        
        
class FilterMovieForm(forms.Form):
    filter_rate = forms.DecimalField(
        validators=[MaxValueValidator(5), MinValueValidator(0)],         
        decimal_places=1,
        max_digits=2,
        required=False)   
       
    # This is how we change the lable or placeholder for a field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filter_rate'].label = 'Movies with the rate greater than:'
        self.fields['filter_rate'].widget.attrs['placeholder'] = 'Between(0-5) Ex. 3.8'
    
