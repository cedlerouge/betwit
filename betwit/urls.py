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
from django.urls import path, re_path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from bets.views import UserProfile
from betwit.views import HomeView, Index, Rules, Cote, Apropos, Players
from django.conf.urls.static import static
from django.conf import settings
from betwit.sitemaps import BetwitSitemap #, TournamentSitemap, TeamSitemap, MatchSitemap, TeamMatchPointSitemap, MatchPointSitemap

#favicon 
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

sitemaps = {
    'betwit': BetwitSitemap(),
}


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('rules/', Rules.as_view(), name="rules"),
    path('cote/', Cote.as_view(), name="cote"),
    path('apropos/', Apropos.as_view(), name="apropos"),
    # path('players/', Players.as_view(), name="players"),
    path('tournaments/', include('tournaments.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('settings/', UserProfile.as_view(), name="settings"),
    path('settings/profile/', UserProfile.as_view(), name="settings_profile"),
    path('reset/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    # andablog disabled
    # path('blog/', include('andablog.urls')),
    # markitup disabled
    # path('markitup/', include('markitup.urls')),
    # newsletter
    path('newsletter/', include('newsletter.urls')),
    path('tinymce/', include('tinymce.urls')),
    # bets
    path('bets/', include('bets.urls')),
    path('api/', include('betwit.api_urls')),

    re_path(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')), name="favicon"),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    # google search console
    re_path(r'^google1df483f09eef1978\.html$', lambda r: HttpResponse("google-site-verification: google1df483f09eef1978.html", content_type="text/plain")),
    re_path(r'^BingSiteAuth\.xml$', lambda r: HttpResponse('<?xml version="1.0"?><users><user>DD087CD831FFD650179243A0BAA97B49</user></users>', content_type="application/xml")),
]
# use django to deliver image only on dev mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
