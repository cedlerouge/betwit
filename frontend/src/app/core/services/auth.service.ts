import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, of } from 'rxjs';
import { AuthTokens, LoginCredentials, RegisterData, User, Profile } from '../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly baseUrl = '/api/auth';

  private readonly _tokens = signal<AuthTokens | null>(this.loadTokens());
  private readonly _user = signal<User | null>(null);
  private readonly _profile = signal<Profile | null>(null);
  private readonly _loading = signal<boolean>(false);

  readonly tokens = this._tokens.asReadonly();
  readonly user = this._user.asReadonly();
  readonly profile = this._profile.asReadonly();
  readonly loading = this._loading.asReadonly();
  readonly isAuthenticated = computed(() => !!this._tokens());

  private loadTokens(): AuthTokens | null {
    const tokens = localStorage.getItem('auth_tokens');
    return tokens ? JSON.parse(tokens) : null;
  }

  private saveTokens(tokens: AuthTokens): void {
    localStorage.setItem('auth_tokens', JSON.stringify(tokens));
    this._tokens.set(tokens);
  }

  private clearTokens(): void {
    localStorage.removeItem('auth_tokens');
    this._tokens.set(null);
    this._user.set(null);
    this._profile.set(null);
  }

  getAccessToken(): string | null {
    return this._tokens()?.access ?? null;
  }

  login(credentials: LoginCredentials): Observable<AuthTokens> {
    this._loading.set(true);
    return this.http.post<AuthTokens>(`${this.baseUrl}/token/`, credentials).pipe(
      tap(tokens => {
        this.saveTokens(tokens);
        this.loadProfile().subscribe();
        this._loading.set(false);
      }),
      catchError(error => {
        this._loading.set(false);
        throw error;
      })
    );
  }

  register(data: RegisterData): Observable<User> {
    this._loading.set(true);
    return this.http.post<User>(`${this.baseUrl}/register/`, data).pipe(
      tap(() => this._loading.set(false)),
      catchError(error => {
        this._loading.set(false);
        throw error;
      })
    );
  }

  logout(): void {
    this.clearTokens();
    this.router.navigate(['/login']);
  }

  refreshToken(): Observable<AuthTokens | null> {
    const tokens = this._tokens();
    if (!tokens?.refresh) {
      return of(null);
    }

    return this.http.post<AuthTokens>(`${this.baseUrl}/token/refresh/`, {
      refresh: tokens.refresh
    }).pipe(
      tap(newTokens => {
        this.saveTokens({ ...tokens, access: newTokens.access });
      }),
      catchError(() => {
        this.clearTokens();
        return of(null);
      })
    );
  }

  loadProfile(): Observable<Profile | null> {
    if (!this.isAuthenticated()) {
      return of(null);
    }

    return this.http.get<Profile[]>('/api/profile/').pipe(
      tap(profiles => {
        if (profiles.length > 0) {
          this._profile.set(profiles[0]);
          this._user.set(profiles[0].user);
        }
      }),
      catchError(() => of(null))
    ) as Observable<Profile | null>;
  }

  updateProfile(data: Partial<Profile>): Observable<Profile> {
    return this.http.put<Profile>('/api/profile/me/', data).pipe(
      tap(profile => {
        this._profile.set(profile);
        this._user.set(profile.user);
      })
    );
  }

  requestPasswordReset(email: string): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.baseUrl}/password-reset/`, { email });
  }

  confirmPasswordReset(uidb64: string, token: string, password: string, password_confirm: string): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.baseUrl}/password-reset/${uidb64}/${token}/`, {
      password,
      password_confirm
    });
  }
}
