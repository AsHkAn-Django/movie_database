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
The ```FilterMovieForm``` is like this:
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
            # Adding all years with an empty string for not querring and showing all the years
            choices= [('', 'All Years')] + [(i, i) for i in range(1950, timezone.now().year + 1)],
            required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['genre'].choices =  [('', 'All Genres')] + [(g.id, g.title) for g in Genre.objects.all()]
        except:
            self.fields['genre'] = []
```

#### Recommendation
The Recommendation system is base on ```surprise``` package which you can see the [full tutorial here](https://medium.com/@ashkan.ahrari/how-to-implement-a-recommendation-system-in-django-e-commerce-using-the-surprise-package-7ca80f856484)
```python
import pandas as pd
from surprise import Dataset, Reader, SVD
from .models import Rating


def get_top_n_recommendations(user_id, n=5):
    # 1. Fetch data from Django model
    ratings_qs = Rating.objects.all().values('user_id', 'movie_id', 'rate')
    ratings_df = pd.DataFrame.from_records(ratings_qs)

    # 2. Check if DataFrame is valid
    required_columns = {'user_id', 'movie_id', 'rate'}
    if ratings_df.empty or not required_columns.issubset(set(ratings_df.columns)):
        return []

    # 3. Define the data format for Surprise
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rate']], reader)

    # 4. Train the model
    trainset = data.build_full_trainset()
    model = SVD()
    model.fit(trainset)

    # 5. Get all movie IDs
    all_movie_ids = ratings_df['movie_id'].unique()

    # 6. Get movies this user already rated
    rated_movies = ratings_df[ratings_df['user_id'] == user_id]['movie_id'].tolist()

    # 7. Filter out already rated movies
    movies_to_predict = [bid for bid in all_movie_ids if bid not in rated_movies]
    # 8. Predict ratings for the unseen movies
    predictions = [model.predict(user_id, bid) for bid in movies_to_predict]

    # 9. Sort and return top n recommendations
    top_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]

    # Get Movie IDs from the top predictions
    top_movie_ids = [int(pred.iid) for pred in top_predictions]

    return top_movie_ids
```
#### Filter Movies
In Here with the help of filter form we check if there is any chosen field for filter form then we query base on that
```python
class MoviesListView(generic.ListView):
    model = Movie
    template_name = "myApp/movies_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FilterMovieForm(self.request.GET)
        context['form'] = form
        # First we add the ratingfield to out data so if there is any filter rating we can use it
        movies = Movie.objects.annotate(
                    rating=Round(Avg('ratings__rate'), 1, output_field=FloatField()))
        if form.is_valid():
            rate = self.request.GET.get('filter_rate', None)
            if rate:
                movies = movies.filter(rating__gte=rate)
            genre = self.request.GET.get('genre', None)
            if genre:
                movies = movies.filter(genre_id=genre)
            release_year = self.request.GET.get('release_year', None)
            if release_year:
                movies = movies.filter(release_year__gte=release_year)
        context['movies'] = movies
        return context
```


