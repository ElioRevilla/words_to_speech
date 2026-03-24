export async function downloadAudioFile(audioUrl, preferredFilename, fallbackFilename = "audio.mp3") {
  const response = await fetch(audioUrl);
  if (!response.ok) {
    throw new Error("Download failed");
  }

  const blob = await response.blob();
  const objectUrl = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = preferredFilename || fallbackFilename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(objectUrl);
}
