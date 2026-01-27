import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { UserRanking, MatchWithRating, TournamentInfo } from '../models';
import { TeamStat } from '../models';

export interface HomeData {
  top_players: UserRanking[];
  upcoming_matches: MatchWithRating[];
  standings: TeamStat[];
  active_tournament: TournamentInfo | null;
}

@Injectable({
  providedIn: 'root'
})
export class HomeService {
  private readonly api = inject(ApiService);

  getHomeData(): Observable<HomeData> {
    return this.api.get<HomeData>('/home/');
  }
}
