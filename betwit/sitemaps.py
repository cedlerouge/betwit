
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
#from betwit.urls import urlpatterns as betwitUrls
from tournaments.models import Tournament, Team, Match, MatchPoint, TeamMatchPoint

class BetwitSitemap(Sitemap):
     priority = 0.8
     changefreq = 'weekly'

     # The below method returns all urls defined in urls.py file
     def items(self):
        staticUrls = [
            'home',
            'rules',
            'apropos',
            #'tournaments_list',
            #'bets_list',
          ]
        #for url in betwitUrls:
        #    mylist.append('betwit:'+url.name) 
        return staticUrls

     def location(self, item):
         return reverse(item)

# class TournamentSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.7

#     def items(self):
#         return Tournament.Objects.filter(state=1)
    
#     def lastmod(self, item):
#         return item.modifiedDate

# class TeamSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.7

#     def items(self):
#         return Team.Objects.get()
    
#     def lastmod(self, item):
#         return item.modifiedDate

# class MatchSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.7

#     def items(self):
#         return Match.Objects.get()
    
#     def lastmod(self, item):
#         return item.modifiedDate

# class TeamMatchPointSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.7

#     def items(self):
#         return Team.Objects.get()
    
#     def lastmod(self, item):
#         return item.modifiedDate

# class MatchPointSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.7

#     def items(self):
#         return Match.Objects.get()
    
#     def lastmod(self, item):
#         return item.modifiedDate

