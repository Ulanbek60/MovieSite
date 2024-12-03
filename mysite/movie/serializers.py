from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'age', 'phone_number', 'status',
        ]
    extra_kwargs = {'passwords': {'write only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user':{
                'username':instance.username,
                'email':instance.email,
            },
            'access':str(refresh.access_token),
            'refresh':str(refresh),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name']


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name', 'bio', 'age', 'director_image']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']

class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'stars', 'text', 'parent', 'created_date']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']


class MovieImageSerializer(models.Model):
    movie = models.ForeignKey(Moments, on_delete= models.CASCADE)
    image = models.ImageField(upload_to='movie_images/')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user']


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ['id', 'cart', 'movie']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'user', 'movie']


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format('%d-%m-%Y'))
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'genre', 'year', 'country', 'status_movie']


class MovieDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    country = CountrySerializer(many=True)
    director = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    year = serializers.DateField(format='%d-%m-%Y')
    movie_trailer = serializers.FileField()
    videos = MovieLanguagesSerializer(many=True, read_only=True)
    # movie_review = RatingSerializer(many=True)
    moments = MomentsSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['movie_name', 'year', 'country', 'director', 'actors', 'genre', 'types',
                  'movie_time', 'movie_image', 'movie_trailer',
                  'status_movie','description', 'videos', 'moments','status_movie']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor_films = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['actor_name', 'bio', 'age', 'actor_image', 'actor_films']

