import { useState } from "react";

import { downloadAudioFile } from "../services/audioDownload";
import { AudioPlayer } from "./AudioPlayer";

export function CombinedAudioCard({ audio, loading, error }) {
  const [downloading, setDownloading] = useState(false);

  if (!audio && !loading && !error) {
    return null;
  }

  const handleDownload = async () => {
    if (!audio?.audio_url || downloading) {
      return;
    }

    try {
      setDownloading(true);
      await downloadAudioFile(audio.audio_url, audio.audio_filename, "history-mix.mp3");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <section className="space-y-4 rounded-[2rem] border border-white/10 bg-white/5 p-5 backdrop-blur">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-2">
          <p className="text-sm uppercase tracking-[0.35em] text-signal">Long audio</p>
          <h2 className="text-2xl font-semibold">Study mix</h2>
          <p className="text-sm text-slate-300">
            {audio ? `Une ${audio.item_count} audios del historial en una sola pista.` : "Creando el audio combinado del historial..."}
          </p>
        </div>
        {audio ? <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-200">{audio.item_count} items</span> : null}
      </div>

      {loading ? <div className="h-24 animate-pulse rounded-2xl bg-white/5" /> : null}
      {error ? <p className="rounded-2xl bg-rose-950/40 p-4 text-sm text-rose-100">{error}</p> : null}
      {audio ? (
        <div className="space-y-4">
          <AudioPlayer src={audio.audio_url} />
          <button
            type="button"
            onClick={handleDownload}
            disabled={downloading}
            className="rounded-full border border-white/15 px-4 py-2 text-sm text-slate-100 transition hover:bg-white hover:text-slate-950 disabled:cursor-wait disabled:opacity-60"
          >
            {downloading ? "Downloading..." : "Download long audio"}
          </button>
        </div>
      ) : null}
    </section>
  );
}
