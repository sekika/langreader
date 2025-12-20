(function() {
  function chooseVoice(u) {
    const voices = speechSynthesis.getVoices ? speechSynthesis.getVoices() : [];
    if (!voices || !voices.length) return;

    let v = voices.find(v => v.lang === u.lang);
    if (!v) {
      v = voices.find(v => v.lang && v.lang.startsWith(u.lang));
    }
    if (!v) {
      const prefix = (u.lang || "").split("-")[0];
      v = voices.find(v => v.lang && v.lang.startsWith(prefix));
    }
    if (v) u.voice = v;
  }

  function speakText(text, lang) {
    if (!text) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = lang;
    chooseVoice(u);
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
