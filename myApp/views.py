from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Rating, Movie, Genre
from .forms import RatingForm, FilterMovieForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import FloatField, Avg, Count
from django.db.models.functions import Round
from .recommend import get_top_n_recommendations



class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            recommend_ids = get_top_n_recommendations(self.request.user.id, 3)
            if recommend_ids:
                context['recommends'] = Movie.objects.filter(id__in=recommend_ids)
        return context




class TrendingMoviesListView(generic.ListView):
    template_name = "myApp/trends.html"
    context_object_name = 'trends'

    def get_queryset(self):
        queryset = Movie.objects.annotate(avg_rating=Avg('ratings__rate'), num_votes=Count('ratings')
                                          ).filter(num_votes__gte=5).order_by('-avg_rating')[:10]
        return queryset




class MoviesListView(generic.ListView):
    model = Movie
    template_name = "myApp/movies_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = FilterMovieForm(self.request.GET)
        context['form'] = form

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



class RateView(LoginRequiredMixin, generic.CreateView):
    model = Rating
    form_class = RatingForm
    template_name = "myApp/rating.html"

    def get_context_data(self, **kwargs):
        """Just to show the name of the movie at top of the page:)"""
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('pk')
        movie = get_object_or_404(Movie, pk=movie_id)
        context['movie'] = movie
        return context

    def form_valid(self, form):
        """Prevent rate duplication and refresh the average rate filed."""
        movie_id = self.kwargs.get('pk')
        movie = get_object_or_404(Movie, pk=movie_id)
        # Check if the user rated this movie before delete it.
        rating_exists = Rating.objects.filter(movie_id=movie_id, user_id=self.request.user.id)
        if rating_exists:
            rating_exists.delete()
        form.instance.user = self.request.user
        form.instance.movie = movie
        form.save()
        messages.success(self.request, "Rating added successfully!")
        # Update the average_rating field.
        movie.get_average_rating()
        return redirect('myApp:home')

    # TODO: Or a better form_valid:
    # def form_valid(self, form):
    # movie_id = self.kwargs.get('pk')
    # movie = get_object_or_404(Movie, pk=movie_id)

    # # Update if exists, or create a new entry
    # rating, created = Rating.objects.update_or_create(
    #     movie=movie, user=self.request.user,
    #     defaults={'rate': form.cleaned_data['rate']}
    # )
    # if created:
    #     messages.success(self.request, "Rating added successfully!")
    # else:
    #     messages.success(self.request, "Rating updated successfully!")
    # return redirect('myApp:home')
