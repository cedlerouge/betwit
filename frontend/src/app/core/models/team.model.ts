export interface Team {
  id: number;
  name: string;
  nationality: string;
  logo: string | null;
  flag: string | null;
}

export interface TeamStat {
  id: number;
  team: Team;
  tournament: Tournament;
  played: number;
  win: number;
  draw: number;
  lose: number;
  ptsfor: number;
  ptsagainst: number;
  ptsdiff: number;
  tryfor: number;
  tryagainst: number;
  trybonus: number;
  losebonus: number;
  points: number;
}

import { Tournament } from './tournament.model';
