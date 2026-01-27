import { Routes } from '@angular/router';
import { authGuard, noAuthGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent),
    canActivate: [noAuthGuard]
  },
  {
    path: 'register',
    loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent),
    canActivate: [noAuthGuard]
  },
  {
    path: 'password-reset',
    loadComponent: () => import('./features/auth/password-reset/password-reset.component').then(m => m.PasswordResetComponent),
    canActivate: [noAuthGuard]
  },
  {
    path: 'tournaments',
    loadComponent: () => import('./features/tournaments/list/tournament-list.component').then(m => m.TournamentListComponent)
  },
  {
    path: 'tournaments/:id',
    loadComponent: () => import('./features/tournaments/detail/tournament-detail.component').then(m => m.TournamentDetailComponent)
  },
  {
    path: 'matches',
    loadComponent: () => import('./features/matches/list/match-list.component').then(m => m.MatchListComponent)
  },
  {
    path: 'matches/:id/bet',
    loadComponent: () => import('./features/matches/bet-form/match-bet-form.component').then(m => m.MatchBetFormComponent),
    canActivate: [authGuard]
  },
  {
    path: 'my-bets',
    loadComponent: () => import('./features/bets/my-bets/my-bets.component').then(m => m.MyBetsComponent),
    canActivate: [authGuard]
  },
  {
    path: 'tournament-bet',
    loadComponent: () => import('./features/bets/tournament-bet/tournament-bet.component').then(m => m.TournamentBetComponent),
    canActivate: [authGuard]
  },
  {
    path: 'prognosis',
    loadComponent: () => import('./features/bets/prognosis/prognosis.component').then(m => m.PrognosisComponent)
  },
  {
    path: 'rankings',
    loadComponent: () => import('./features/rankings/rankings.component').then(m => m.RankingsComponent)
  },
  {
    path: 'profile',
    loadComponent: () => import('./features/profile/profile.component').then(m => m.ProfileComponent),
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: ''
  }
];
