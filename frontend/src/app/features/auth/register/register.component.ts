import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, RouterLink],
  template: `
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h4 class="mb-0">Inscription</h4>
          </div>
          <div class="card-body">
            @if (error()) {
              <div class="alert alert-danger" role="alert">
                {{ error() }}
              </div>
            }
            @if (success()) {
              <div class="alert alert-success" role="alert">
                Inscription réussie ! Vous pouvez maintenant <a routerLink="/login">vous connecter</a>.
              </div>
            } @else {
              <form (ngSubmit)="onSubmit()">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label">Prénom</label>
                    <input
                      type="text"
                      class="form-control"
                      id="firstName"
                      [(ngModel)]="formData.first_name"
                      name="firstName"
                      [disabled]="loading()"
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label">Nom</label>
                    <input
                      type="text"
                      class="form-control"
                      id="lastName"
                      [(ngModel)]="formData.last_name"
                      name="lastName"
                      [disabled]="loading()"
                    >
                  </div>
                </div>
                <div class="mb-3">
                  <label for="username" class="form-label">Nom d'utilisateur *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="username"
                    [(ngModel)]="formData.username"
                    name="username"
                    required
                    [disabled]="loading()"
                  >
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">E-mail *</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    [(ngModel)]="formData.email"
                    name="email"
                    required
                    [disabled]="loading()"
                  >
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Mot de passe *</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    [(ngModel)]="formData.password"
                    name="password"
                    required
                    minlength="8"
                    [disabled]="loading()"
                  >
                  <div class="form-text">Le mot de passe doit contenir au moins 8 caractères.</div>
                </div>
                <div class="mb-3">
                  <label for="passwordConfirm" class="form-label">Confirmer le mot de passe *</label>
                  <input
                    type="password"
                    class="form-control"
                    id="passwordConfirm"
                    [(ngModel)]="formData.password_confirm"
                    name="passwordConfirm"
                    required
                    [disabled]="loading()"
                  >
                </div>
                <div class="d-grid">
                  <button type="submit" class="btn btn-success" [disabled]="loading()">
                    @if (loading()) {
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    }
                    S'inscrire
                  </button>
                </div>
              </form>
            }
          </div>
          <div class="card-footer text-center">
            Déjà un compte ? <a routerLink="/login">Se connecter</a>
          </div>
        </div>
      </div>
    </div>
  `
})
export class RegisterComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  formData = {
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: ''
  };

  error = signal<string | null>(null);
  success = signal(false);
  loading = signal(false);

  onSubmit(): void {
    this.error.set(null);

    if (this.formData.password !== this.formData.password_confirm) {
      this.error.set('Les mots de passe ne correspondent pas.');
      return;
    }

    this.loading.set(true);

    this.authService.register(this.formData).subscribe({
      next: () => {
        this.loading.set(false);
        this.success.set(true);
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err.message || 'Échec de l\'inscription. Veuillez réessayer.');
      }
    });
  }
}
