# md-llm-lang-reader

Markdown から「学習用のHTMLリーダー教材」を生成するツールです（LLMで文分割＋翻訳、TTSボタン付き）。

- 段落を **文ごとに分割**して自然な単位で表示
- 各文に **訳（ターゲット言語）**を付与
- 原文（src）には **ワンクリックで読み上げ（TTS）**ボタン
- ``` や ~~~ の **fenced code block は翻訳せず**、コードとしてそのままHTMLに出力

PyPIのパッケージ名は **`md-llm-lang-reader`**、インストールされるコマンドは **`langreader`** です。

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sekika/langreader/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/sekika/langreader/blob/main/README-ja.md)
[![fr](https://img.shields.io/badge/lang-fr-green.svg)](https://github.com/sekika/langreader/blob/main/README-fr.md)

## 特長

- **Markdown → HTML**（見出し＋段落のシンプル変換）
- **LLMによる文分割**（自然な文境界）
- **文単位の翻訳**（原文と訳をペア表示）
- **各文にTTSボタン**
- **コードブロックは保持**（LLMに渡さない）
- **箇条書きも翻訳**（特別扱いせずテキストとしてLLMに渡します）

## インストール

```bash
pip install md-llm-lang-reader
```

## APIキーの設定（multiai）

このツールは内部で **multiai** を利用して LLM にアクセスします。
そのため、使用するプロバイダ（OpenAI / Anthropic / Google など）に応じた **APIキーの設定が事前に必要**です。

APIキーの設定方法や対応プロバイダの詳細については、以下のドキュメントを参照してください。

https://sekika.github.io/multiai/index-ja.html

## クイックスタート

`input.md` を作成します:

```md
# Example

Bonjour ! Ceci est un court paragraphe.

```python
# コードブロックは翻訳されません
print("Hello")
```

- Premier point
- Deuxième point
```

HTMLを生成します:

```bash
langreader \
  -i input.md \
  -o output.html \
  --src fr \
  --tgt en \
  --provider YOUR_PROVIDER \
  --model YOUR_MODEL
```

生成された `output.html` をブラウザで開き、スピーカーボタンを押すと原文が読み上げられます。

## 使い方（CLI）

```bash
langreader -i INPUT.md -o OUTPUT.html --src SRC --tgt TGT --provider PROVIDER --model MODEL [-v 0|1|2|3]
```

### オプション

- `-i, --input`（必須）  
  入力Markdownファイルのパス

- `-o, --output`（必須）  
  出力HTMLファイルのパス

- `--src`（デフォルト: `fr`）  
  原文の言語コード（例: `fr`, `de`, `es`, `ja`）

- `--tgt`（デフォルト: `en`）  
  翻訳先の言語コード

- `--provider`（必須）  
  `multiai` に渡す provider 名（あなたの `multiai` 設定に依存します）

- `--model`（必須）  
  `multiai` に渡す model 名

- `-v, --verbose`（デフォルト: `1`）  
  端末への出力レベル:
  - `0`: 何も出力しない
  - `1`: 見出しのみ出力
  - `2`: 段落の冒頭（先頭5語程度）のみ出力
  - `3`: 原文段落を全文出力

### 例

フランス語 → 英語:

```bash
langreader -i alsace.md -o alsace.html --src fr --tgt en --provider ... --model ...
```

ドイツ語 → 英語:

```bash
langreader -i berlin.md -o berlin.html --src de --tgt en --provider ... --model ...
```

日本語 → 英語:

```bash
langreader -i news.md -o news.html --src ja --tgt en --provider ... --model ...
```

## 仕組み（概要）

各段落ごとにLLMへ次のタスクを依頼します。

1. 段落を自然な文に分割（略語などで不自然に切らない）
2. 各文をターゲット言語へ直訳気味に翻訳
3. **JSONのみ**で返す（余計な説明やMarkdownは禁止）

期待するJSONスキーマ:

```json
[
  { "src": "…", "tgt": "…" }
]
```

ツール側でJSONを検証・パースし、原文＋訳をHTMLに並べて出力します。

## TTS（読み上げ）について

- ブラウザの **Web Speech API**（`speechSynthesis`）を利用します。
- 利用できる音声（voice）はOS/ブラウザに依存します。
- 発話言語は `--src` を `SpeechSynthesisUtterance.lang` に設定します（例: `fr`）。
  - `fr-FR` のようにロケールまで指定したい場合は、現状は生成HTMLを編集してください（将来的にCLI化可能）。

## Markdownサポート（現状）

対応:
- 見出し: `#`, `##`, `###`, `####`
- 段落: 空行で区切り、連続行はスペース結合
- fenced code block: ``` / ~~~（言語指定などの info string があってもOK）

未対応（特別なレンダリングはしません）:
- 引用、表、画像
- インライン装飾（リンク、強調など）はMarkdownとしてレンダリングされず、プレーンテキストとして扱われます

よりリッチなMarkdown対応が必要なら、Markdownパーサを導入し、原文とHTMLの対応付けを設計するのがおすすめです。

## セキュリティ

- HTML出力時はエスケープを行い、`onclick` に任意テキストを直埋めしない設計にしています。
- TTSボタンは `data-speak="..."` にテキストを保持し、JSのイベントリスナーで読み取ります（引用符問題とXSSリスクの低減）。

ただし、入力Markdownが不特定多数から来る場合は、生成HTMLを「完全に安全」とはみなさず取り扱いに注意してください。

## 開発

開発用インストール:

```bash
pip install -e .
```

テスト:

```bash
pytest
```

ビルド:

```bash
python -m build
```

## ライセンス

MIT
