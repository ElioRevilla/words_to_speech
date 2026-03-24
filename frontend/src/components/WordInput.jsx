import { useState } from "react";

function parseWords(value) {
  return value
    .split(/[\n,]+/)
    .map((word) => word.trim())
    .filter(Boolean);
}

export function WordInput({ onSubmit, loading }) {
  const [value, setValue] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    const words = parseWords(value);
    if (words.length === 0) {
      return;
    }
    onSubmit(words);
  };

  return (
    <form className="rounded-[2rem] border border-white/10 bg-white/5 p-5 shadow-glow backdrop-blur" onSubmit={handleSubmit}>
      <label className="mb-3 block text-sm text-slate-300" htmlFor="word-input">
        Ingresa una o varias palabras separadas por coma o salto de línea.
      </label>
      <div className="grid gap-4 md:grid-cols-[1fr_auto]">
        <textarea
          id="word-input"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          className="min-h-32 rounded-3xl border border-white/10 bg-slate-950/40 px-4 py-3 text-base text-white outline-none ring-0 placeholder:text-slate-500"
          placeholder={"resilience,\nthroughput,\nstakeholder"}
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-3xl bg-accent px-6 py-4 text-sm font-semibold text-slate-950 transition hover:bg-signal disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Generating..." : "Generate Audio"}
        </button>
      </div>
    </form>
  );
}
