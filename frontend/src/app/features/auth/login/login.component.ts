import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink],
  template: `
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h4 class="mb-0">Connexion</h4>
          </div>
          <div class="card-body">
            @if (error()) {
              <div class="alert alert-danger" role="alert">
                {{ error() }}
              </div>
            }
            <form (ngSubmit)="onSubmit()">
              <div class="mb-3">
                <label for="username" class="form-label">Nom d'utilisateur</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  [(ngModel)]="username"
                  name="username"
                  required
                  [disabled]="loading()"
                >
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Mot de passe</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  [(ngModel)]="password"
                  name="password"
                  required
                  [disabled]="loading()"
                >
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-success" [disabled]="loading()">
                  @if (loading()) {
                    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                  }
                  Se connecter
                </button>
              </div>
            </form>
            <div class="mt-3 text-center">
              <a routerLink="/password-reset" class="text-muted">Mot de passe oublié ?</a>
            </div>
          </div>
          <div class="card-footer text-center">
            Pas encore de compte ? <a routerLink="/register">S'inscrire</a>
          </div>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  username = '';
  password = '';
  error = signal<string | null>(null);
  loading = signal(false);

  onSubmit(): void {
    this.error.set(null);
    this.loading.set(true);

    this.authService.login({ username: this.username, password: this.password }).subscribe({
      next: () => {
        const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
        this.router.navigateByUrl(returnUrl);
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err.message || 'Échec de la connexion. Veuillez vérifier vos identifiants.');
      }
    });
  }
}
