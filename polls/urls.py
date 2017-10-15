from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^login/$',views.login, name='login'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^auth/$',views.auth, name='auth'),
    url(r'^search$', views.search, name='search'),
    url(r'^voting$', views.voting, name='voting'),
    url(r'^search-results$', views.searchSong, name='searchSong')
]
