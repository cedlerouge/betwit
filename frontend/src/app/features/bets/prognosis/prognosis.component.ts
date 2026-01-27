import { Component, inject, OnInit, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BetService } from '../../../core/services/bet.service';
import { MatchService } from '../../../core/services/match.service';
import { BetPoint, Match } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

interface MatchPrognosis {
  match: Match;
  betPoints: BetPoint[];
}

@Component({
  selector: 'app-prognosis',
  standalone: true,
  imports: [DecimalPipe, FormsModule, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Pronostics</h2>
    <p class="text-muted mb-4">Découvrez comment les autres joueurs ont parié sur les matchs terminés.</p>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      @if (betPoints().length) {
        <div class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Joueur</th>
                <th>Match</th>
                <th class="text-center">Points gagnés</th>
              </tr>
            </thead>
            <tbody>
              @for (bp of betPoints(); track bp.id) {
                <tr>
                  <td>Joueur #{{ bp.player }}</td>
                  <td>Match #{{ bp.match }}</td>
                  <td class="text-center">
                    <span
                      class="badge"
                      [class.bg-success]="bp.points_won > 0"
                      [class.bg-secondary]="bp.points_won === 0"
                      [class.bg-danger]="bp.points_won < 0"
                    >
                      {{ bp.points_won | number:'1.1-1' }}
                    </span>
                  </td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      } @else {
        <div class="alert alert-info">
          Pas encore de résultats de paris disponibles.
        </div>
      }
    }
  `
})
export class PrognosisComponent implements OnInit {
  private readonly betService = inject(BetService);

  betPoints = signal<BetPoint[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    this.betService.getBetPoints().subscribe({
      next: (data) => {
        this.betPoints.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }
}
