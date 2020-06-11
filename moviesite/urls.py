from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from movies.views import views
from movies.views import actionviews
from movies.views import crudviews
from movies.views import searchviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns (
    path('', views.home, name='home'),
    ## ACTIONS
    path('movieaddfavorite/', actionviews.movieaddfavorite, name='movieaddfavorite'),
    path('movieaddwatched/', actionviews.movieaddwatched, name='movieaddwatched'),
    path('movieaddwatchlist/', actionviews.movieaddwatchlist, name='movieaddwatchlist'),
    path('moviegiverating/', actionviews.moviegiverating, name='moviegiverating'),
    path('seriesaddfavorite/', actionviews.seriesaddfavorite, name='seriesaddfavorite'),
    path('seriesaddwatched/', actionviews.seriesaddwatched, name='seriesaddwatched'),
    path('seriesaddwatchlist/', actionviews.seriesaddwatchlist, name='seriesaddwatchlist'),
    path('seriesgiverating/', actionviews.seriesgiverating, name='seriesgiverating'),
    path('artistaddfavorite/', actionviews.artistaddfavorite, name='artistaddfavorite'),
    path('artistaddfollowed/', actionviews.artistaddfollowed, name='artistaddfollowed'),
    path('artistgiverating/', actionviews.artistgiverating, name='artistgiverating'),
    # path('postcomment/', movieactionviews.postComment, name='postcomment'),
    # path('commentlike/', movieactionviews.commentLike, name='commentlike'),
    # path('commentdislike/', movieactionviews.commentDislike, name='commentdislike'),
    ## SEARCH ACTIONS
    path('searchmovie/', searchviews.searchmovie, name='searchmovie'),
    path('searchartist/', searchviews.searchartist, name='searchartist'),    
    path('searchproducer/', searchviews.searchproducer, name='searchproducer'),
    path('searchdirector/', searchviews.searchdirector, name='searchdirector'),
    path('searchwriter/', searchviews.searchwriter, name='searchwriter'),
    path('searchactor/', searchviews.searchactor, name='searchactor'),
    path('searchproduction/', searchviews.searchproduction, name='searchproduction'),
    path('getmoviebyid/', searchviews.getmoviebyid, name='getmoviebyid'),
    path('getartistbyid/', searchviews.getartistbyid, name='getartistbyid'),
    path('getproductionbyid/', searchviews.getproductionbyid, name='getproductionbyid'),
    ## SERIES VIEWS
    path('serieslist/', crudviews.SeriesListView.as_view(), name='serieslist'),
    path('seriesdetail/<pk>/', crudviews.SeriesDetailView.as_view(), name='seriesdetail'),
    path('seriescreate/', crudviews.SeriesCreateView.as_view(), name='seriescreate'),
    path('seriesupdate/<pk>/', crudviews.SeriesUpdateView.as_view(), name='seriesupdate'),
    path('seriesdelete/<pk>/', crudviews.SeriesDeleteView.as_view(), name='seriesdelete'),
    path('seriescastedit/<pk>/', crudviews.SeriesCastEdit, name='seriescastedit'),
    ## MOVIE VIEWS
    path('movielist/', crudviews.MovieListView.as_view(), name='movielist'),
    path('moviedetail/<pk>/', crudviews.MovieDetailView.as_view(), name='moviedetail'),
    path('moviecreate/', crudviews.MovieCreateView.as_view(), name='moviecreate'),
    path('movieupdate/<pk>/', crudviews.MovieUpdateView.as_view(), name='movieupdate'),
    path('moviedelete/<pk>/', crudviews.MovieDeleteView.as_view(), name='moviedelete'),
    path('moviecastedit/<pk>/', crudviews.MovieCastEdit, name='moviecastedit'),
    ## ARTIST VIEWS
    path('artistlist/', crudviews.ArtistListView.as_view(), name='artistlist'),
    path('artistdetail/<pk>/', crudviews.ArtistDetailView.as_view(), name='artistdetail'),
    path('artistcreate/', crudviews.ArtistCreateView.as_view(), name='artistcreate'),
    path('artistupdate/<pk>/', crudviews.ArtistUpdateView.as_view(), name='artistupdate'),
    path('artistdelete/<pk>/', crudviews.ArtistDeleteView.as_view(), name='artistdelete'),
    ## AUTH
    path('accounts/', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),    
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
