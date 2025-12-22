(function() {
  let cachedVoices = [];
  let activeUtterance = null; // Prevents garbage collection during playback

  function loadVoices() {
    const voices = speechSynthesis.getVoices();
    if (voices.length > 0) cachedVoices = voices;
  }

  // Ensure voices are loaded asynchronously
  speechSynthesis.onvoiceschanged = loadVoices;
  loadVoices();

  function getBestVoice(lang) {
    if (!cachedVoices.length) loadVoices();
    const voices = cachedVoices;
    
    // 1. Exact match, 2. Starts with (e.g., 'fr-FR' for 'fr'), 3. Prefix match
    let v = voices.find(v => v.lang === lang);
    if (!v) v = voices.find(v => v.lang && v.lang.startsWith(lang));
    if (!v) {
      const prefix = (lang || "").split("-")[0];
      v = voices.find(v => v.lang && v.lang.startsWith(prefix));
    }
    return v;
  }

  function speakText(text, lang) {
    if (!text) return;
    speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    u.lang = lang;
    
    const voice = getBestVoice(lang);
    if (voice) u.voice = voice;

    // Keep reference to prevent GC pausing playback
    activeUtterance = u;
    u.onend = () => { activeUtterance = null; };

    speechSynthesis.speak(u);
  }

  function wireButtons() {
    document.querySelectorAll("button.speak-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        speakText(btn.dataset.speak || "", btn.dataset.lang || "");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireButtons);
  } else {
    wireButtons();
  }
})();
