from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^login/$',views.login, name='login'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^auth/$',views.auth, name='auth'),
    url(r'^(\w+)/vote$', views.vote, name='vote'),
    url(r'^(\w+)/submit-vote$', views.submit_vote, name='submit_vote'),
    url(r'^(\w+)/call-vote$', views.call_vote, name='call_vote'),
]
