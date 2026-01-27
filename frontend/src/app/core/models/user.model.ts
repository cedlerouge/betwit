export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Profile {
  id: number;
  user: User;
  is_admin: boolean;
  tz: string;
  points_won: number;
  total_points: number;
  language?: string;
}

export interface UserRanking {
  rank: number;
  user_id: number;
  username: string;
  total_points: number;
  matches_bet: number;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}
