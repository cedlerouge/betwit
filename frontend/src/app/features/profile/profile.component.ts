import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';
import { Profile } from '../../core/models';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [FormsModule, LoadingSpinnerComponent],
  template: `
    <h2 class="mb-4">Paramètres du profil</h2>

    <app-loading-spinner [loading]="loading()" />

    @if (!loading()) {
      <div class="row">
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Informations du compte</h5>
            </div>
            <div class="card-body">
              @if (error()) {
                <div class="alert alert-danger">{{ error() }}</div>
              }
              @if (success()) {
                <div class="alert alert-success">Profil mis à jour avec succès !</div>
              }

              <form (ngSubmit)="onSubmit()">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label class="form-label">Nom d'utilisateur</label>
                    <input
                      type="text"
                      class="form-control"
                      [value]="profile()?.user?.username"
                      disabled
                    >
                    <small class="text-muted">Le nom d'utilisateur ne peut pas être modifié</small>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">E-mail</label>
                    <input
                      type="email"
                      class="form-control"
                      [(ngModel)]="formData.email"
                      name="email"
                    >
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label class="form-label">Prénom</label>
                    <input
                      type="text"
                      class="form-control"
                      [(ngModel)]="formData.first_name"
                      name="firstName"
                    >
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">Nom</label>
                    <input
                      type="text"
                      class="form-control"
                      [(ngModel)]="formData.last_name"
                      name="lastName"
                    >
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label class="form-label">Fuseau horaire</label>
                    <select class="form-select" [(ngModel)]="formData.tz" name="timezone">
                      @for (tz of timezones; track tz) {
                        <option [value]="tz">{{ tz }}</option>
                      }
                    </select>
                  </div>
                </div>

                <button type="submit" class="btn btn-success" [disabled]="saving()">
                  @if (saving()) {
                    <span class="spinner-border spinner-border-sm me-2"></span>
                  }
                  Enregistrer les modifications
                </button>
              </form>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Statistiques</h5>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between">
                  <span>Points totaux</span>
                  <strong>{{ profile()?.total_points || 0 }}</strong>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                  <span>Points gagnés</span>
                  <strong>{{ profile()?.points_won || 0 }}</strong>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                  <span>Admin</span>
                  <span>{{ profile()?.is_admin ? 'Oui' : 'Non' }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    }
  `
})
export class ProfileComponent implements OnInit {
  private readonly authService = inject(AuthService);

  profile = signal<Profile | null>(null);
  loading = signal(true);
  saving = signal(false);
  error = signal<string | null>(null);
  success = signal(false);

  formData = {
    email: '',
    first_name: '',
    last_name: '',
    tz: 'Europe/Paris'
  };

  timezones = [
    'Europe/Paris',
    'Europe/London',
    'Europe/Berlin',
    'Europe/Madrid',
    'Europe/Rome',
    'America/New_York',
    'America/Los_Angeles',
    'America/Chicago',
    'Asia/Tokyo',
    'Asia/Shanghai',
    'Australia/Sydney',
    'UTC'
  ];

  ngOnInit(): void {
    this.authService.loadProfile().subscribe({
      next: () => {
        const profile = this.authService.profile();
        if (profile) {
          this.profile.set(profile);
          this.formData = {
            email: profile.user.email,
            first_name: profile.user.first_name,
            last_name: profile.user.last_name,
            tz: profile.tz
          };
        }
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  onSubmit(): void {
    this.error.set(null);
    this.success.set(false);
    this.saving.set(true);

    this.authService.updateProfile({
      user: {
        id: this.profile()!.user.id,
        username: this.profile()!.user.username,
        email: this.formData.email,
        first_name: this.formData.first_name,
        last_name: this.formData.last_name
      },
      tz: this.formData.tz
    } as Profile).subscribe({
      next: (updatedProfile) => {
        this.profile.set(updatedProfile);
        this.saving.set(false);
        this.success.set(true);
      },
      error: (err) => {
        this.saving.set(false);
        this.error.set(err.message || 'Échec de la mise à jour du profil.');
      }
    });
  }
}
