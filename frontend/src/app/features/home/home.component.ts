import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DatePipe, DecimalPipe } from '@angular/common';
import { HomeService, HomeData } from '../../core/services/home.service';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink, DatePipe, DecimalPipe, LoadingSpinnerComponent],
  template: `
    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      <div class="row">
        <!-- Welcome Section -->
        <div class="col-12 mb-4">
          <div class="card bg-success text-white">
            <div class="card-body text-center py-4">
              <h1 class="display-5">Bienvenue sur Betwit</h1>
              <p class="lead mb-0">Jeu de paris Rugby - Prédisez les résultats des matchs et affrontez vos amis !</p>
            </div>
          </div>
        </div>

        <!-- Active Tournament -->
        @if (data()?.active_tournament) {
          <div class="col-12 mb-4">
            <div class="alert alert-info mb-0">
              <strong>Tournoi en cours :</strong>
              <a [routerLink]="['/tournaments', data()?.active_tournament?.id]" class="alert-link ms-2">
                {{ data()?.active_tournament?.name }}
              </a>
            </div>
          </div>
        }

        <!-- Top Players -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="mb-0">Top 5 Joueurs</h5>
            </div>
            <div class="card-body p-0">
              @if (data()?.top_players?.length) {
                <ul class="list-group list-group-flush">
                  @for (player of data()?.top_players; track player.user_id) {
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>
                        <span class="badge bg-secondary me-2">{{ player.rank }}</span>
                        {{ player.username }}
                      </span>
                      <span class="badge bg-success rounded-pill">{{ player.total_points | number:'1.1-1' }} pts</span>
                    </li>
                  }
                </ul>
              } @else {
                <p class="text-muted text-center py-3 mb-0">Pas encore de classement</p>
              }
            </div>
            <div class="card-footer">
              <a routerLink="/rankings" class="btn btn-outline-success btn-sm w-100">Voir tout le classement</a>
            </div>
          </div>
        </div>

        <!-- Upcoming Matches -->
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="mb-0">Prochains Matchs</h5>
            </div>
            <div class="card-body p-0">
              @if (data()?.upcoming_matches?.length) {
                <ul class="list-group list-group-flush">
                  @for (match of data()?.upcoming_matches; track match.id) {
                    <li class="list-group-item">
                      <div class="d-flex justify-content-between align-items-start">
                        <div>
                          <strong>{{ match.home_team }}</strong> vs <strong>{{ match.away_team }}</strong>
                          <br>
                          <small class="text-muted">{{ match.date | date:'short' }}</small>
                        </div>
                        <a [routerLink]="['/matches', match.id, 'bet']" class="btn btn-success btn-sm">Parier</a>
                      </div>
                      @if (match.rating) {
                        <div class="mt-2">
                          <small class="text-muted">
                            Cotes : {{ match.rating.ht_rating | number:'1.1-1' }} /
                            {{ match.rating.null_rating | number:'1.1-1' }} /
                            {{ match.rating.at_rating | number:'1.1-1' }}
                            ({{ match.rating.total_votes }} votes)
                          </small>
                        </div>
                      }
                    </li>
                  }
                </ul>
              } @else {
                <p class="text-muted text-center py-3 mb-0">Pas de matchs à venir</p>
              }
            </div>
            <div class="card-footer">
              <a routerLink="/matches" class="btn btn-outline-success btn-sm w-100">Voir tous les matchs</a>
            </div>
          </div>
        </div>

        <!-- Standings -->
        <div class="col-md-12 col-lg-4 mb-4">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="mb-0">Classement du Tournoi</h5>
            </div>
            <div class="card-body p-0">
              @if (data()?.standings?.length) {
                <div class="table-responsive">
                  <table class="table table-sm table-hover mb-0">
                    <thead class="table-light">
                      <tr>
                        <th>#</th>
                        <th>Équipe</th>
                        <th class="text-center">J</th>
                        <th class="text-center">G</th>
                        <th class="text-center">N</th>
                        <th class="text-center">P</th>
                        <th class="text-center">Pts</th>
                      </tr>
                    </thead>
                    <tbody>
                      @for (stat of data()?.standings; track stat.id; let i = $index) {
                        <tr>
                          <td>{{ i + 1 }}</td>
                          <td>{{ stat.team.name }}</td>
                          <td class="text-center">{{ stat.played }}</td>
                          <td class="text-center">{{ stat.win }}</td>
                          <td class="text-center">{{ stat.draw }}</td>
                          <td class="text-center">{{ stat.lose }}</td>
                          <td class="text-center"><strong>{{ stat.points }}</strong></td>
                        </tr>
                      }
                    </tbody>
                  </table>
                </div>
              } @else {
                <p class="text-muted text-center py-3 mb-0">Pas de classement disponible</p>
              }
            </div>
            @if (data()?.active_tournament) {
              <div class="card-footer">
                <a [routerLink]="['/tournaments', data()?.active_tournament?.id]" class="btn btn-outline-success btn-sm w-100">
                  Voir le tournoi
                </a>
              </div>
            }
          </div>
        </div>
      </div>
    }
  `
})
export class HomeComponent implements OnInit {
  private readonly homeService = inject(HomeService);

  data = signal<HomeData | null>(null);
  loading = signal(true);

  ngOnInit(): void {
    this.loadData();
  }

  private loadData(): void {
    this.homeService.getHomeData().subscribe({
      next: (data) => {
        this.data.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }
}
