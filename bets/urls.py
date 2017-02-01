from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^u/$', views.UserRedirect.as_view() ),
    url( r'^u/(\w+)/$', views.Profile.as_view() ),
    url( r'^bet/$', views.bet_list, name='bet_list' ),
    
]
