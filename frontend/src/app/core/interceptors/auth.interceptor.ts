import { HttpInterceptorFn, HttpRequest, HttpHandlerFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  const authService = inject(AuthService);
  const token = authService.getAccessToken();

  // Skip auth header for token endpoints
  if (req.url.includes('/auth/token')) {
    return next(req);
  }

  let authReq = req;
  if (token) {
    authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && token) {
        // Try to refresh the token
        return authService.refreshToken().pipe(
          switchMap(newTokens => {
            if (newTokens) {
              const retryReq = req.clone({
                setHeaders: {
                  Authorization: `Bearer ${newTokens.access}`
                }
              });
              return next(retryReq);
            }
            authService.logout();
            return throwError(() => error);
          }),
          catchError(() => {
            authService.logout();
            return throwError(() => error);
          })
        );
      }
      return throwError(() => error);
    })
  );
};
