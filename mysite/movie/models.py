from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
)

class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(70)],
                                           null=True, blank=True)
    phone_number= PhoneNumberField(null=True, blank=True, region='KG')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name}-{self.last_name}-{self.status}'


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=32, unique=True)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                           validators=[MaxValueValidator(90)])
    director_image = models.ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name

class Actor(models.Model):
    actor_name = models.CharField(max_length=32, unique=True)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                           validators=[MinValueValidator(15), MaxValueValidator(90)])
    actor_image = models.ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    TYPES_CHOICES = (
        ('144', '144p'),
        ('360', '360p'),
        ('480', '480p'),
        ('720', '720p'),
        ('1080', '1080p')
    )
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor, related_name='actor_films')
    genre = models.ManyToManyField(Genre)
    types = MultiSelectField(max_length=16, choices=TYPES_CHOICES, max_choices=5)
    movie_time = models.PositiveSmallIntegerField(default=0)
    movie_image = models.ImageField(upload_to='movie_poster/', verbose_name='фото')
    movie_trailer = models.FileField(upload_to='movie_trailer/', verbose_name='видео')
    status_movie = models.CharField(max_length=16, choices=STATUS_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.movie_name


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32, unique=True)
    video = models.FileField(upload_to='videos/', verbose_name='фильм')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.language


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moments')
    movie_moments = models.ImageField(upload_to='movie_moments/')

    def __str__(self):
        return str(self.movie)



class Rating(models.Model):
    user_review = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], verbose_name='рейтинг', null=True, blank=True)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_review} - {self.movie}'


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} - {self.movie}'


