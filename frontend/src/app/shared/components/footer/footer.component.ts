import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [],
  template: `
    <footer class="footer mt-auto py-3 bg-light">
      <div class="container text-center">
        <span class="text-muted">Betwit - Jeu de paris Rugby &copy; {{ currentYear }}</span>
      </div>
    </footer>
  `
})
export class FooterComponent {
  currentYear = new Date().getFullYear();
}
