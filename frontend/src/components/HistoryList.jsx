import { WordCard } from "./WordCard";

export function HistoryList({ history, onRepeatSlow }) {
  if (history.length === 0) {
    return null;
  }

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">History</h2>
        <p className="text-sm text-slate-400">Disponible offline si el audio ya fue descargado.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {history.map((item) => (
          <WordCard key={`history-${item.word}-${item.audio_filename ?? item.error}`} item={item} onRepeatSlow={onRepeatSlow} />
        ))}
      </div>
    </section>
  );
}
