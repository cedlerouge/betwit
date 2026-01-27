import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Match, MatchDetail } from '../models';

export interface MatchFilters {
  tournament?: number;
  date_from?: string;
  date_to?: string;
  upcoming?: boolean;
  home_team?: number;
  away_team?: number;
  cup_round?: string;
}

@Injectable({
  providedIn: 'root'
})
export class MatchService {
  private readonly api = inject(ApiService);

  getAll(filters?: MatchFilters): Observable<Match[]> {
    return this.api.get<Match[]>('/matches/', filters as Record<string, string | number | boolean>);
  }

  getById(id: number): Observable<MatchDetail> {
    return this.api.get<MatchDetail>(`/matches/${id}/`);
  }

  getUpcoming(limit?: number): Observable<Match[]> {
    const params: MatchFilters = { upcoming: true };
    return this.api.get<Match[]>('/matches/', params as Record<string, string | number | boolean>);
  }

  getByTournament(tournamentId: number): Observable<Match[]> {
    return this.api.get<Match[]>('/matches/', { tournament: tournamentId });
  }
}
