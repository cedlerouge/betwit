import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BetService } from '../../../core/services/bet.service';
import { TournamentService } from '../../../core/services/tournament.service';
import { TeamService } from '../../../core/services/team.service';
import { Tournament, Team, TournamentBet, TournamentBetCreate } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-tournament-bet',
  standalone: true,
  imports: [FormsModule, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Pari Tournoi</h2>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      <!-- Existing Bets -->
      @if (existingBets().length) {
        <div class="card mb-4">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Vos paris tournoi</h5>
          </div>
          <div class="card-body">
            @for (bet of existingBets(); track bet.id) {
              <div class="mb-3 pb-3 border-bottom">
                <strong>{{ bet.tournament_name }}</strong>
                <ol class="mb-2 mt-2">
                  <li>{{ bet.first_team_name }}</li>
                  <li>{{ bet.second_team_name }}</li>
                  <li>{{ bet.third_team_name }}</li>
                  <li>{{ bet.fourth_team_name }}</li>
                  <li>{{ bet.fifth_team_name }}</li>
                  <li>{{ bet.sixth_team_name }}</li>
                </ol>
                <small class="text-muted">
                  Grand Chelem: {{ bet.grand_slam ? 'Oui' : 'Non' }} |
                  Cuillère de bois: {{ bet.wooden_spoon ? 'Oui' : 'Non' }}
                  @if (bet.points_won !== null) {
                    | Points: {{ bet.points_won }}
                  }
                </small>
              </div>
            }
          </div>
        </div>
      }

      <!-- New Bet Form -->
      <div class="card">
        <div class="card-header bg-success text-white">
          <h5 class="mb-0">Placer un nouveau pari</h5>
        </div>
        <div class="card-body">
          @if (error()) {
            <div class="alert alert-danger">{{ error() }}</div>
          }

          @if (success()) {
            <div class="alert alert-success">Pari tournoi placé avec succès !</div>
          }

          @if (activeTournaments().length === 0) {
            <div class="alert alert-info">Aucun tournoi actif disponible pour les paris.</div>
          } @else {
            <form (ngSubmit)="onSubmit()">
              <div class="mb-3">
                <label class="form-label">Tournoi</label>
                <select class="form-select" [(ngModel)]="bet.tournament" name="tournament" required>
                  <option [ngValue]="0" disabled>Sélectionner un tournoi</option>
                  @for (t of activeTournaments(); track t.id) {
                    <option [ngValue]="t.id">{{ t.name }} {{ t.year }}</option>
                  }
                </select>
              </div>

              <p class="text-muted">Prédisez le classement final (1ère à 6ème place) :</p>

              <div class="row">
                @for (position of positions; track position.rank) {
                  <div class="col-md-6 col-lg-4 mb-3">
                    <label class="form-label">{{ position.label }}</label>
                    <select
                      class="form-select"
                      [(ngModel)]="bet[position.field]"
                      [name]="position.field"
                      required
                    >
                      <option [ngValue]="0" disabled>Sélectionner une équipe</option>
                      @for (team of teams(); track team.id) {
                        <option [ngValue]="team.id">{{ team.name }}</option>
                      }
                    </select>
                  </div>
                }
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="form-check">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      [(ngModel)]="bet.grand_slam"
                      name="grandSlam"
                      id="grandSlam"
                    >
                    <label class="form-check-label" for="grandSlam">
                      Grand Chelem (1ère place gagne tous ses matchs)
                    </label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-check">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      [(ngModel)]="bet.wooden_spoon"
                      name="woodenSpoon"
                      id="woodenSpoon"
                    >
                    <label class="form-check-label" for="woodenSpoon">
                      Cuillère de bois (6ème place perd tous ses matchs)
                    </label>
                  </div>
                </div>
              </div>

              <button type="submit" class="btn btn-success" [disabled]="submitting()">
                @if (submitting()) {
                  <span class="spinner-border spinner-border-sm me-2"></span>
                }
                Placer le pari
              </button>
            </form>
          }
        </div>
      </div>
    }
  `
})
export class TournamentBetComponent implements OnInit {
  private readonly betService = inject(BetService);
  private readonly tournamentService = inject(TournamentService);
  private readonly teamService = inject(TeamService);

  activeTournaments = signal<Tournament[]>([]);
  teams = signal<Team[]>([]);
  existingBets = signal<TournamentBet[]>([]);
  loading = signal(true);
  submitting = signal(false);
  error = signal<string | null>(null);
  success = signal(false);

  positions = [
    { rank: 1, label: '1ère Place', field: 'first_team' as keyof TournamentBetCreate },
    { rank: 2, label: '2ème Place', field: 'second_team' as keyof TournamentBetCreate },
    { rank: 3, label: '3ème Place', field: 'third_team' as keyof TournamentBetCreate },
    { rank: 4, label: '4ème Place', field: 'fourth_team' as keyof TournamentBetCreate },
    { rank: 5, label: '5ème Place', field: 'fifth_team' as keyof TournamentBetCreate },
    { rank: 6, label: '6ème Place', field: 'sixth_team' as keyof TournamentBetCreate },
  ];

  bet: TournamentBetCreate = {
    tournament: 0,
    first_team: 0,
    second_team: 0,
    third_team: 0,
    fourth_team: 0,
    fifth_team: 0,
    sixth_team: 0,
    grand_slam: false,
    wooden_spoon: false
  };

  ngOnInit(): void {
    this.loadData();
  }

  private loadData(): void {
    this.tournamentService.getActive().subscribe({
      next: (tournaments) => {
        this.activeTournaments.set(tournaments);
        if (tournaments.length > 0) {
          this.bet.tournament = tournaments[0].id;
        }
      }
    });

    this.teamService.getAll().subscribe({
      next: (teams) => this.teams.set(teams)
    });

    this.betService.getTournamentBets().subscribe({
      next: (bets) => {
        this.existingBets.set(bets);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  onSubmit(): void {
    this.error.set(null);
    this.success.set(false);

    // Validate unique teams
    const selectedTeams = [
      this.bet.first_team,
      this.bet.second_team,
      this.bet.third_team,
      this.bet.fourth_team,
      this.bet.fifth_team,
      this.bet.sixth_team
    ];

    const uniqueTeams = new Set(selectedTeams);
    if (uniqueTeams.size !== 6 || selectedTeams.includes(0)) {
      this.error.set('Veuillez sélectionner 6 équipes différentes.');
      return;
    }

    this.submitting.set(true);

    this.betService.createTournamentBet(this.bet).subscribe({
      next: (newBet) => {
        this.submitting.set(false);
        this.success.set(true);
        this.existingBets.update(bets => [newBet, ...bets]);
      },
      error: (err) => {
        this.submitting.set(false);
        this.error.set(err.message || 'Échec du placement du pari.');
      }
    });
  }
}
