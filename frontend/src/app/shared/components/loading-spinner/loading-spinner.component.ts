import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [],
  template: `
    @if (loading) {
      <div class="d-flex justify-content-center align-items-center" [style.min-height]="minHeight">
        <div class="spinner-border text-success" role="status">
          <span class="visually-hidden">Chargement...</span>
        </div>
      </div>
    }
  `
})
export class LoadingSpinnerComponent {
  @Input() loading = false;
  @Input() minHeight = '200px';
}
