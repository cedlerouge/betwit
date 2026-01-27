import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { TournamentService } from '../../../core/services/tournament.service';
import { MatchService } from '../../../core/services/match.service';
import { Tournament, Match, TeamStat } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-tournament-detail',
  standalone: true,
  imports: [RouterLink, DatePipe, LoadingSpinnerComponent],
  template: `
    <app-loading-spinner [loading]="loading()" />

    @if (!loading() && tournament()) {
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>{{ tournament()?.name }} {{ tournament()?.year }}</h2>
        <a routerLink="/tournaments" class="btn btn-outline-secondary">Retour aux tournois</a>
      </div>

      <div class="row">
        <!-- Standings -->
        <div class="col-lg-5 mb-4">
          <div class="card">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Classement</h5>
            </div>
            <div class="card-body p-0">
              @if (standings().length) {
                <div class="table-responsive">
                  <table class="table table-hover mb-0">
                    <thead class="table-light">
                      <tr>
                        <th>#</th>
                        <th>Équipe</th>
                        <th class="text-center">J</th>
                        <th class="text-center">G</th>
                        <th class="text-center">N</th>
                        <th class="text-center">P</th>
                        <th class="text-center">+/-</th>
                        <th class="text-center">Pts</th>
                      </tr>
                    </thead>
                    <tbody>
                      @for (stat of standings(); track stat.id; let i = $index) {
                        <tr>
                          <td>{{ i + 1 }}</td>
                          <td>{{ stat.team.name }}</td>
                          <td class="text-center">{{ stat.played }}</td>
                          <td class="text-center">{{ stat.win }}</td>
                          <td class="text-center">{{ stat.draw }}</td>
                          <td class="text-center">{{ stat.lose }}</td>
                          <td class="text-center">{{ stat.ptsdiff }}</td>
                          <td class="text-center"><strong>{{ stat.points }}</strong></td>
                        </tr>
                      }
                    </tbody>
                  </table>
                </div>
              } @else {
                <p class="text-muted text-center py-3 mb-0">Pas encore de classement</p>
              }
            </div>
          </div>
        </div>

        <!-- Matches -->
        <div class="col-lg-7 mb-4">
          <div class="card">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Matchs</h5>
            </div>
            <div class="card-body p-0">
              @if (matches().length) {
                <div class="table-responsive">
                  <table class="table table-hover mb-0">
                    <thead class="table-light">
                      <tr>
                        <th>Date</th>
                        <th>Match</th>
                        <th class="text-center">Score</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      @for (match of matches(); track match.id) {
                        <tr>
                          <td>
                            <small>{{ match.date | date:'short' }}</small>
                          </td>
                          <td>
                            <strong>{{ match.home_team }}</strong> vs <strong>{{ match.away_team }}</strong>
                          </td>
                          <td class="text-center">
                            @if (isPastMatch(match.date)) {
                              {{ match.home_team_score }} - {{ match.away_team_score }}
                            } @else {
                              <span class="text-muted">-</span>
                            }
                          </td>
                          <td class="text-end">
                            @if (!isPastMatch(match.date)) {
                              <a [routerLink]="['/matches', match.id, 'bet']" class="btn btn-success btn-sm">Parier</a>
                            }
                          </td>
                        </tr>
                      }
                    </tbody>
                  </table>
                </div>
              } @else {
                <p class="text-muted text-center py-3 mb-0">Aucun match programmé</p>
              }
            </div>
          </div>
        </div>
      </div>
    }
  `
})
export class TournamentDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly tournamentService = inject(TournamentService);
  private readonly matchService = inject(MatchService);

  tournament = signal<Tournament | null>(null);
  standings = signal<TeamStat[]>([]);
  matches = signal<Match[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.loadTournament(id);
    }
  }

  private loadTournament(id: number): void {
    this.tournamentService.getById(id).subscribe({
      next: (tournament) => {
        this.tournament.set(tournament);
        this.loadStandings(id);
        this.loadMatches(id);
      },
      error: () => this.loading.set(false)
    });
  }

  private loadStandings(tournamentId: number): void {
    this.tournamentService.getTeamStats(tournamentId).subscribe({
      next: (standings) => this.standings.set(standings)
    });
  }

  private loadMatches(tournamentId: number): void {
    this.matchService.getByTournament(tournamentId).subscribe({
      next: (matches) => {
        this.matches.set(matches);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  isPastMatch(dateStr: string): boolean {
    return new Date(dateStr) < new Date();
  }
}
