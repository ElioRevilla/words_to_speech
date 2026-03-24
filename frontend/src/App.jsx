import { useEffect, useState } from "react";

import { CombinedAudioCard } from "./components/CombinedAudioCard";
import { HistoryList } from "./components/HistoryList";
import { WordCard } from "./components/WordCard";
import { WordInput } from "./components/WordInput";
import { useGenerateWord } from "./hooks/useGenerateWord";
import { combineHistoryAudioRequest } from "./services/api";

const HISTORY_KEY = "wordsound-history";
const COMBINED_AUDIO_KEY = "wordsound-combined-audio";

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function loadCombinedAudio() {
  try {
    const raw = localStorage.getItem(COMBINED_AUDIO_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export default function App() {
  const [history, setHistory] = useState(loadHistory);
  const [combinedAudio, setCombinedAudio] = useState(loadCombinedAudio);
  const [combinedState, setCombinedState] = useState("idle");
  const [combinedError, setCombinedError] = useState(null);
  const { state, items, error, generateWords, repeatSlowly } = useGenerateWord({
    onPersist: (newItems) => {
      setHistory((previousHistory) => {
        const nextHistory = [...newItems, ...previousHistory].slice(0, 20);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(nextHistory));
        return nextHistory;
      });
    }
  });

  useEffect(() => {
    const filenames = history.map((item) => item.audio_filename).filter(Boolean);

    if (filenames.length === 0) {
      setCombinedAudio(null);
      setCombinedState("idle");
      setCombinedError(null);
      localStorage.removeItem(COMBINED_AUDIO_KEY);
      return undefined;
    }

    let active = true;

    const syncCombinedAudio = async () => {
      setCombinedState("loading");
      setCombinedError(null);

      try {
        const nextCombinedAudio = await combineHistoryAudioRequest(filenames);
        if (!active) {
          return;
        }

        setCombinedAudio(nextCombinedAudio);
        setCombinedState("success");
        localStorage.setItem(COMBINED_AUDIO_KEY, JSON.stringify(nextCombinedAudio));
      } catch (requestError) {
        if (!active) {
          return;
        }

        setCombinedState("error");
        setCombinedError(requestError.message || "Combined audio request failed");
      }
    };

    syncCombinedAudio();

    return () => {
      active = false;
    };
  }, [history]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,#103a53_0%,#041b2d_60%)] text-slate-50">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-10 px-4 py-8 md:px-8">
        <header className="space-y-4">
          <p className="text-sm uppercase tracking-[0.35em] text-signal">PWA English practice</p>
          <div className="max-w-3xl space-y-3">
            <h1 className="text-4xl font-semibold tracking-tight md:text-6xl">WordSound</h1>
            <p className="text-base text-slate-300 md:text-lg">
              Genera pronunciacion, spelling, definicion y ejemplo bilingue con audio listo para repetir.
            </p>
          </div>
        </header>

        <WordInput onSubmit={generateWords} loading={state === "loading"} />

        {state === "error" ? (
          <section className="rounded-3xl border border-rose-400/30 bg-rose-950/30 p-5 text-rose-100">
            {error}
          </section>
        ) : null}

        {state === "loading" ? (
          <section className="grid gap-4 md:grid-cols-2">
            {Array.from({ length: 2 }).map((_, index) => (
              <div key={index} className="h-72 animate-pulse rounded-3xl bg-white/5" />
            ))}
          </section>
        ) : null}

        {items.length > 0 ? (
          <section className="grid gap-4 md:grid-cols-2">
            {items.map((item) => (
              <WordCard key={`${item.word}-${item.audio_filename ?? item.error}`} item={item} onRepeatSlow={repeatSlowly} />
            ))}
          </section>
        ) : null}

        <CombinedAudioCard
          audio={combinedAudio}
          loading={combinedState === "loading"}
          error={combinedState === "error" ? combinedError : null}
        />

        <HistoryList history={history} onRepeatSlow={repeatSlowly} />
      </div>
    </main>
  );
}
