import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Trophy, Info, ExternalLink, Lock, Zap, ChevronRight, Copy, Check, X, Gem } from "lucide-react";
import { toast } from "sonner";
import { analyzeName, getMeta, getAccess, searchNames, getLeaderboard } from "./lib/api";
import type { NameAnalysis, MetaResponse, AccessResult, NameTier, GateError } from "./types";
import "./index.css";

const ALPHABET = "ABEHIKMNSTUVWXYZ";
const TIER_COLOR: Record<NameTier | string, string> = {
  common: "#64748B", uncommon: "#22C55E", rare: "#22D3EE",
  legendary: "#7C5CFF", mythic: "#F59E0B", invalid: "#EF4444",
};
const TIER_LABEL: Record<string, string> = {
  common: "Common", uncommon: "Uncommon", rare: "Rare",
  legendary: "Legendary", mythic: "Mythic", invalid: "Invalid",
};

function cn(...classes: (string | undefined | false | null)[]) {
  return classes.filter(Boolean).join(" ");
}

function ScoreRing({ score, tier, size = 120 }: { score: number; tier: string; size?: number }) {
  const [displayed, setDisplayed] = useState(0);
  const r = (size / 2) - 10;
  const circ = 2 * Math.PI * r;
  const offset = circ - (displayed / 100) * circ;
  const color = TIER_COLOR[tier] ?? "#64748B";

  useEffect(() => {
    let start: number | null = null;
    const duration = 800;
    const animate = (ts: number) => {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      setDisplayed(Math.round(score * ease));
      if (progress < 1) requestAnimationFrame(animate);
    };
    const id = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(id);
  }, [score]);

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="rotate-[-90deg]">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="6" />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth="6"
          strokeLinecap="round" strokeDasharray={circ}
          strokeDashoffset={offset} className="ring-path"
          style={{ filter: `drop-shadow(0 0 6px ${color}60)` }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="font-mono font-bold text-white" style={{ fontSize: size * 0.25 }}>{displayed}</span>
        <span className="font-mono text-xs uppercase tracking-widest" style={{ color, fontSize: size * 0.08 }}>
          {TIER_LABEL[tier]}
        </span>
      </div>
    </div>
  );
}

function TierBadge({ tier, label }: { tier: string; label?: string }) {
  const color = TIER_COLOR[tier] ?? "#64748B";
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-mono font-medium border"
      style={{ borderColor: `${color}40`, color, backgroundColor: `${color}15` }}>
      {label ?? TIER_LABEL[tier]}
    </span>
  );
}

function TagBadge({ tag }: { tag: string }) {
  const TAG_STYLE: Record<string, { color: string; icon: string }> = {
    "dictionary-word": { color: "#22D3EE", icon: "📖" },
    "palindrome": { color: "#7C5CFF", icon: "↔" },
    "solid": { color: "#F59E0B", icon: "◆" },
    "mirror-half": { color: "#A78BFA", icon: "🪞" },
    "rare-letters": { color: "#F97316", icon: "✦" },
    "heavy-repeat": { color: "#8B5CF6", icon: "⟳" },
    "triple": { color: "#6366F1", icon: "∷" },
    "double-start": { color: "#60A5FA", icon: "‖" },
    "low-alphabet": { color: "#94A3B8", icon: "Aa" },
  };
  const style = TAG_STYLE[tag] ?? { color: "#94A3B8", icon: "·" };
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-mono border"
      style={{ borderColor: `${style.color}30`, color: style.color, backgroundColor: `${style.color}10` }}>
      <span>{style.icon}</span> {tag}
    </span>
  );
}

function BreakdownBar({ breakdown }: { breakdown: NameAnalysis["breakdown"] }) {
  const items = [
    { key: "word", label: "Word", color: "#22D3EE", max: 45 },
    { key: "palindrome", label: "Palindrome", color: "#7C5CFF", max: 22 },
    { key: "repetition", label: "Pattern", color: "#F59E0B", max: 30 },
    { key: "rarity", label: "Rarity", color: "#F97316", max: 18 },
    { key: "structure", label: "Structure", color: "#A78BFA", max: 14 },
  ] as const;

  return (
    <div className="space-y-2 w-full">
      {items.map(({ key, label, color, max }) => {
        const val = breakdown[key] ?? 0;
        const pct = Math.round((val / max) * 100);
        return (
          <div key={key} className="flex items-center gap-3">
            <span className="text-xs font-mono w-20 text-slate-400 shrink-0">{label}</span>
            <div className="flex-1 h-1.5 rounded-full bg-white/5">
              <motion.div className="h-full rounded-full"
                initial={{ width: 0 }} animate={{ width: `${pct}%` }}
                transition={{ duration: 0.6, delay: 0.1 }} style={{ background: color }} />
            </div>
            <span className="text-xs font-mono w-8 text-right" style={{ color }}>{val}</span>
          </div>
        );
      })}
    </div>
  );
}

function NameInput({ onAnalyze, loading }: { onAnalyze: (name: string) => void; loading: boolean }) {
  const [cells, setCells] = useState<string[]>(["Z", "E", "N", "I", "T", "H"]);
  const [invalid, setInvalid] = useState<boolean[]>([false, false, false, false, false, false]);
  const refs = useRef<(HTMLInputElement | null)[]>([]);

  const handleKey = (idx: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace") {
      e.preventDefault();
      const next = [...cells];
      if (next[idx]) { next[idx] = ""; setCells(next); }
      else if (idx > 0) { next[idx - 1] = ""; setCells(next); refs.current[idx - 1]?.focus(); }
    } else if (e.key === "ArrowLeft" && idx > 0) refs.current[idx - 1]?.focus();
    else if (e.key === "ArrowRight" && idx < 5) refs.current[idx + 1]?.focus();
    else if (e.key === "Enter") {
      const name = cells.join("");
      if (name.length === 6) onAnalyze(name);
    }
  };

  const handleInput = (idx: number, e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value.toUpperCase();
    const next = [...cells];
    const inv = [...invalid];

    if (val.length > 1) {
      const pasted = val.replace(/[^A-Z]/g, "").slice(0, 6 - idx);
      for (let i = 0; i < pasted.length; i++) {
        const ch = pasted[i];
        if (ALPHABET.includes(ch)) { next[idx + i] = ch; inv[idx + i] = false; }
        else { next[idx + i] = ch; inv[idx + i] = true; }
      }
      setCells(next); setInvalid(inv);
      const nextIdx = Math.min(idx + pasted.length, 5);
      setTimeout(() => refs.current[nextIdx]?.focus(), 0);
      return;
    }

    const ch = val.slice(-1);
    if (!ch) return;
    if (!ALPHABET.includes(ch)) {
      inv[idx] = true; setInvalid(inv);
      setTimeout(() => { const r = [...invalid]; r[idx] = false; setInvalid(r); }, 600);
      return;
    }
    next[idx] = ch; inv[idx] = false;
    setCells(next); setInvalid(inv);
    if (idx < 5) setTimeout(() => refs.current[idx + 1]?.focus(), 0);
  };

  const name = cells.join("");
  const ready = name.length === 6 && cells.every((c) => ALPHABET.includes(c));

  return (
    <div className="flex flex-col items-center gap-6">
      <div className="flex gap-2">
        {cells.map((ch, i) => (
          <input key={i} ref={(el) => { refs.current[i] = el; }}
            className={cn("name-cell", ch && "filled", invalid[i] && "invalid")}
            value={ch} maxLength={6} autoCorrect="off" autoCapitalize="characters" spellCheck={false}
            inputMode="text"
            onChange={(e) => handleInput(i, e)}
            onKeyDown={(e) => handleKey(i, e)}
            onFocus={(e) => e.target.select()}
            aria-label={`Letter ${i + 1} of HACD name`}
          />
        ))}
      </div>
      <p className="text-xs text-slate-500 font-mono">Valid letters: A B E H I K M N S T U V W X Y Z</p>
      <button onClick={() => ready && onAnalyze(name)} disabled={!ready || loading}
        className={cn(
          "px-8 py-3 rounded-xl font-semibold text-sm transition-all duration-200",
          ready && !loading
            ? "bg-gradient-to-r from-[#7C5CFF] to-[#22D3EE] text-white hover:opacity-90 hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-violet-500/20"
            : "bg-white/5 text-slate-500 cursor-not-allowed"
        )}>
        {loading ? (
          <span className="flex items-center gap-2"><span className="animate-spin">⟳</span> Analyzing…</span>
        ) : (
          <span className="flex items-center gap-2"><Zap size={14} /> Analyze Name</span>
        )}
      </button>
    </div>
  );
}

function AnalyzeResult({ result, onClose }: { result: NameAnalysis; onClose: () => void }) {
  const [copied, setCopied] = useState(false);
  const color = TIER_COLOR[result.tier] ?? "#64748B";

  const copy = () => {
    navigator.clipboard.writeText(`${window.location.origin}?name=${result.name}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isGlowing = result.tier === "mythic" || result.tier === "legendary";

  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}
      className={cn(
        "rounded-2xl border p-6 space-y-6 w-full max-w-2xl mx-auto",
        isGlowing ? "glow-legendary" : ""
      )}
      style={{ borderColor: `${color}30`, background: "rgba(15,15,20,0.8)", backdropFilter: "blur(12px)" }}>

      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-5">
          <ScoreRing score={result.score} tier={result.tier} size={100} />
          <div>
            <div className="hacd-name text-3xl text-white mb-2" style={isGlowing ? { color } : {}}>
              {result.name}
            </div>
            <div className="flex flex-wrap gap-1.5 mt-2">
              {result.tags.map((tag) => <TagBadge key={tag} tag={tag} />)}
              {result.tags.length === 0 && <TierBadge tier={result.tier} />}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={copy} className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors">
            {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
          </button>
          <button onClick={onClose} className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors">
            <X size={14} />
          </button>
        </div>
      </div>

      {result.reasons.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-mono text-slate-500 uppercase tracking-wider">Why this score</p>
          {result.reasons.map((r, i) => (
            <div key={i} className="flex gap-2 text-sm text-slate-300">
              <span style={{ color }}>✦</span> {r}
            </div>
          ))}
        </div>
      )}

      <div>
        <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-3">Score breakdown</p>
        <BreakdownBar breakdown={result.breakdown} />
      </div>
    </motion.div>
  );
}

function StatTicker({ meta }: { meta: MetaResponse | null }) {
  const stats = [
    { label: "possible names", value: (16777216).toLocaleString() },
    { label: "dictionary words", value: (meta?.dictionary_word_names ?? 1219).toLocaleString() },
    { label: "solid names", value: (meta?.solid_letter_names ?? 16).toLocaleString() },
    { label: "letter alphabet", value: "16" },
    { label: "letters per name", value: "6" },
  ];
  return (
    <div className="flex flex-wrap justify-center gap-x-6 gap-y-1 text-xs font-mono text-slate-500">
      {stats.map(({ label, value }, i) => (
        <span key={i}><span className="text-slate-300">{value}</span> {label}</span>
      ))}
    </div>
  );
}

function ConnectModal({ onConnect, onClose }: { onConnect: (a: AccessResult) => void; onClose: () => void }) {
  const [addr, setAddr] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!addr.trim()) return;
    setLoading(true);
    try {
      const res = await getAccess(addr.trim());
      onConnect(res);
      toast.success(`Connected — ${res.tier.toUpperCase()} tier`);
    } catch {
      toast.error("Could not check address. Try again.");
    } finally { setLoading(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md mx-4 rounded-2xl border border-white/10 bg-[#0F0F14] p-6 space-y-5"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-white">Connect address</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white"><X size={16} /></button>
        </div>
        <p className="text-sm text-slate-400">Enter your public Hacash address to check your ZEN balance and unlock holder features.</p>
        <p className="text-xs text-slate-500 border border-green-500/20 bg-green-500/5 rounded-lg px-3 py-2 text-green-400">
          🔒 Read-only. ZENITH never asks for your private key, seed phrase, or signature.
        </p>
        <input value={addr} onChange={(e) => setAddr(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="0x… or Hacash address"
          className="w-full bg-white/4 border border-white/10 rounded-xl px-4 py-3 text-sm font-mono text-white placeholder-slate-600 outline-none focus:border-violet-500/60 focus:bg-violet-500/5 transition-colors" />
        <button onClick={submit} disabled={!addr.trim() || loading}
          className="w-full py-3 rounded-xl font-semibold text-sm bg-gradient-to-r from-[#7C5CFF] to-[#22D3EE] text-white hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity">
          {loading ? "Checking…" : "Check access"}
        </button>
      </motion.div>
    </div>
  );
}

function GatedPanel({ feature, access, gateError, children }: {
  feature: string; access: AccessResult | null; gateError: GateError | null; children: React.ReactNode;
}) {
  const locked = gateError?.error === "insufficient_zen" || (!access && feature !== "free");
  if (!locked) return <>{children}</>;

  return (
    <div className="relative rounded-2xl border border-white/8 overflow-hidden min-h-48">
      <div className="blur-sm pointer-events-none opacity-30">{children}</div>
      <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/50 backdrop-blur-sm gap-4 p-6">
        <div className="p-3 rounded-full border border-violet-500/30 bg-violet-500/10">
          <Lock size={20} className="text-violet-400" />
        </div>
        <div className="text-center space-y-1">
          <p className="font-semibold text-white text-sm">Holder feature</p>
          <p className="text-xs text-slate-400">Stack ≥ 1,000 ZEN to unlock {feature}</p>
          {gateError && (
            <p className="text-xs text-slate-500 font-mono">
              Your balance: {gateError.your_zen_balance} ZEN · {gateError.your_tier}
            </p>
          )}
        </div>
        <a href="https://hacd.it/launchpad" target="_blank" rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-gradient-to-r from-[#7C5CFF] to-[#22D3EE] text-white text-xs font-semibold hover:opacity-90 transition-opacity">
          Get ZEN on HACD Launchpad <ExternalLink size={10} />
        </a>
      </div>
    </div>
  );
}

function SearchPanel({ access }: { access: AccessResult | null }) {
  const [contains, setContains] = useState("");
  const [startsWith, setStartsWith] = useState("");
  const [minScore, setMinScore] = useState(0);
  const [results, setResults] = useState<NameAnalysis[]>([]);
  const [loading, setLoading] = useState(false);
  const [gateError, setGateError] = useState<GateError | null>(null);
  const [activeResult, setActiveResult] = useState<NameAnalysis | null>(null);

  const run = async () => {
    setLoading(true);
    try {
      const data = await searchNames({ contains, starts_with: startsWith, min_score: minScore, limit: 48, address: access?.address ?? "" });
      setResults(data.results);
      setGateError(null);
    } catch (e: any) {
      if (e.status === 402) setGateError(e.detail);
      else toast.error("Search failed");
    } finally { setLoading(false); }
  };

  const inputCls = "bg-white/4 border border-white/10 rounded-xl px-3 py-2 text-sm font-mono text-white placeholder-slate-600 outline-none focus:border-violet-500/60 transition-colors w-full";

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <input value={contains} onChange={(e) => setContains(e.target.value.toUpperCase())} placeholder="contains" className={inputCls} maxLength={6} />
        <input value={startsWith} onChange={(e) => setStartsWith(e.target.value.toUpperCase())} placeholder="starts with" className={inputCls} maxLength={6} />
        <div className="flex flex-col gap-1 col-span-2 sm:col-span-1">
          <label className="text-xs text-slate-500 font-mono">Min score: {minScore}</label>
          <input type="range" min={0} max={100} value={minScore} onChange={(e) => setMinScore(+e.target.value)} className="accent-violet-500" />
        </div>
        <button onClick={run} disabled={loading}
          className="col-span-2 sm:col-span-1 px-4 py-2 rounded-xl bg-gradient-to-r from-[#7C5CFF] to-[#22D3EE] text-white text-sm font-semibold hover:opacity-90 disabled:opacity-50 transition-opacity">
          {loading ? "Searching…" : <span className="flex items-center justify-center gap-1.5"><Search size={13} /> Search</span>}
        </button>
      </div>

      <GatedPanel feature="search" access={access} gateError={gateError}>
        {results.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
            {results.map((r) => (
              <button key={r.name} onClick={() => setActiveResult(r)}
                className="group p-3 rounded-xl border border-white/8 bg-white/3 hover:border-white/20 hover:bg-white/6 hover:scale-[1.02] transition-all text-left">
                <div className="hacd-name text-sm mb-1 text-white">{r.name}</div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono" style={{ color: TIER_COLOR[r.tier] }}>{r.score}</span>
                  <TierBadge tier={r.tier} label={TIER_LABEL[r.tier]?.slice(0, 4)} />
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-slate-500 gap-2">
            <Search size={24} className="opacity-30" />
            <p className="text-sm">Run a search to discover premium names</p>
          </div>
        )}
      </GatedPanel>

      <AnimatePresence>
        {activeResult && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <AnalyzeResult result={activeResult} onClose={() => setActiveResult(null)} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function LeaderboardPanel({ access }: { access: AccessResult | null }) {
  const [data, setData] = useState<NameAnalysis[]>([]);
  const [loading, setLoading] = useState(false);
  const [gateError, setGateError] = useState<GateError | null>(null);
  const [loaded, setLoaded] = useState(false);

  const load = useCallback(async () => {
    if (loaded) return;
    setLoading(true);
    try {
      const res = await getLeaderboard(25, access?.address ?? "");
      setData(res.results);
      setLoaded(true);
      setGateError(null);
    } catch (e: any) {
      if (e.status === 402) setGateError(e.detail);
      else toast.error("Leaderboard failed");
    } finally { setLoading(false); }
  }, [access, loaded]);

  useEffect(() => { load(); }, [load]);

  const medals: Record<number, string> = { 0: "🥇", 1: "🥈", 2: "🥉" };

  return (
    <GatedPanel feature="leaderboard" access={access} gateError={gateError}>
      {loading ? (
        <div className="space-y-2 animate-pulse">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-10 rounded-xl bg-white/4" />
          ))}
        </div>
      ) : data.length > 0 ? (
        <div className="rounded-xl border border-white/8 overflow-hidden">
          <div className="grid grid-cols-[2rem_1fr_5rem_3rem] gap-3 px-4 py-2 text-xs font-mono text-slate-500 border-b border-white/8">
            <span>#</span><span>Name</span><span>Tags</span><span className="text-right">Score</span>
          </div>
          {data.map((r, i) => (
            <motion.div key={r.name} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.03 }}
              className="grid grid-cols-[2rem_1fr_5rem_3rem] gap-3 px-4 py-2.5 border-b border-white/5 hover:bg-white/3 transition-colors items-center"
              style={i < 3 ? { borderLeft: `2px solid ${TIER_COLOR[r.tier]}` } : {}}>
              <span className="text-xs text-slate-500">{medals[i] ?? i + 1}</span>
              <span className="hacd-name text-sm text-white">{r.name}</span>
              <div className="flex gap-1 flex-wrap">
                {r.tags.slice(0, 1).map((t) => <TagBadge key={t} tag={t} />)}
              </div>
              <span className="text-right font-mono text-sm font-semibold" style={{ color: TIER_COLOR[r.tier] }}>{r.score}</span>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-12 text-slate-500 gap-2">
          <Trophy size={24} className="opacity-30" />
          <p className="text-sm">Leaderboard loading…</p>
        </div>
      )}
    </GatedPanel>
  );
}

const SCORING_DIMS = [
  { label: "Dictionary word", pts: 45, desc: "Real English word in the HACD alphabet — only 1,219 qualify." },
  { label: "Palindrome", pts: 22, desc: "Reads the same forwards and backwards." },
  { label: "Repetition pattern", pts: 30, desc: "Solid (6×), heavy repeat (5+2, 4+2), triple, or mirror-half." },
  { label: "Letter rarity", pts: 18, desc: "Names built from uncommon letters score higher." },
  { label: "Structure", pts: 14, desc: "Low distinct-letter count and mirror-half bonuses." },
];

export default function App() {
  const [tab, setTab] = useState<"analyze" | "search" | "leaderboard" | "about">("analyze");
  const [result, setResult] = useState<NameAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [meta, setMeta] = useState<MetaResponse | null>(null);
  const [access, setAccess] = useState<AccessResult | null>(null);
  const [showConnect, setShowConnect] = useState(false);

  useEffect(() => { getMeta().then(setMeta); }, []);

  const analyze = async (name: string) => {
    setLoading(true);
    setResult(null);
    try {
      const data = await analyzeName(name);
      setResult(data);
      if (tab !== "analyze") setTab("analyze");
    } finally { setLoading(false); }
  };

  const tabs = [
    { id: "analyze", label: "Analyze", icon: <Zap size={13} /> },
    { id: "search", label: "Search", icon: <Search size={13} /> },
    { id: "leaderboard", label: "Leaderboard", icon: <Trophy size={13} /> },
    { id: "about", label: "About", icon: <Info size={13} /> },
  ] as const;

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="sticky top-0 z-40 border-b border-white/8 bg-black/40 backdrop-blur-xl">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between gap-4">
          <button onClick={() => setTab("analyze")} className="font-mono font-bold text-lg gradient-text tracking-widest">
            ZENITH
          </button>
          <div className="hidden sm:flex items-center gap-1">
            {tabs.map((t) => (
              <button key={t.id} onClick={() => setTab(t.id)}
                className={cn(
                  "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors",
                  tab === t.id ? "bg-white/8 text-white" : "text-slate-400 hover:text-white hover:bg-white/4"
                )}>
                {t.icon} {t.label}
              </button>
            ))}
          </div>
          <button onClick={() => setShowConnect(true)}
            className={cn(
              "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-mono border transition-all",
              access
                ? "border-violet-500/40 text-violet-300 bg-violet-500/10"
                : "border-white/10 text-slate-400 hover:border-white/20 hover:text-white"
            )}>
            {access ? (
              <><span className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
              {access.tier.toUpperCase()} · {access.zen_balance.toLocaleString()} ZEN</>
            ) : "Connect address"}
          </button>
        </div>
        <div className="sm:hidden flex border-t border-white/5 max-w-5xl mx-auto">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={cn(
                "flex-1 flex items-center justify-center gap-1 py-2.5 text-xs font-medium transition-colors",
                tab === t.id ? "text-white border-b border-violet-500" : "text-slate-500"
              )}>
              {t.icon} {t.label}
            </button>
          ))}
        </div>
      </nav>

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8">
        <AnimatePresence mode="wait">
          {tab === "analyze" && (
            <motion.div key="analyze" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-10">
              <div className="text-center space-y-4 pt-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 text-xs font-mono text-slate-400 bg-white/3 mb-2">
                  <Gem size={10} className="text-violet-400" /> HACD Naming Layer · Incubator Cohort 2
                </div>
                <h1 className="text-3xl sm:text-5xl font-bold gradient-text font-mono tracking-tight leading-tight">
                  ZENITH
                </h1>
                <p className="text-lg sm:text-xl text-slate-300 max-w-lg mx-auto leading-relaxed">
                  Every HACD is a word.<br />
                  <span className="text-white font-medium">ZENITH tells you which words are worth owning.</span>
                </p>
                <p className="text-sm text-slate-500 max-w-sm mx-auto">
                  Score any 6-letter HACD name across 5 dimensions. Discover the 1,219 that are real words — and the handful that are legendary.
                </p>
              </div>

              <NameInput onAnalyze={analyze} loading={loading} />
              <StatTicker meta={meta} />

              <AnimatePresence>
                {result && (
                  <motion.div key={result.name} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                    <AnalyzeResult result={result} onClose={() => setResult(null)} />
                  </motion.div>
                )}
              </AnimatePresence>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
                {[
                  { name: "ZENITH", label: "Dictionary word · score 51" },
                  { name: "AAAAAA", label: "Solid · palindrome · score 72" },
                  { name: "MINIMI", label: "Palindrome · rare letters · try it" },
                ].map(({ name, label }) => (
                  <button key={name} onClick={() => analyze(name)}
                    className="group p-4 rounded-xl border border-white/8 bg-white/3 hover:border-violet-500/30 hover:bg-violet-500/5 transition-all text-left">
                    <div className="hacd-name text-lg text-white mb-1">{name}</div>
                    <div className="text-xs text-slate-500 group-hover:text-slate-400 transition-colors flex items-center gap-1">
                      {label} <ChevronRight size={10} />
                    </div>
                  </button>
                ))}
              </div>
            </motion.div>
          )}

          {tab === "search" && (
            <motion.div key="search" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-white mb-1">Search premium names</h2>
                <p className="text-sm text-slate-400">Filter the 1,219+ premium HACD names by pattern, prefix, or minimum score.</p>
              </div>
              <SearchPanel access={access} />
            </motion.div>
          )}

          {tab === "leaderboard" && (
            <motion.div key="leaderboard" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-white mb-1">Name leaderboard</h2>
                <p className="text-sm text-slate-400">The highest-scoring HACD names in the entire 16,777,216-name space.</p>
              </div>
              <LeaderboardPanel access={access} />
            </motion.div>
          )}

          {tab === "about" && (
            <motion.div key="about" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-8 max-w-2xl">
              <div>
                <h2 className="text-xl font-semibold text-white mb-2">How the namescore works</h2>
                <p className="text-sm text-slate-400 mb-6">Five independent dimensions, scored 0–100 total. Purely linguistic and structural — not a market price.</p>
                <div className="space-y-3">
                  {SCORING_DIMS.map(({ label, pts, desc }) => (
                    <div key={label} className="flex gap-4 p-4 rounded-xl border border-white/8 bg-white/3">
                      <span className="font-mono font-bold text-violet-400 text-sm w-8 shrink-0 mt-0.5">{pts}</span>
                      <div>
                        <div className="text-sm font-medium text-white mb-0.5">{label}</div>
                        <div className="text-xs text-slate-400">{desc}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-4 rounded-xl border border-cyan-500/20 bg-cyan-500/5">
                <p className="text-sm font-medium text-cyan-300 mb-1">ZENITH vs Carat Protocol</p>
                <p className="text-xs text-slate-400">
                  Carat scores what a HACD is worth on the market. ZENITH scores what it says.
                  The two are complementary — different layers of the same namespace.
                </p>
              </div>

              <div className="space-y-3">
                <p className="text-xs font-mono text-slate-500 uppercase tracking-wider">ZEN tokenomics</p>
                <div className="rounded-xl border border-white/8 overflow-hidden">
                  {[
                    ["Total supply", "16,777,216 ZEN", "= 16^6 = total HACD namespace"],
                    ["HACD lots", "256", "= 16^2"],
                    ["ZEN per lot", "65,536", "= 16^4"],
                    ["Stack cost", "50 HAC / HACD", "paid by participant"],
                    ["Reserved", "32 lots · 12.5%", "ecosystem + engine costs"],
                    ["Public", "224 lots · 87.5%", "open participation"],
                  ].map(([k, v, note]) => (
                    <div key={k} className="grid grid-cols-[8rem_8rem_1fr] gap-3 px-4 py-2.5 border-b border-white/5 text-sm">
                      <span className="text-slate-400">{k}</span>
                      <span className="font-mono text-white">{v}</span>
                      <span className="text-slate-500 text-xs">{note}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-4 rounded-xl border border-white/8 bg-white/3 text-xs text-slate-500 leading-relaxed">
                ZEN is a utility Stack Asset, not an investment product. The namescore is a linguistic opinion, not a financial valuation. No price, liquidity, listing, or return is guaranteed. Built for HACD Labs Incubator Cohort 2.
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer className="border-t border-white/8 mt-12">
        <div className="max-w-5xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="font-mono font-bold gradient-text tracking-widest text-sm">ZENITH</span>
          <div className="flex items-center gap-5 text-xs text-slate-500">
            {[
              { label: "Launchpad", href: "https://hacd.it/launchpad" },
              { label: "Explorer", href: "https://explorer.hacash.org" },
              { label: "HACD Labs", href: "https://hacd.it" },
              { label: "X", href: "https://x.com/ZenithHACD" },
            ].map(({ label, href }) => (
              <a key={label} href={href} target="_blank" rel="noopener noreferrer"
                className="hover:text-white transition-colors flex items-center gap-0.5">
                {label} <ExternalLink size={9} />
              </a>
            ))}
          </div>
          <p className="text-xs text-slate-600">Not financial advice</p>
        </div>
      </footer>

      {showConnect && <ConnectModal onConnect={(a) => { setAccess(a); setShowConnect(false); }} onClose={() => setShowConnect(false)} />}
    </div>
  );
}
