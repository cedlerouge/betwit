import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatchService } from '../../../core/services/match.service';
import { TournamentService } from '../../../core/services/tournament.service';
import { Match, Tournament } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-match-list',
  standalone: true,
  imports: [RouterLink, DatePipe, FormsModule, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Matchs</h2>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label for="tournament" class="form-label">Tournoi</label>
            <select
              id="tournament"
              class="form-select"
              [(ngModel)]="selectedTournament"
              (ngModelChange)="filterMatches()"
            >
              <option [ngValue]="null">Tous les tournois</option>
              @for (t of tournaments(); track t.id) {
                <option [ngValue]="t.id">{{ t.name }} {{ t.year }}</option>
              }
            </select>
          </div>
          <div class="col-md-4">
            <label for="filter" class="form-label">Afficher</label>
            <select
              id="filter"
              class="form-select"
              [(ngModel)]="matchFilter"
              (ngModelChange)="filterMatches()"
            >
              <option value="all">Tous les matchs</option>
              <option value="upcoming">À venir uniquement</option>
              <option value="past">Passés uniquement</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      <div class="row">
        @for (match of filteredMatches(); track match.id) {
          <div class="col-md-6 col-lg-4 mb-4">
            <div class="card match-card h-100">
              <div class="card-header">
                <small class="text-muted">{{ match.tournament }} - Journée {{ match.cup_round }}</small>
              </div>
              <div class="card-body text-center">
                <div class="row align-items-center">
                  <div class="col-5">
                    <h5 class="mb-0">{{ match.home_team }}</h5>
                  </div>
                  <div class="col-2">
                    @if (isPastMatch(match.date)) {
                      <span class="badge bg-secondary fs-6">
                        {{ match.home_team_score }} - {{ match.away_team_score }}
                      </span>
                    } @else {
                      <span class="text-muted">vs</span>
                    }
                  </div>
                  <div class="col-5">
                    <h5 class="mb-0">{{ match.away_team }}</h5>
                  </div>
                </div>
                <hr>
                <small class="text-muted">{{ match.date | date:'medium' }}</small>
              </div>
              <div class="card-footer">
                @if (!isPastMatch(match.date)) {
                  <a [routerLink]="['/matches', match.id, 'bet']" class="btn btn-success btn-sm w-100">
                    Parier
                  </a>
                } @else {
                  <span class="text-muted">Match terminé</span>
                }
              </div>
            </div>
          </div>
        } @empty {
          <div class="col-12">
            <div class="alert alert-info">Aucun match trouvé.</div>
          </div>
        }
      </div>
    }
  `
})
export class MatchListComponent implements OnInit {
  private readonly matchService = inject(MatchService);
  private readonly tournamentService = inject(TournamentService);

  matches = signal<Match[]>([]);
  filteredMatches = signal<Match[]>([]);
  tournaments = signal<Tournament[]>([]);
  loading = signal(true);

  selectedTournament: number | null = null;
  matchFilter = 'all';

  ngOnInit(): void {
    this.loadTournaments();
    this.loadMatches();
  }

  private loadTournaments(): void {
    this.tournamentService.getAll().subscribe({
      next: (data) => this.tournaments.set(data)
    });
  }

  private loadMatches(): void {
    this.matchService.getAll().subscribe({
      next: (data) => {
        this.matches.set(data);
        this.filterMatches();
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  filterMatches(): void {
    let filtered = this.matches();

    if (this.selectedTournament) {
      filtered = filtered.filter(m => m.tournament.includes(String(this.selectedTournament)));
    }

    const now = new Date();
    if (this.matchFilter === 'upcoming') {
      filtered = filtered.filter(m => new Date(m.date) > now);
    } else if (this.matchFilter === 'past') {
      filtered = filtered.filter(m => new Date(m.date) <= now);
    }

    this.filteredMatches.set(filtered);
  }

  isPastMatch(dateStr: string): boolean {
    return new Date(dateStr) < new Date();
  }
}
