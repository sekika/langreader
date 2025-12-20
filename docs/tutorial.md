# Tutorial

This tutorial demonstrates how to create a French reading practice file based on the Wikipedia article for **Alsace**.

## Step 1: Get the Helper Script

Download the `wiki_to_md.py` script. This script fetches Wikipedia content, removes clutter (citations, tables), and formats it for the reader.

- [**Download wiki_to_md.py**](scripts/wiki_to_md.py)

## Step 2: Fetch Content

Run the script to download the French Wikipedia page for "Alsace".

```bash
python wiki_to_md.py Alsace -o alsace.md --lang fr
```

This generates a file named `alsace.md`.
You can view the generated Markdown file here:
[**View alsace.md**](https://github.com/sekika/langreader/blob/main/docs/examples/alsace.md)

Notice that it includes a **YAML description** with the date and license:

```markdown
---
description: French reading practice. Based on the French Wikipedia article [Alsace](https://fr.wikipedia.org/wiki/Alsace) (as of 2025-12-16). Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
---
# Alsace
...
```

## Step 3: Generate the Reader

Now, use `langreader` to translate the content and generate the HTML.

```bash
langreader \
  -i alsace.md \
  -o alsace.html \
  --src fr \
  --tgt en \
  --provider openai \
  --model gpt-4o-mini
```

*(Note: Replace provider/model with your actual configuration)*

## Step 4: Result

Open the resulting HTML file in your browser. You will see the original text with audio buttons and the English translation below each sentence.

[**View Final Result (alsace.html)**](examples/alsace.html)
*(Click this link to see the live HTML example)*
