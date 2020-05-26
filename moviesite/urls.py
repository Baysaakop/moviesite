from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from movies.views import views
from movies.views import movieactionviews
from movies.views import adminviews
from movies.views import searchviews
from movies.views import artistactionviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns (
    path('', views.home, name='home'),
    path('movielist/', views.movielist, name='movielist'),
    path('moviedetail/<pk>/', views.moviedetail, name='moviedetail'),
    path('artistlist/', views.artistlist, name='artistlist'),
    path('artistdetail/<pk>/', views.artistdetail, name='artistdetail'),
    ## MOVIE ACTIONS
    path('likemovie/', movieactionviews.likeMovie, name='likemovie'),
    path('addtowatched/', movieactionviews.addToWatched, name='addtowatched'),
    path('addtowatchlist/', movieactionviews.addToWatchlist, name='addtowatchlist'),
    path('ratemovie/', movieactionviews.rateMovie, name='ratemovie'),
    path('postcomment/', movieactionviews.postComment, name='postcomment'),
    path('commentlike/', movieactionviews.commentLike, name='commentlike'),
    path('commentdislike/', movieactionviews.commentDislike, name='commentdislike'),
    ## ARTIST ACTIONS
    path('likeartist/', artistactionviews.likeArtist, name='likeartist'),
    path('followartist/', artistactionviews.followArtist, name='followartist'),
    ## ADMIN ACTIONS
    path('movieadd/', adminviews.movieadd, name='movieadd'),
    path('movieedit/', adminviews.movieedit, name='movieedit'),    
    path('moviedelete/', adminviews.moviedelete, name='moviedelete'),   
    path('artistadd/', adminviews.artistadd, name='artistadd'),
    path('artistedit/', adminviews.artistedit, name='artistedit'),
    path('artistdelete/', adminviews.artistdelete, name='artistdelete'), 
    ## SEARCH ACTIONS
    path('searchmovie/', searchviews.searchmovie, name='searchmovie'),
    path('searchartist/', searchviews.searchartist, name='searchartist'),    
    path('searchdirector/', searchviews.searchdirector, name='searchdirector'),
    path('searchactor/', searchviews.searchactor, name='searchactor'),
    path('getmoviebyid/', searchviews.getmoviebyid, name='getmoviebyid'),
    path('getartistbyid/', searchviews.getartistbyid, name='getartistbyid'),
    ## AUTH
    path('accounts/', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),    
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
