export type Tier = "free" | "holder" | "pro";
export type NameTier = "common" | "uncommon" | "rare" | "legendary" | "mythic" | "invalid";

export interface ScoreBreakdown {
  word: number;
  palindrome: number;
  repetition: number;
  rarity: number;
  structure: number;
}

export interface NameAnalysis {
  name: string;
  valid: boolean;
  score: number;
  tier: NameTier;
  breakdown: ScoreBreakdown;
  tags: string[];
  reasons: string[];
  is_dictionary_word: boolean;
  is_palindrome: boolean;
  repeat_signature: string;
}

export interface MetaResponse {
  alphabet: string;
  alphabet_size?: number;
  name_length?: number;
  total_name_space: number;
  dictionary_word_names?: number;
  solid_letter_names?: number;
}

export interface AccessResult {
  address: string;
  zen_balance: number;
  tier: Tier;
  source: "offline-sim" | "explorer";
}

export interface SearchResponse {
  count: number;
  tier: string;
  results: NameAnalysis[];
}

export interface GateError {
  error: string;
  message: string;
  your_tier: string;
  your_zen_balance: number;
  required_tier: string;
  how_to_unlock: string;
}
