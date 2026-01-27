export interface MatchBet {
  id: number;
  player: string;
  match: number;
  home_team_score: number;
  home_team_tries: number;
  home_team_bonus: 'Null' | 'Defense' | 'Attack';
  away_team_score: number;
  away_team_tries: number;
  away_team_bonus: 'Null' | 'Defense' | 'Attack';
  card: boolean;
  drop_goal: boolean;
  fight: boolean;
  jokerbet_text: string | null;
  jokerbet_value: boolean | null;
  points_won: number;
  created_date: string;
  modified_date: string;
}

export interface MatchBetCreate {
  match: number;
  home_team_score: number;
  home_team_tries: number;
  home_team_bonus: 'Null' | 'Defense' | 'Attack';
  away_team_score: number;
  away_team_tries: number;
  away_team_bonus: 'Null' | 'Defense' | 'Attack';
  card: boolean;
  drop_goal: boolean;
  fight: boolean;
  jokerbet_text?: string;
  jokerbet_value?: boolean;
}

export interface TournamentBet {
  id: number;
  player: string;
  tournament: number;
  tournament_name: string;
  first_team: number;
  first_team_name: string;
  second_team: number;
  second_team_name: string;
  third_team: number;
  third_team_name: string;
  fourth_team: number;
  fourth_team_name: string;
  fifth_team: number;
  fifth_team_name: string;
  sixth_team: number;
  sixth_team_name: string;
  grand_slam: boolean;
  wooden_spoon: boolean;
  points_won: number | null;
  created_date: string;
  modified_date: string;
}

export interface TournamentBetCreate {
  tournament: number;
  first_team: number;
  second_team: number;
  third_team: number;
  fourth_team: number;
  fifth_team: number;
  sixth_team: number;
  grand_slam: boolean;
  wooden_spoon: boolean;
}

export interface BetPoint {
  id: number;
  player: number;
  match: number;
  matchbet: number;
  points_won: number;
}
