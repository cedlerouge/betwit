"""betwit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from bets.views import Index, Rules, Apropos, UserProfile
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url( r'^$', Index.as_view(), name="home" ),
    url( r'^admin/', admin.site.urls ),
    url( r'^rules/$', Rules.as_view(), name="rules" ),
    url( r'^apropos/$', Apropos.as_view(), name="apropos" ),
    url( r'^tournaments/', include( 'tournaments.urls', namespace="tournaments" ) ),
    url( r'^accounts/', include( 'registration.backends.default.urls' ) ),
    url( r'^accounts/', include( 'django.contrib.auth.urls', namespace='auth' ) ),
    url( r'^settings/', UserProfile.as_view(), name="settings"),
    url( r'^settings/profile/', UserProfile.as_view(), name="settings_profile"),
    url( r'^reset/', include( 'django.contrib.auth.urls') ),

    #url( r'^accounts/.*', include( 'django.contrib.auth.urls', namespace='auth' ) ),
    # TODO bets and user page /bets/bets/user
    url( r'^bets/', include( 'bets.urls', namespace="bets" ) ),
]
# use django to deliver image only on dev mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
