import { toast } from "sonner";
import type { NameAnalysis, MetaResponse, AccessResult, SearchResponse } from "../types";

const BASE = (import.meta.env.VITE_API_BASE as string) || "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw { status: res.status, detail: body?.detail ?? body };
  }
  return res.json();
}

export async function analyzeName(name: string): Promise<NameAnalysis> {
  try {
    return await get<NameAnalysis>(`/analyze?name=${encodeURIComponent(name)}`);
  } catch {
    toast.error("Engine unreachable. Running in offline demo mode.");
    return getDemoAnalysis(name);
  }
}

export async function getMeta(): Promise<MetaResponse> {
  try {
    return await get<MetaResponse>("/meta");
  } catch {
    return { alphabet: "ABEHIKMNSTUVWXYZ", total_name_space: 16777216, dictionary_word_names: 1219, solid_letter_names: 16 };
  }
}

export async function getAccess(address: string): Promise<AccessResult> {
  return get<AccessResult>(`/access?address=${encodeURIComponent(address)}`);
}

export async function searchNames(params: {
  contains?: string;
  starts_with?: string;
  ends_with?: string;
  only_words?: boolean;
  min_score?: number;
  limit?: number;
  address?: string;
}): Promise<SearchResponse> {
  const q = new URLSearchParams();
  if (params.contains) q.set("contains", params.contains);
  if (params.starts_with) q.set("starts_with", params.starts_with);
  if (params.ends_with) q.set("ends_with", params.ends_with);
  q.set("only_words", String(params.only_words ?? true));
  if (params.min_score !== undefined) q.set("min_score", String(params.min_score));
  if (params.limit) q.set("limit", String(params.limit));
  if (params.address) q.set("address", params.address);
  return get<SearchResponse>(`/search?${q.toString()}`);
}

export async function getLeaderboard(limit = 25, address = ""): Promise<{ tier: string; results: NameAnalysis[] }> {
  return get(`/leaderboard?limit=${limit}&address=${encodeURIComponent(address)}`);
}

function getDemoAnalysis(name: string): NameAnalysis {
  const upper = name.toUpperCase();
  const DEMO: Record<string, NameAnalysis> = {
    ZENITH: { name: "ZENITH", valid: true, score: 51, tier: "legendary", breakdown: { word: 45, palindrome: 0, repetition: 0, rarity: 6, structure: 0 }, tags: ["dictionary-word"], reasons: ["Real English dictionary word — only 1,219 of 16,777,216 names qualify."], is_dictionary_word: true, is_palindrome: false, repeat_signature: "111111" },
    AAAAAA: { name: "AAAAAA", valid: true, score: 72, tier: "legendary", breakdown: { word: 0, palindrome: 22, repetition: 30, rarity: 0, structure: 14 }, tags: ["solid", "palindrome", "mirror-half"], reasons: ["Solid name — single letter repeated six times (only 16 exist).", "Reads the same forwards and backwards."], is_dictionary_word: false, is_palindrome: true, repeat_signature: "6" },
  };
  return DEMO[upper] ?? { name: upper, valid: true, score: 8, tier: "common", breakdown: { word: 0, palindrome: 0, repetition: 0, rarity: 8, structure: 0 }, tags: [], reasons: ["Valid HACD name with no premium pattern detected."], is_dictionary_word: false, is_palindrome: false, repeat_signature: "" };
}
