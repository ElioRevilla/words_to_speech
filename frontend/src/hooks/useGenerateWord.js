import { useState } from "react";

import { generateWordsRequest } from "../services/api";

async function warmAudioCache(items) {
  const validItems = items.filter((item) => item.audio_url);
  await Promise.all(
    validItems.map(async (item) => {
      try {
        await fetch(item.audio_url, { cache: "force-cache" });
      } catch {
        return null;
      }
      return null;
    })
  );
}

export function useGenerateWord({ onPersist }) {
  const [state, setState] = useState("idle");
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);

  const run = async (words, slow = false) => {
    setState("loading");
    setError(null);

    try {
      const responseItems = await generateWordsRequest(words, slow);
      setItems(responseItems);
      setState("success");
      await warmAudioCache(responseItems);
      onPersist(responseItems);
    } catch (requestError) {
      setState("error");
      setError(requestError.message || "Request failed");
    }
  };

  return {
    state,
    items,
    error,
    generateWords: (words) => run(words, false),
    repeatSlowly: (word) => run([word], true)
  };
}
