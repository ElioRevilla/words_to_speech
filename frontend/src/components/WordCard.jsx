import { useState } from "react";

import { downloadAudioFile } from "../services/audioDownload";
import { AudioPlayer } from "./AudioPlayer";

export function WordCard({ item, onRepeatSlow }) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    if (!item.audio_url || downloading) {
      return;
    }

    const fallbackName = `${item.word}${item.slow ? "-slow" : ""}.mp3`;

    try {
      setDownloading(true);
      await downloadAudioFile(item.audio_url, item.audio_filename, fallbackName);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <article className="rounded-[2rem] border border-white/10 bg-white/5 p-5 backdrop-blur">
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-2xl font-semibold capitalize">{item.word}</h2>
          <p className="text-sm text-signal">{item.phonetic ?? "No phonetic available"}</p>
        </div>
        {item.slow ? <span className="rounded-full bg-signal px-3 py-1 text-xs font-medium text-slate-950">Slow</span> : null}
      </div>

      {item.error ? (
        <p className="rounded-2xl bg-rose-950/40 p-4 text-sm text-rose-100">{item.error}</p>
      ) : (
        <div className="space-y-4">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Spelling</p>
            <p className="mt-1 text-base text-slate-100">{item.spelling}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Meaning</p>
            <p className="mt-1 text-base text-slate-100">{item.meaning}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Example</p>
            <p className="mt-1 text-base text-slate-100">{item.example_en}</p>
            <p className="mt-1 text-sm text-slate-300">{item.example_es}</p>
          </div>
          {item.audio_url ? <AudioPlayer src={item.audio_url} /> : null}
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => onRepeatSlow(item.word)}
              className="rounded-full border border-accent/40 px-4 py-2 text-sm text-accent transition hover:bg-accent hover:text-slate-950"
            >
              Repeat slowly
            </button>
            {item.audio_url ? (
              <button
                type="button"
                onClick={handleDownload}
                disabled={downloading}
                className="rounded-full border border-white/15 px-4 py-2 text-sm text-slate-100 transition hover:bg-white hover:text-slate-950 disabled:cursor-wait disabled:opacity-60"
              >
                {downloading ? "Downloading..." : "Download audio"}
              </button>
            ) : null}
          </div>
        </div>
      )}
    </article>
  );
}
