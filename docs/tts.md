# Text-to-Speech (TTS) Setup Guide

`langreader` uses your browser's built-in **Web Speech API**. The quality and availability of voices depend entirely on your operating system and browser settings.

If the audio does not play or sounds robotic, you may need to install "Enhanced" or "Natural" voices for the target language (e.g., French).

## 🍎 macOS (Mac)

1. Open **System Settings** > **Accessibility**.
2. Click on **Spoken Content**.
3. Look for **System Voice** or click the **"i"** (info) icon next to it.
4. Go to **Manage Voices...**.
5. Search for the language (e.g., French).
6. Download **Premium** or **Siri** voices (e.g., "Thomas (Premium)" or "Siri Voice 1") for better quality.
7. Restart your browser.

## 🪟 Windows

1. Open **Settings** > **Time & language** > **Speech**.
2. Under **Manage voices**, click **Add voices**.
3. Search for the language pack (e.g., French) and install it.
4. **Important**: Using **Microsoft Edge** often provides better, natural online voices (Azure Neural voices) compared to other browsers on Windows.

## 📱 iOS / iPadOS (iPhone, iPad)

1. Open **Settings** > **Accessibility**.
2. Tap **Spoken Content** > **Voices**.
3. Select the language (e.g., French).
4. Download **Enhanced** or **Premium** versions of the voices (tap the cloud icon).
5. Ensure your device is not in Silent mode if audio doesn't play.

## 🤖 Android

1. Open **Settings** > **Accessibility**.
2. Tap **Text-to-speech output**.
3. Tap the gear icon next to **Preferred engine** (usually Speech Services by Google).
4. Tap **Install voice data**.
5. Find the language and download it.

## Troubleshooting

- **No Sound?** Check if `data-lang` is set correctly in the HTML (e.g., `fr`). Some browsers require a user interaction (click) before allowing speech, which the buttons handle.
- **Wrong Language/Accent?** 
  - If the voice sounds like it is reading with an English accent (e.g., system default) instead of the target language, ensure you have **installed the language pack** as described above.
  - **Restart your browser completely** after installing new voices. The script loads voices immediately upon opening the page, so it needs the browser to recognize the new system voices first.
