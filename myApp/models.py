from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.text import slugify
import os



class Genre(models.Model):
    title = models.CharField(max_length=164)

    def __str__(self):
        return self.title


def movie_image_upload_path(instance, filename):
    title_slug = slugify(instance.title)
    return os.path.join('uploads', title_slug, filename)


class Movie(models.Model):
    title = models.CharField(max_length=164)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    release_year = models.IntegerField(validators=[MaxValueValidator(2050), MinValueValidator(1950)])
    image = models.ImageField(upload_to=movie_image_upload_path, blank=True)

    def get_average_rating(self):
        '''Get the average rating for this movie.'''
        ratings = self.ratings.all()
        if not ratings:
            return Decimal('0.0')
        else:
            total = sum(rating.rate for rating in ratings)
        return Decimal(round(total / len(ratings), 1))

    def get_rates_number(self):
        return len(self.ratings.all())

    def __str__(self):
        return self.title


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.DecimalField(
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        decimal_places=1,
        max_digits=2)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # We don't want a user gives more than one rate to a movie
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='unique_movie_user_rating')
        ]

    def __str__(self):
        return f"{self.user.username} rate {self.rate} for {self.movie.title}"


