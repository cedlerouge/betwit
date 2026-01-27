import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { TournamentService } from '../../../core/services/tournament.service';
import { Tournament } from '../../../core/models';
import { LoadingSpinnerComponent } from '../../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-tournament-list',
  standalone: true,
  imports: [RouterLink, DatePipe, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Tournois</h2>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      <div class="row">
        @for (tournament of tournaments(); track tournament.id) {
          <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
              <div class="card-header" [class.bg-success]="tournament.state === '1'" [class.text-white]="tournament.state === '1'">
                <h5 class="mb-0">{{ tournament.name }} {{ tournament.year }}</h5>
              </div>
              <div class="card-body">
                <p class="mb-2">
                  <strong>Début :</strong> {{ tournament.begins | date:'mediumDate' }}
                </p>
                <p class="mb-0">
                  <strong>Statut :</strong>
                  @switch (tournament.state) {
                    @case ('1') { <span class="badge bg-success">Actif</span> }
                    @case ('2') { <span class="badge bg-info">À venir</span> }
                    @case ('3') { <span class="badge bg-secondary">Archivé</span> }
                  }
                </p>
              </div>
              <div class="card-footer">
                <a [routerLink]="['/tournaments', tournament.id]" class="btn btn-outline-success btn-sm w-100">
                  Voir les détails
                </a>
              </div>
            </div>
          </div>
        } @empty {
          <div class="col-12">
            <div class="alert alert-info">Aucun tournoi disponible.</div>
          </div>
        }
      </div>
    }
  `
})
export class TournamentListComponent implements OnInit {
  private readonly tournamentService = inject(TournamentService);

  tournaments = signal<Tournament[]>([]);
  loading = signal(true);

  ngOnInit(): void {
    this.tournamentService.getAll().subscribe({
      next: (data) => {
        this.tournaments.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }
}
