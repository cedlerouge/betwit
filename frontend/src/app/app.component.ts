import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { FooterComponent } from './shared/components/footer/footer.component';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FooterComponent],
  template: `
    <div class="d-flex flex-column min-vh-100">
      <app-navbar />
      <main class="container py-4 flex-grow-1">
        <router-outlet />
      </main>
      <app-footer />
    </div>
  `,
  styles: []
})
export class AppComponent implements OnInit {
  private readonly authService = inject(AuthService);

  ngOnInit(): void {
    if (this.authService.isAuthenticated()) {
      this.authService.loadProfile().subscribe();
    }
  }
}
