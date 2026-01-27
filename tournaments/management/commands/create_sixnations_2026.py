"""
Management command to create the Six Nations 2026 tournament and all its matches.

Usage:
    python manage.py create_sixnations_2026
    python manage.py create_sixnations_2026 --dry-run  # Preview without creating
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
import pytz

from tournaments.models import Team, Tournament, Match, TeamStat


class Command(BaseCommand):
    help = 'Create the Six Nations 2026 tournament with all matches'

    # Teams participating in Six Nations
    TEAMS = {
        'France': 'France',
        'Ireland': 'Ireland',
        'England': 'England',
        'Scotland': 'Scotland',
        'Wales': 'Wales',
        'Italy': 'Italy',
    }

    # Complete match schedule for Six Nations 2026
    # Format: (date, time_gmt, home_team, away_team, cup_round)
    MATCHES = [
        # Round 1
        ('2026-02-05', '20:10', 'France', 'Ireland', '1'),
        ('2026-02-07', '14:10', 'Italy', 'Scotland', '1'),
        ('2026-02-07', '16:40', 'England', 'Wales', '1'),
        # Round 2
        ('2026-02-14', '14:10', 'Ireland', 'Italy', '2'),
        ('2026-02-14', '16:40', 'Scotland', 'England', '2'),
        ('2026-02-15', '15:10', 'Wales', 'France', '2'),
        # Round 3
        ('2026-02-21', '14:10', 'England', 'Ireland', '3'),
        ('2026-02-21', '16:40', 'Wales', 'Scotland', '3'),
        ('2026-02-22', '15:10', 'France', 'Italy', '3'),
        # Round 4
        ('2026-03-06', '20:10', 'Ireland', 'Wales', '4'),
        ('2026-03-07', '14:10', 'Scotland', 'France', '4'),
        ('2026-03-07', '16:40', 'Italy', 'England', '4'),
        # Round 5 (Super Saturday)
        ('2026-03-14', '14:10', 'Ireland', 'Scotland', '5'),
        ('2026-03-14', '16:40', 'Wales', 'Italy', '5'),
        ('2026-03-14', '20:10', 'France', 'England', '5'),
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview what would be created without actually creating anything',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be created\n'))

        # Step 1: Create or get teams
        self.stdout.write(self.style.MIGRATE_HEADING('Step 1: Creating/Getting teams...'))
        teams = self._create_or_get_teams(dry_run)

        # Step 2: Create the tournament
        self.stdout.write(self.style.MIGRATE_HEADING('\nStep 2: Creating tournament...'))
        tournament = self._create_tournament(dry_run)

        # Step 3: Create all matches
        self.stdout.write(self.style.MIGRATE_HEADING('\nStep 3: Creating matches...'))
        matches = self._create_matches(tournament, teams, dry_run)

        # Step 4: Create TeamStat entries for each team
        self.stdout.write(self.style.MIGRATE_HEADING('\nStep 4: Creating team stats...'))
        self._create_team_stats(tournament, teams, dry_run)

        # Summary
        self.stdout.write('\n' + '=' * 60)
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN COMPLETE - No data was created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created Six Nations 2026!'))
            self.stdout.write(f'  - Tournament ID: {tournament.id if tournament else "N/A"}')
            self.stdout.write(f'  - Teams: {len(teams)}')
            self.stdout.write(f'  - Matches: {len(matches)}')

    def _create_or_get_teams(self, dry_run):
        """Create teams if they don't exist, or get existing ones."""
        teams = {}

        for team_name, nationality in self.TEAMS.items():
            if dry_run:
                team = Team.objects.filter(name=team_name).first()
                if team:
                    self.stdout.write(f'  [EXISTS] {team_name}')
                else:
                    self.stdout.write(f'  [WOULD CREATE] {team_name} ({nationality})')
                teams[team_name] = team
            else:
                team, created = Team.objects.get_or_create(
                    name=team_name,
                    defaults={'nationality': nationality}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  [CREATED] {team_name}'))
                else:
                    self.stdout.write(f'  [EXISTS] {team_name}')
                teams[team_name] = team

        return teams

    def _create_tournament(self, dry_run):
        """Create the Six Nations 2026 tournament."""
        tournament_name = 'Six Nations'
        year = 2026
        # Tournament begins with the first match
        begins = timezone.make_aware(
            datetime(2026, 2, 5, 20, 10, 0),
            timezone=pytz.UTC
        )

        existing = Tournament.objects.filter(name=tournament_name, year=year).first()

        if dry_run:
            if existing:
                self.stdout.write(f'  [EXISTS] {tournament_name} {year}')
                return existing
            else:
                self.stdout.write(f'  [WOULD CREATE] {tournament_name} {year}')
                return None
        else:
            if existing:
                self.stdout.write(f'  [EXISTS] {tournament_name} {year} (ID: {existing.id})')
                return existing

            tournament = Tournament.objects.create(
                name=tournament_name,
                year=year,
                begins=begins,
                state='2'  # Coming
            )
            self.stdout.write(self.style.SUCCESS(
                f'  [CREATED] {tournament_name} {year} (ID: {tournament.id})'
            ))
            return tournament

    def _create_matches(self, tournament, teams, dry_run):
        """Create all matches for the tournament."""
        matches = []

        for date_str, time_str, home_name, away_name, cup_round in self.MATCHES:
            # Parse date and time
            hour, minute = map(int, time_str.split(':'))
            year, month, day = map(int, date_str.split('-'))
            match_datetime = timezone.make_aware(
                datetime(year, month, day, hour, minute, 0),
                timezone=pytz.UTC
            )

            home_team = teams.get(home_name)
            away_team = teams.get(away_name)

            if dry_run:
                self.stdout.write(
                    f'  [WOULD CREATE] Round {cup_round}: {home_name} vs {away_name} '
                    f'({date_str} {time_str} GMT)'
                )
                matches.append(None)
            else:
                if not home_team or not away_team:
                    self.stdout.write(self.style.ERROR(
                        f'  [SKIPPED] Missing team: {home_name} or {away_name}'
                    ))
                    continue

                # Check if match already exists
                existing = Match.objects.filter(
                    tournament=tournament,
                    home_team=home_team,
                    away_team=away_team,
                    cup_round=cup_round
                ).first()

                if existing:
                    self.stdout.write(
                        f'  [EXISTS] Round {cup_round}: {home_name} vs {away_name}'
                    )
                    matches.append(existing)
                else:
                    match = Match.objects.create(
                        tournament=tournament,
                        date=match_datetime,
                        cup_round=cup_round,
                        home_team=home_team,
                        away_team=away_team,
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'  [CREATED] Round {cup_round}: {home_name} vs {away_name} '
                        f'(ID: {match.id})'
                    ))
                    matches.append(match)

        return matches

    def _create_team_stats(self, tournament, teams, dry_run):
        """Create TeamStat entries for each team in the tournament."""
        if tournament is None:
            self.stdout.write('  [SKIPPED] No tournament available')
            return

        for team_name, team in teams.items():
            if team is None:
                continue

            if dry_run:
                existing = TeamStat.objects.filter(
                    tournament=tournament, team=team
                ).first()
                if existing:
                    self.stdout.write(f'  [EXISTS] Stats for {team_name}')
                else:
                    self.stdout.write(f'  [WOULD CREATE] Stats for {team_name}')
            else:
                stat, created = TeamStat.objects.get_or_create(
                    tournament=tournament,
                    team=team,
                    defaults={
                        'played': 0, 'win': 0, 'draw': 0, 'lose': 0,
                        'ptsfor': 0, 'ptsagainst': 0, 'ptsdiff': 0,
                        'tryfor': 0, 'tryagainst': 0,
                        'trybonus': 0, 'losebonus': 0, 'points': 0,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'  [CREATED] Stats for {team_name}'
                    ))
                else:
                    self.stdout.write(f'  [EXISTS] Stats for {team_name}')
