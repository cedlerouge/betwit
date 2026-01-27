import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatchService } from '../../../core/services/match.service';
import { BetService } from '../../../core/services/bet.service';
import { MatchDetail, MatchBetCreate } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-match-bet-form',
  standalone: true,
  imports: [RouterLink, DatePipe, FormsModule, LoadingSpinnerComponent],
  template: `
    <app-loading-spinner [loading]="loading()" />

    @if (!loading() && match()) {
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header bg-success text-white">
              <h4 class="mb-0">Placer votre pari</h4>
            </div>
            <div class="card-body">
              <!-- Match Info -->
              <div class="text-center mb-4">
                <h5>{{ match()?.home_team?.name }} vs {{ match()?.away_team?.name }}</h5>
                <p class="text-muted mb-0">
                  {{ match()?.tournament?.name }} - Journée {{ match()?.cup_round }}
                </p>
                <p class="text-muted">{{ match()?.date | date:'medium' }}</p>
              </div>

              @if (error()) {
                <div class="alert alert-danger">{{ error() }}</div>
              }

              @if (success()) {
                <div class="alert alert-success">
                  Pari placé avec succès ! <a routerLink="/my-bets">Voir vos paris</a>
                </div>
              }

              <form (ngSubmit)="onSubmit()">
                <div class="row">
                  <!-- Home Team -->
                  <div class="col-md-6 mb-4">
                    <div class="card">
                      <div class="card-header bg-light">
                        <strong>{{ match()?.home_team?.name }}</strong>
                      </div>
                      <div class="card-body">
                        <div class="mb-3">
                          <label class="form-label">Score</label>
                          <input
                            type="number"
                            class="form-control"
                            [(ngModel)]="bet.home_team_score"
                            name="homeScore"
                            min="0"
                            required
                          >
                        </div>
                        <div class="mb-3">
                          <label class="form-label">Essais</label>
                          <input
                            type="number"
                            class="form-control"
                            [(ngModel)]="bet.home_team_tries"
                            name="homeTries"
                            min="0"
                            required
                          >
                        </div>
                        <div class="mb-3">
                          <label class="form-label">Bonus</label>
                          <select class="form-select" [(ngModel)]="bet.home_team_bonus" name="homeBonus">
                            <option value="Null">Aucun</option>
                            <option value="Attack">Attaque (4+ essais)</option>
                            <option value="Defense">Défense (perdre de 7 ou moins)</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Away Team -->
                  <div class="col-md-6 mb-4">
                    <div class="card">
                      <div class="card-header bg-light">
                        <strong>{{ match()?.away_team?.name }}</strong>
                      </div>
                      <div class="card-body">
                        <div class="mb-3">
                          <label class="form-label">Score</label>
                          <input
                            type="number"
                            class="form-control"
                            [(ngModel)]="bet.away_team_score"
                            name="awayScore"
                            min="0"
                            required
                          >
                        </div>
                        <div class="mb-3">
                          <label class="form-label">Essais</label>
                          <input
                            type="number"
                            class="form-control"
                            [(ngModel)]="bet.away_team_tries"
                            name="awayTries"
                            min="0"
                            required
                          >
                        </div>
                        <div class="mb-3">
                          <label class="form-label">Bonus</label>
                          <select class="form-select" [(ngModel)]="bet.away_team_bonus" name="awayBonus">
                            <option value="Null">Aucun</option>
                            <option value="Attack">Attaque (4+ essais)</option>
                            <option value="Defense">Défense (perdre de 7 ou moins)</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Match Extras -->
                <div class="card mb-4">
                  <div class="card-header bg-light">
                    <strong>Prédictions du match</strong>
                  </div>
                  <div class="card-body">
                    <div class="row">
                      <div class="col-md-4">
                        <div class="form-check">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            [(ngModel)]="bet.card"
                            name="card"
                            id="card"
                          >
                          <label class="form-check-label" for="card">
                            Carton (Jaune/Rouge)
                          </label>
                        </div>
                      </div>
                      <div class="col-md-4">
                        <div class="form-check">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            [(ngModel)]="bet.drop_goal"
                            name="dropGoal"
                            id="dropGoal"
                          >
                          <label class="form-check-label" for="dropGoal">
                            Drop Goal
                          </label>
                        </div>
                      </div>
                      <div class="col-md-4">
                        <div class="form-check">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            [(ngModel)]="bet.fight"
                            name="fight"
                            id="fight"
                          >
                          <label class="form-check-label" for="fight">
                            Bagarre
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Joker Bet -->
                @if (match()?.jokerbet_text) {
                  <div class="card mb-4">
                    <div class="card-header bg-warning">
                      <strong>Pari Joker</strong>
                    </div>
                    <div class="card-body">
                      <p class="mb-3">{{ match()?.jokerbet_text }}</p>
                      <p class="text-muted small">
                        Gagné : +{{ match()?.jokerbet_win_pts }} pts / Perdu : -{{ match()?.jokerbet_lose_pts }} pts
                      </p>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          name="jokerbet"
                          id="jokerYes"
                          [value]="true"
                          [(ngModel)]="bet.jokerbet_value"
                        >
                        <label class="form-check-label" for="jokerYes">Oui</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          name="jokerbet"
                          id="jokerNo"
                          [value]="false"
                          [(ngModel)]="bet.jokerbet_value"
                        >
                        <label class="form-check-label" for="jokerNo">Non</label>
                      </div>
                    </div>
                  </div>
                }

                <div class="d-flex justify-content-between">
                  <a routerLink="/matches" class="btn btn-outline-secondary">Annuler</a>
                  <button type="submit" class="btn btn-success" [disabled]="submitting()">
                    @if (submitting()) {
                      <span class="spinner-border spinner-border-sm me-2"></span>
                    }
                    Placer le pari
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    }
  `
})
export class MatchBetFormComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly matchService = inject(MatchService);
  private readonly betService = inject(BetService);

  match = signal<MatchDetail | null>(null);
  loading = signal(true);
  submitting = signal(false);
  error = signal<string | null>(null);
  success = signal(false);

  bet: MatchBetCreate = {
    match: 0,
    home_team_score: 0,
    home_team_tries: 0,
    home_team_bonus: 'Null',
    away_team_score: 0,
    away_team_tries: 0,
    away_team_bonus: 'Null',
    card: false,
    drop_goal: false,
    fight: false
  };

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.bet.match = id;
      this.loadMatch(id);
    }
  }

  private loadMatch(id: number): void {
    this.matchService.getById(id).subscribe({
      next: (match) => {
        this.match.set(match);
        this.loading.set(false);

        // Check if match has already started
        if (new Date(match.date) < new Date()) {
          this.error.set('Ce match a déjà commencé. Vous ne pouvez pas placer de pari.');
        }
      },
      error: () => this.loading.set(false)
    });
  }

  onSubmit(): void {
    this.error.set(null);
    this.submitting.set(true);

    this.betService.createMatchBet(this.bet).subscribe({
      next: () => {
        this.submitting.set(false);
        this.success.set(true);
      },
      error: (err) => {
        this.submitting.set(false);
        this.error.set(err.message || 'Échec du placement du pari. Veuillez réessayer.');
      }
    });
  }
}
