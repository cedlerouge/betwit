import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { UserRanking } from '../models';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly api = inject(ApiService);

  getRankings(): Observable<UserRanking[]> {
    return this.api.get<UserRanking[]>('/rankings/');
  }
}
