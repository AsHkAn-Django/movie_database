# movie_database

Just a quick little project I made while practicing Django and backend development.
This is part of my journey as I learn and improve my skills.

## About the Project

This project is built using Django and includes basic frontend styling with HTML, CSS, Bootstrap, and some JavaScript.
I usually focus on the backend side of things and try to keep things simple and clean.
Each project I make is a way for me to learn something new or reinforce what I already know.

## Features

- Filters for genres, ratings and release dates.
- Raiting and recommendation system.
- Trending movies.
- Serve the Media and Static on CloudFlare R2


## Technologies Used

- Python
- Django
- HTML
- CSS
- Bootstrap
- JavaScript

## About Me

Hi, I'm Ashkan — a junior Django developer who recently transitioned from teaching English as a second language to learning backend development.
I’m currently focused on improving my skills, building projects, and looking for opportunities to work as a backend developer.
You can find more of my work here: [My GitHub](https://github.com/AsHkAn-Django)
[Linkdin](in/ashkan-ahrari-146080150)

## How to Use

1. Clone the repository
   `git clone https://github.com/AsHkAn-Django/movie_database.git`
2. Navigate into the folder
   `cd movie_database`
3. Create a virtual environment and activate it
   `python -m venv .venv`
   `source .venv/bin/activate  # Or .venv\Scripts\activate  on Windows`
4. Install the dependencies
   `pip install -r requirements.txt`
5. Run the server
   `python manage.py migrate`
   `python manage.py createsuperuser`
   `python manage.py runserver`

## Tutorial
If you wanna know how I served the media and static files check my medium account [How to serve StaticFiles & Media on Cloudflare R2 (Django)](https://medium.com/@ashkan.ahrari/how-to-serve-staticfiles-and-media-on-cloudflare-r2-storage-in-a-django-project-b09932382a4f)


#### Form
Our ```FilterMovieForm``` is like this:
```python
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
```




