from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('movielist/', views.movielist, name='movielist'),
    path('moviedetail/<pk>/', views.moviedetail, name='moviedetail'),
    path('artistlist/', views.artistlist, name='artistlist'),
    path('artistdetail/<pk>/', views.artistdetail, name='artistdetail'),
    ## ACTION
    path('likemovie/', views.likeMovie, name='likemovie'),
    path('addtowatched/', views.addToWatched, name='addtowatched'),
    path('addtowatchlist/', views.addToWatchlist, name='addtowatchlist'),
    path('postcomment/', views.postComment, name='postcomment'),
    ## AUTH
    path('accounts/', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
