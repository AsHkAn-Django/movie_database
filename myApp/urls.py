from django.urls import path
from . import views

app_name = 'myApp'
urlpatterns = [
    path('rating/<int:pk>', views.RateView.as_view(), name='rating'),
    path('movies-list/', views.MoviesListView.as_view(), name='movies_list'),
    path('trends/', views.TrendingMoviesListView.as_view(), name='trends'),
    path('', views.IndexView.as_view(), name='home'),
]