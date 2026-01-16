# langreader

Generate language-learning HTML readers from Markdown using an LLM.

**langreader** is a CLI tool that converts Markdown texts into interactive HTML readers. It uses Large Language Models (LLMs) via [multiai](https://sekika.github.io/multiai/) to split paragraphs into natural sentences and provide sentence-level translations.

## 👀 Demo

Before reading further, check out what this tool generates:

👉 **[Live Demo: French Reader (Alsace)](https://sekika.github.io/langreader/examples/alsace.html)**

## Movie

<iframe width="560" height="315" src="https://www.youtube.com/embed/IFxaOei3A_E?si=dZYHPAszlbejN-LL" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- Movies in [日本語](https://www.youtube.com/watch?v=aZnBuUSo68E) / [Français](https://www.youtube.com/watch?v=AUacF2CqzFo)
- Movie created with [slidemovie](https://sekika.github.io/slidemovie/)

## Features

- 🤖 **AI-Powered Translation**: Automatically splits paragraphs into natural sentences and translates them line-by-line.
- 🔊 **Text-to-Speech**: Built-in audio buttons for every source sentence (uses browser Web Speech API).
- ⏯️ **Resumable Generation**: Hit an API rate limit? Use `--continue` to resume generation exactly where it stopped.
- 📝 **Markdown Support**: Preserves headings, code blocks, and basic formatting.
- 🌍 **Wikipedia Helper**: Includes a script to easily fetch and format Wikipedia articles for learning.

## Installation

```bash
pip install md-llm-lang-reader
```

## Prerequisite: multiai configuration

This tool uses **multiai** internally to access LLM providers (OpenAI, Anthropic, Google, etc.).
Before using `langreader`, you must configure **multiai**.

Details on supported providers and configuration can be found here:
[https://sekika.github.io/multiai/](https://sekika.github.io/multiai/)

## Quick Start

1.  **Prepare a Markdown file (`input.md`)**:
    ```markdown
    # Bonjour

    Ceci est un exemple de phrase.
    ```

2.  **Run the command**:
    ```bash
    langreader -i input.md -o output.html --src fr --tgt en --provider openai --model gpt-5-nano
    ```

3.  **Open `output.html`** in your browser.

## Documentation Navigation

- [**Usage Guide**](usage.md): Detailed CLI options, YAML metadata, and styling.
- [**Tutorial**](tutorial.md): A step-by-step example creating a French reader from Wikipedia ("Alsace").
- [**TTS Setup**](tts.md): How to configure voices on Windows, macOS, iOS, and Android.
