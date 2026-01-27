import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Tournament } from '../models';
import { TeamStat } from '../models';

@Injectable({
  providedIn: 'root'
})
export class TournamentService {
  private readonly api = inject(ApiService);

  getAll(): Observable<Tournament[]> {
    return this.api.get<Tournament[]>('/tournaments/');
  }

  getById(id: number): Observable<Tournament> {
    return this.api.get<Tournament>(`/tournaments/${id}/`);
  }

  getActive(): Observable<Tournament[]> {
    return this.api.get<Tournament[]>('/tournaments/', { state: '1' });
  }

  getTeamStats(tournamentId?: number): Observable<TeamStat[]> {
    const params: Record<string, string | number | boolean> = {};
    if (tournamentId) {
      params['tournament'] = tournamentId;
    }
    return this.api.get<TeamStat[]>('/teamstats/', params);
  }
}
