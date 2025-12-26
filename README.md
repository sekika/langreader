# langreader

Generate interactive language-learning HTML readers from Markdown using LLMs.

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sekika/langreader/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/sekika/langreader/blob/main/README-ja.md)
[![fr](https://img.shields.io/badge/lang-fr-green.svg)](https://github.com/sekika/langreader/blob/main/README-fr.md)

## 👀 Demo

Before reading further, check out what this tool generates:

👉 **[Live Demo: French Reader (Alsace)](https://sekika.github.io/langreader/examples/alsace.html)**

---

`md-llm-lang-reader` (CLI command: `langreader`) converts standard Markdown text into a bilingual HTML reader. It uses Large Language Models (via [multiai](https://sekika.github.io/multiai/)) to intelligently split paragraphs into natural sentences and provide translations, while adding Text-to-Speech (TTS) capabilities to every sentence.

## Features

- 🤖 **AI-Powered Translation**: Automatically splits paragraphs into natural sentences and translates them line-by-line.
- 🔊 **Text-to-Speech**: Built-in audio buttons for every source sentence (uses browser Web Speech API).
- ⏯️ **Resumable Generation**: Hit an API rate limit? Use `--continue` to resume generation exactly where it stopped.
- 📝 **Markdown Support**: Preserves headings, code blocks, and basic formatting.
- 🌍 **Wikipedia Helper**: Includes a script to easily fetch and format Wikipedia articles for learning.

## 📚 Documentation

For detailed installation instructions, CLI options, and tutorials, please visit the official documentation:

👉 **[https://sekika.github.io/langreader/](https://sekika.github.io/langreader/)**

- [**Usage Guide**](https://sekika.github.io/langreader/usage/): Options for styling, resuming, and metadata.
- [**Tutorial**](https://sekika.github.io/langreader/tutorial/): Step-by-step guide to creating a reader from a Wikipedia article.
- [**TTS Setup**](https://sekika.github.io/langreader/tts/): How to configure high-quality voices on your device.

## Installation

```bash
pip install md-llm-lang-reader
```

*Note: This tool requires [multiai](https://sekika.github.io/multiai/) configuration to access LLM providers (OpenAI, Anthropic, etc.).*

## Quick Start

1.  **Create a Markdown file (`input.md`)**:
    ```markdown
    # Bonjour
    Ceci est un exemple de phrase pour l'apprentissage.
    ```

2.  **Run the generator**:
    ```bash
    langreader -i input.md -o output.html --src fr --tgt en --provider openai --model gpt-5-nano
    ```

3.  **Open `output.html`** in your browser to start reading and listening!

## License

MIT

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sekika/langreader)
