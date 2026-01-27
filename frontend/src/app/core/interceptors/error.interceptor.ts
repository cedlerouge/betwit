import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'Une erreur est survenue';

      if (error.error instanceof ErrorEvent) {
        // Client-side error
        errorMessage = error.error.message;
      } else {
        // Server-side error
        if (error.status === 0) {
          errorMessage = 'Impossible de se connecter au serveur. Vérifiez votre connexion internet.';
        } else if (error.status === 400) {
          errorMessage = extractErrorMessage(error.error) || 'Requête invalide';
        } else if (error.status === 401) {
          errorMessage = 'Authentification requise. Veuillez vous connecter.';
        } else if (error.status === 403) {
          errorMessage = 'Vous n\'avez pas la permission d\'effectuer cette action.';
        } else if (error.status === 404) {
          errorMessage = 'Ressource non trouvée.';
        } else if (error.status >= 500) {
          errorMessage = 'Erreur serveur. Veuillez réessayer plus tard.';
        }
      }

      console.error('HTTP Error:', errorMessage, error);
      return throwError(() => ({ message: errorMessage, originalError: error }));
    })
  );
};

function extractErrorMessage(errorBody: unknown): string | null {
  if (!errorBody) return null;

  if (typeof errorBody === 'string') {
    return errorBody;
  }

  if (typeof errorBody === 'object') {
    const obj = errorBody as Record<string, unknown>;
    // Common DRF error formats
    if (obj['detail']) {
      return String(obj['detail']);
    }
    if (obj['non_field_errors']) {
      const errors = obj['non_field_errors'];
      return Array.isArray(errors) ? errors.join(', ') : String(errors);
    }
    // Field-specific errors
    const fieldErrors: string[] = [];
    for (const [key, value] of Object.entries(obj)) {
      if (Array.isArray(value)) {
        fieldErrors.push(`${key}: ${value.join(', ')}`);
      } else if (typeof value === 'string') {
        fieldErrors.push(`${key}: ${value}`);
      }
    }
    if (fieldErrors.length > 0) {
      return fieldErrors.join('; ');
    }
  }

  return null;
}
