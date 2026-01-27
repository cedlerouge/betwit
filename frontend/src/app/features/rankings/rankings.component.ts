import { Component, inject, OnInit, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { UserService } from '../../core/services/user.service';
import { AuthService } from '../../core/services/auth.service';
import { UserRanking } from '../../core/models';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-rankings',
  standalone: true,
  imports: [DecimalPipe, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Classement des joueurs</h2>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      @if (rankings().length) {
        <div class="card">
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="text-center" style="width: 80px">Rang</th>
                    <th>Joueur</th>
                    <th class="text-center">Matchs pariés</th>
                    <th class="text-center">Points totaux</th>
                  </tr>
                </thead>
                <tbody>
                  @for (ranking of rankings(); track ranking.user_id) {
                    <tr [class.table-success]="isCurrentUser(ranking.username)">
                      <td class="text-center">
                        @switch (ranking.rank) {
                          @case (1) {
                            <span class="badge bg-warning text-dark fs-6">1</span>
                          }
                          @case (2) {
                            <span class="badge bg-secondary fs-6">2</span>
                          }
                          @case (3) {
                            <span class="badge bg-danger fs-6">3</span>
                          }
                          @default {
                            <span class="text-muted">{{ ranking.rank }}</span>
                          }
                        }
                      </td>
                      <td>
                        <strong>{{ ranking.username }}</strong>
                        @if (isCurrentUser(ranking.username)) {
                          <span class="badge bg-info ms-2">Vous</span>
                        }
                      </td>
                      <td class="text-center">{{ ranking.matches_bet }}</td>
                      <td class="text-center">
                        <span class="badge bg-success fs-6">{{ ranking.total_points | number:'1.1-1' }}</span>
                      </td>
                    </tr>
                  }
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Stats Summary -->
        <div class="row mt-4">
          <div class="col-md-4">
            <div class="card text-center">
              <div class="card-body">
                <h3>{{ rankings().length }}</h3>
                <small class="text-muted">Total joueurs</small>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card text-center">
              <div class="card-body">
                <h3>{{ totalBets() }}</h3>
                <small class="text-muted">Total paris placés</small>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card text-center">
              <div class="card-body">
                <h3>{{ averagePoints() | number:'1.1-1' }}</h3>
                <small class="text-muted">Points moyens</small>
              </div>
            </div>
          </div>
        </div>
      } @else {
        <div class="alert alert-info">
          Pas encore de classement disponible. Commencez à parier pour apparaître au classement !
        </div>
      }
    }
  `
})
export class RankingsComponent implements OnInit {
  private readonly userService = inject(UserService);
  private readonly authService = inject(AuthService);

  rankings = signal<UserRanking[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    this.userService.getRankings().subscribe({
      next: (data) => {
        this.rankings.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  isCurrentUser(username: string): boolean {
    return this.authService.user()?.username === username;
  }

  totalBets(): number {
    return this.rankings().reduce((sum, r) => sum + r.matches_bet, 0);
  }

  averagePoints(): number {
    if (this.rankings().length === 0) return 0;
    const total = this.rankings().reduce((sum, r) => sum + r.total_points, 0);
    return total / this.rankings().length;
  }
}
