import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-password-reset',
  standalone: true,
  imports: [FormsModule, RouterLink],
  template: `
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h4 class="mb-0">Réinitialiser le mot de passe</h4>
          </div>
          <div class="card-body">
            @if (error()) {
              <div class="alert alert-danger" role="alert">
                {{ error() }}
              </div>
            }
            @if (success()) {
              <div class="alert alert-success" role="alert">
                Si un compte existe avec cette adresse e-mail, un lien de réinitialisation a été envoyé. Veuillez vérifier votre boîte de réception.
              </div>
            } @else {
              <p class="text-muted mb-3">
                Entrez votre adresse e-mail et nous vous enverrons un lien pour réinitialiser votre mot de passe.
              </p>
              <form (ngSubmit)="onSubmit()">
                <div class="mb-3">
                  <label for="email" class="form-label">E-mail</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    [(ngModel)]="email"
                    name="email"
                    required
                    [disabled]="loading()"
                  >
                </div>
                <div class="d-grid">
                  <button type="submit" class="btn btn-success" [disabled]="loading()">
                    @if (loading()) {
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    }
                    Envoyer le lien
                  </button>
                </div>
              </form>
            }
          </div>
          <div class="card-footer text-center">
            <a routerLink="/login">Retour à la connexion</a>
          </div>
        </div>
      </div>
    </div>
  `
})
export class PasswordResetComponent {
  private readonly authService = inject(AuthService);

  email = '';
  error = signal<string | null>(null);
  success = signal(false);
  loading = signal(false);

  onSubmit(): void {
    this.error.set(null);
    this.loading.set(true);

    this.authService.requestPasswordReset(this.email).subscribe({
      next: () => {
        this.loading.set(false);
        this.success.set(true);
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err.message || 'Échec de l\'envoi du lien. Veuillez réessayer.');
      }
    });
  }
}
