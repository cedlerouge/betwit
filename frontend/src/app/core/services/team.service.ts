import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Team } from '../models';

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  private readonly api = inject(ApiService);

  getAll(): Observable<Team[]> {
    return this.api.get<Team[]>('/teams/');
  }

  getById(id: number): Observable<Team> {
    return this.api.get<Team>(`/teams/${id}/`);
  }
}
