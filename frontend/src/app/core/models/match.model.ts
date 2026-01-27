import { Team } from './team.model';
import { Tournament } from './tournament.model';

export interface Match {
  id: number;
  tournament: string;
  date: string;
  cup_round: string;
  home_team: string;
  home_team_score: number;
  home_team_tries: number;
  home_team_bonus: string;
  away_team: string;
  away_team_score: number;
  away_team_tries: number;
  away_team_bonus: string;
  card: boolean;
  drop_goal: boolean;
  fight: boolean;
  odds: number;
  jokerbet_text: string;
  jokerbet_response: boolean | null;
  jokerbet_win_pts: number;
  jokerbet_lose_pts: number;
}

export interface MatchDetail {
  id: number;
  tournament: Tournament;
  date: string;
  cup_round: string;
  home_team: Team;
  home_team_score: number;
  home_team_tries: number;
  home_team_bonus: string;
  away_team: Team;
  away_team_score: number;
  away_team_tries: number;
  away_team_bonus: string;
  card: boolean;
  drop_goal: boolean;
  fight: boolean;
  odds: number;
  jokerbet_text: string;
  jokerbet_response: boolean | null;
  jokerbet_win_pts: number;
  jokerbet_lose_pts: number;
  created_date: string;
  modified_date: string;
}

export interface MatchRating {
  ht_rating: number;
  at_rating: number;
  null_rating: number;
  total_votes: number;
}

export interface MatchWithRating extends Match {
  rating: MatchRating | null;
}
