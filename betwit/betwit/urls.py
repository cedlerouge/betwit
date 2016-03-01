"""betwit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, patterns, include
from django.contrib import admin, auth
from bets.views import Index, Profile, PostBet, UserRedirect, PostBetCup, BetRanking, BetRules, BetPrognosis, Logout
from matchs.views import Results
import django.contrib.auth.views

admin.autodiscover()

urlpatterns = [
    url(r'^$', Results.as_view(), name="home"),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^user/(\w+)/postbet/$', PostBet.as_view()),
    url(r'^user/(\w+)/postbetcup/$', PostBetCup.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth.views.login),
    url(r'^logout/$', Logout.as_view()),
    url(r'^profile/$', UserRedirect.as_view()),
    url(r'^ranking/$', BetRanking.as_view()),
    url(r'^prognosis/$', BetPrognosis.as_view()),
    url(r'^rules/$', BetRules.as_view())
]
