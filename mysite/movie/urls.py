from rest_framework import routers
from .views import *
from django.urls import path,include

router = routers.SimpleRouter()
router.register(r'user', ProfileViewSet, basename='user')
router.register(r'director', DirectorViewSet, basename='director')
router.register(r'director_detail', DirectorDetailViewSet, basename='director_detail')
router.register(r'actor', ActorViewSet, basename='actor')
router.register(r'favorite', FavoriteViewSet, basename='favorite')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'rating', RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('movie/', MovieListApiView.as_view(), name = 'movie_list'),
    path('movie/<int:pk>/', MovieDetailApiView.as_view(), name = 'movie_detail'),
]