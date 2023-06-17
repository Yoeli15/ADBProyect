from django.urls import path
from movies.views import MovieView, ConfigureMovieView

urlpatterns =[
    path('movies/', MovieView.as_view()),
    path('configure_movies/', ConfigureMovieView.as_view())
]