
from django.core.management.base import BaseCommand
from tournaments.models import Tournament, Match, Team

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Populates tournament application with teams and matchs'

    def _create_tournament(self):

        t1 = Tournament(
            name="6 nations",
            year=2018,
            begins="2018-02-03",
            state="1")
        t1.save()
        anglais = Team(
            name = 'Angleterre',
            nationality = 'Anglais',
            logo = 'photo/23px-Flag_of_England.svg.png',
            flag = 'photo/england_logo.png')
        anglais.save()
        francais = Team(
            name = 'France',
            nationality = 'francais',
            logo = 'photo/23px-Flag_of_France.svg.png',
            flag = 'photo/france_logo.png')
        francais.save()
        ecossais = Team(
            name = 'Ecosse',
            nationality = 'Ecossais',
            logo = 'photo/23px-Flag_of_Scotland.svg.png',
            flag = 'photo/scotland_logo.png')
        ecossais.save()
        gallois = Team(
            name = 'Pays de Galles',
            nationality = 'Gallois',
            logo = 'photo/23px-Flag_of_Wales_2.svg.png',
            flag = 'photo/wales_logo.png')
        gallois.save()
        italien = Team(
            name = 'Italie',
            nationality = 'Italien',
            logo = 'photo/23px-Flag_of_Italy.svg.png',
            flag = 'photo/italy_logo.png')
        italien.save()
        irlandais = Team(
            name = 'Irlande',
            nationality = 'Irlandais',
            logo = 'photo/23px-Flag_of_Irelande.svg.png',
            flag = 'photo/ireland_logo.png')
        irlandais.save()
        
        matchj11 = Match(
            tournament = Tournament.objects.first(),
            date = "2018-02-02 14:50",
            cup_round = "1",
            home_team = Team.objects.get(name="France"),
            away_team = Team.objects.get(name="Irlande")
        )
        matchj11.save()

    def handle(self, *args, **options):
        self._create_tournament()

