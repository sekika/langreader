# Usage Guide

## CLI Usage

```bash
langreader -i INPUT.md -o OUTPUT.html --src SRC --tgt TGT --provider PROVIDER --model MODEL [options]
```

### Required Arguments

- `-i, --input`: Input Markdown file path.
- `-o, --output`: Output HTML file path.
- `--provider`: Provider name configured in `multiai` (e.g., `openai`, `anthropic`).
- `--model`: Model name (e.g., `gpt-4o`, `claude-3-5-sonnet`).

### Optional Arguments

- `--src` (default: `fr`): Source language code (e.g., `fr`, `de`, `ja`).
- `--tgt` (default: `en`): Target language code for translation.
- `-v, --verbose`: Verbosity level (`0`=silent, `1`=headings, `2`=preview, `3`=full).
- `--continue`: Resume generation from the existing output file if the process was interrupted (e.g., by API rate limits). The tool saves progress incrementally; this option allows you to restart where it left off without re-translating the beginning of the file.
- `--js-url`: URL for the external JavaScript file.
    - Default: [https://cdn.jsdelivr.net/gh/sekika/langreader@main/js/langreader.js](https://cdn.jsdelivr.net/gh/sekika/langreader@main/js/langreader.js)
- `--css-url`: URL for the external CSS file.
    - Default: [https://cdn.jsdelivr.net/gh/sekika/langreader@main/css/langreader.css](https://cdn.jsdelivr.net/gh/sekika/langreader@main/css/langreader.css)


## YAML Frontmatter Support

You can add metadata at the top of your Markdown file using YAML syntax. This is useful for adding descriptions, attribution, or license information.

```markdown
---
description: French reading practice. Based on the article [Alsace](https://fr.wikipedia.org/wiki/Alsace) (as of 2025-12-16). Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
---
# Alsace

L’ Alsace est une région historique...
```

The `description` field supports Markdown links (`[text](url)`), which will be rendered as HTML links in the generated reader's header.

## Helper Script: wiki_to_md.py

We provide a helper script, `wiki_to_md.py`, to download Wikipedia articles and format them for `langreader`. It automatically adds the necessary YAML frontmatter, including the license and last updated date.

See the [Tutorial](tutorial.md) for details.
