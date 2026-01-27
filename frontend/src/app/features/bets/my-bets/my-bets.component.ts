import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DatePipe, DecimalPipe } from '@angular/common';
import { BetService } from '../../../core/services/bet.service';
import { MatchBet } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-my-bets',
  standalone: true,
  imports: [RouterLink, DatePipe, DecimalPipe, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Mes Paris</h2>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      @if (bets().length) {
        <div class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Date</th>
                <th>Match</th>
                <th class="text-center">Votre prédiction</th>
                <th class="text-center">Extras</th>
                <th class="text-center">Points gagnés</th>
              </tr>
            </thead>
            <tbody>
              @for (bet of bets(); track bet.id) {
                <tr>
                  <td>
                    <small>{{ bet.created_date | date:'short' }}</small>
                  </td>
                  <td>
                    <a [routerLink]="['/matches', bet.match]">Match #{{ bet.match }}</a>
                  </td>
                  <td class="text-center">
                    <span class="badge bg-primary">
                      {{ bet.home_team_score }} - {{ bet.away_team_score }}
                    </span>
                    <br>
                    <small class="text-muted">
                      Essais: {{ bet.home_team_tries }} - {{ bet.away_team_tries }}
                    </small>
                  </td>
                  <td class="text-center">
                    @if (bet.card) {
                      <span class="badge bg-warning me-1">Carton</span>
                    }
                    @if (bet.drop_goal) {
                      <span class="badge bg-info me-1">Drop</span>
                    }
                    @if (bet.fight) {
                      <span class="badge bg-danger me-1">Bagarre</span>
                    }
                    @if (!bet.card && !bet.drop_goal && !bet.fight) {
                      <span class="text-muted">-</span>
                    }
                  </td>
                  <td class="text-center">
                    @if (bet.points_won !== null && bet.points_won !== undefined) {
                      <span
                        class="badge"
                        [class.bg-success]="bet.points_won > 0"
                        [class.bg-secondary]="bet.points_won === 0"
                        [class.bg-danger]="bet.points_won < 0"
                      >
                        {{ bet.points_won | number:'1.1-1' }}
                      </span>
                    } @else {
                      <span class="text-muted">En attente</span>
                    }
                  </td>
                </tr>
              }
            </tbody>
          </table>
        </div>

        <!-- Summary -->
        <div class="card mt-4">
          <div class="card-body">
            <div class="row text-center">
              <div class="col-md-4">
                <h5>{{ bets().length }}</h5>
                <small class="text-muted">Total paris</small>
              </div>
              <div class="col-md-4">
                <h5>{{ totalPoints() | number:'1.1-1' }}</h5>
                <small class="text-muted">Points totaux</small>
              </div>
              <div class="col-md-4">
                <h5>{{ averagePoints() | number:'1.1-1' }}</h5>
                <small class="text-muted">Moyenne pts/pari</small>
              </div>
            </div>
          </div>
        </div>
      } @else {
        <div class="alert alert-info">
          Vous n'avez pas encore placé de paris.
          <a routerLink="/matches">Parcourir les matchs</a> pour commencer à parier !
        </div>
      }
    }
  `
})
export class MyBetsComponent implements OnInit {
  private readonly betService = inject(BetService);

  bets = signal<MatchBet[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    this.betService.getMatchBets().subscribe({
      next: (data) => {
        this.bets.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  totalPoints(): number {
    return this.bets().reduce((sum, bet) => sum + (bet.points_won || 0), 0);
  }

  averagePoints(): number {
    const betsWithPoints = this.bets().filter(b => b.points_won !== null);
    if (betsWithPoints.length === 0) return 0;
    return this.totalPoints() / betsWithPoints.length;
  }
}
