import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { MatchBet, MatchBetCreate, TournamentBet, TournamentBetCreate, BetPoint } from '../models';

@Injectable({
  providedIn: 'root'
})
export class BetService {
  private readonly api = inject(ApiService);

  // Match Bets
  getMatchBets(): Observable<MatchBet[]> {
    return this.api.get<MatchBet[]>('/matchbets/');
  }

  getMatchBetById(id: number): Observable<MatchBet> {
    return this.api.get<MatchBet>(`/matchbets/${id}/`);
  }

  createMatchBet(bet: MatchBetCreate): Observable<MatchBet> {
    return this.api.post<MatchBet>('/matchbets/', bet);
  }

  updateMatchBet(id: number, bet: Partial<MatchBetCreate>): Observable<MatchBet> {
    return this.api.patch<MatchBet>(`/matchbets/${id}/`, bet);
  }

  deleteMatchBet(id: number): Observable<void> {
    return this.api.delete<void>(`/matchbets/${id}/`);
  }

  // Tournament Bets
  getTournamentBets(): Observable<TournamentBet[]> {
    return this.api.get<TournamentBet[]>('/tournamentbets/');
  }

  getTournamentBetById(id: number): Observable<TournamentBet> {
    return this.api.get<TournamentBet>(`/tournamentbets/${id}/`);
  }

  createTournamentBet(bet: TournamentBetCreate): Observable<TournamentBet> {
    return this.api.post<TournamentBet>('/tournamentbets/', bet);
  }

  updateTournamentBet(id: number, bet: Partial<TournamentBetCreate>): Observable<TournamentBet> {
    return this.api.patch<TournamentBet>(`/tournamentbets/${id}/`, bet);
  }

  deleteTournamentBet(id: number): Observable<void> {
    return this.api.delete<void>(`/tournamentbets/${id}/`);
  }

  // Bet Points (for prognosis/history)
  getBetPoints(): Observable<BetPoint[]> {
    return this.api.get<BetPoint[]>('/betpoints/');
  }
}
