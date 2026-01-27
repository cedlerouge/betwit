export interface Tournament {
  id: number;
  name: string;
  year: number;
  begins: string;
  state: '1' | '2' | '3';
}

export interface TournamentInfo {
  id: number;
  name: string;
}
