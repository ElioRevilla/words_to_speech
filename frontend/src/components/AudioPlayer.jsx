import { useEffect, useRef, useState } from "react";

const SPEEDS = [0.75, 1, 1.25];

export function AudioPlayer({ src }) {
  const audioRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [speed, setSpeed] = useState(1);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) {
      return undefined;
    }

    const syncTime = () => {
      if (!audio.duration) {
        setProgress(0);
        return;
      }
      setProgress((audio.currentTime / audio.duration) * 100);
    };

    const onEnded = () => {
      setPlaying(false);
      setProgress(0);
    };

    audio.addEventListener("timeupdate", syncTime);
    audio.addEventListener("ended", onEnded);
    return () => {
      audio.removeEventListener("timeupdate", syncTime);
      audio.removeEventListener("ended", onEnded);
    };
  }, []);

  const toggle = async () => {
    const audio = audioRef.current;
    if (!audio) {
      return;
    }
    if (playing) {
      audio.pause();
      setPlaying(false);
      return;
    }
    audio.playbackRate = speed;
    await audio.play();
    setPlaying(true);
  };

  const updateSpeed = (value) => {
    setSpeed(value);
    if (audioRef.current) {
      audioRef.current.playbackRate = value;
    }
  };

  return (
    <div className="space-y-3 rounded-2xl border border-white/10 bg-slate-950/50 p-4">
      <audio ref={audioRef} src={src} preload="auto" />
      <div className="flex items-center gap-3">
        <button onClick={toggle} type="button" className="rounded-full bg-signal px-4 py-2 text-sm font-medium text-slate-950">
          {playing ? "Pause" : "Play"}
        </button>
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/10">
          <div className="h-full bg-accent transition-all" style={{ width: `${progress}%` }} />
        </div>
      </div>
      <div className="flex gap-2">
        {SPEEDS.map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => updateSpeed(option)}
            className={`rounded-full px-3 py-1 text-xs ${speed === option ? "bg-accent text-slate-950" : "bg-white/10 text-slate-200"}`}
          >
            {option}x
          </button>
        ))}
      </div>
    </div>
  );
}
