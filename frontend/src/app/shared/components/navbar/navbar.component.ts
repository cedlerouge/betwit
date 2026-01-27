import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { NgClass } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, NgClass],
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
      <div class="container">
        <a class="navbar-brand" routerLink="/">
          <strong>Betwit</strong>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          (click)="isCollapsed = !isCollapsed"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" [ngClass]="{ show: !isCollapsed }" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <a class="nav-link" routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">
                Accueil
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/tournaments" routerLinkActive="active">
                Tournois
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/matches" routerLinkActive="active">
                Matchs
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/rankings" routerLinkActive="active">
                Classement
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/prognosis" routerLinkActive="active">
                Pronostics
              </a>
            </li>
          </ul>
          <ul class="navbar-nav align-items-center">
            @if (authService.isAuthenticated()) {
              <li class="nav-item">
                <a class="nav-link" routerLink="/my-bets" routerLinkActive="active">
                  Mes Paris
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" routerLink="/tournament-bet" routerLinkActive="active">
                  Pari Tournoi
                </a>
              </li>
              <li class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  (click)="$event.preventDefault(); userMenuOpen = !userMenuOpen"
                >
                  {{ authService.user()?.username || 'Utilisateur' }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end" [ngClass]="{ show: userMenuOpen }">
                  <li>
                    <a class="dropdown-item" routerLink="/profile" (click)="userMenuOpen = false">Profil</a>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item" href="#" (click)="logout($event)">Déconnexion</a>
                  </li>
                </ul>
              </li>
            } @else {
              <li class="nav-item">
                <a class="nav-link" routerLink="/login" routerLinkActive="active">Connexion</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" routerLink="/register" routerLinkActive="active">Inscription</a>
              </li>
            }
          </ul>
        </div>
      </div>
    </nav>
  `
})
export class NavbarComponent {
  readonly authService = inject(AuthService);
  isCollapsed = true;
  userMenuOpen = false;

  logout(event: Event): void {
    event.preventDefault();
    this.userMenuOpen = false;
    this.authService.logout();
  }
}
