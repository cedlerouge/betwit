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
from django.contrib.sitemaps.views import sitemap
from bets.views import UserProfile
from betwit.views import HomeView, Index, Rules, Apropos, Players
from django.conf.urls.static import static
from django.conf import settings
from andablog.sitemaps import EntrySitemap
from betwit.sitemaps import BetwitSitemap #, TournamentSitemap, TeamSitemap, MatchSitemap, TeamMatchPointSitemap, MatchPointSitemap

sitemaps = {
    'betwit': BetwitSitemap(),
    'blog': EntrySitemap(),
    # 'tournament': TournamentSitemap(),
    # 'team': TeamSitemap(),
    # 'match': MatchSitemap(),
    # 'team': TeamMatchPointSitemap(),
    # 'match': MatchPointSitemap(),
}


urlpatterns = [
    url( r'^$', HomeView.as_view(), name="home" ),
    url( r'^admin/', admin.site.urls ),
    url( r'^rules/$', Rules.as_view(), name="rules" ),
    url( r'^apropos/$', Apropos.as_view(), name="apropos" ),
    url( r'^players/$', Players.as_view(), name="players" ),
    url( r'^tournaments/', include( 'tournaments.urls', namespace="tournaments" ) ),
    url( r'^accounts/', include( 'registration.backends.default.urls' ) ),
    url( r'^accounts/', include( 'django.contrib.auth.urls', namespace='auth' ) ),
    url( r'^settings/', UserProfile.as_view(), name="settings"),
    url( r'^settings/profile/', UserProfile.as_view(), name="settings_profile"),
    url( r'^reset/', include( 'django.contrib.auth.urls') ),
    ## andablog
    url( r'^blog/', include( 'andablog.urls', namespace="andablog") ),
    # for live preview
    url( r'^markitup/', include('markitup.urls')),
    ##
    ## newsletter
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    ##
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    #url( r'^accounts/.*', include( 'django.contrib.auth.urls', namespace='auth' ) ),
    # TODO bets and user page /bets/bets/user
    url( r'^bets/', include( 'bets.urls', namespace="bets" ) ),
    # google search console
    url(r'^googlexxxx\.html$', lambda r: HttpResponse("google-site-verification: googlexxxx.html", mimetype="text/plain")),
]
# use django to deliver image only on dev mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
