const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function generateWordsRequest(words, slow = false) {
  const response = await fetch(`${API_BASE_URL}/api/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ words, slow })
  });

  if (!response.ok) {
    throw new Error(`Backend request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data.items || [];
}

export async function combineHistoryAudioRequest(filenames) {
  const response = await fetch(`${API_BASE_URL}/api/audio/combine`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ filenames })
  });

  if (!response.ok) {
    throw new Error(`Combined audio request failed with status ${response.status}`);
  }

  return response.json();
}
