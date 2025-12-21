# langreader

LLMを活用し、Markdownからインタラクティブな語学学習用HTMLリーダーを生成します。

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sekika/langreader/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/sekika/langreader/blob/main/README-ja.md)
[![fr](https://img.shields.io/badge/lang-fr-green.svg)](https://github.com/sekika/langreader/blob/main/README-fr.md)

## 👀 デモ

詳細を読む前に、まずはこのツールがどのようなものを生成するのかをご覧ください。

👉 **[ライブデモ: フランス語リーダー (アルザス)](https://sekika.github.io/langreader/examples/alsace.html)**

---

`md-llm-lang-reader`（CLIコマンド: `langreader`）は、標準的なMarkdownテキストを対訳付きのHTMLリーダーに変換します。[multiai](https://github.com/sekika/multiai)を介して大規模言語モデル（LLM）を使用し、段落を自然な文単位に分割して翻訳を提供すると同時に、すべての文に音声読み上げ（TTS）機能を追加します。

## 特徴

- 🤖 **AI翻訳**: 段落を自動的に自然な文に分割し、行ごとに翻訳します。
- 🔊 **音声読み上げ**: すべての原文に対して音声ボタンを埋め込みます（ブラウザのWeb Speech APIを使用）。
- ⏯️ **生成の再開**: APIレート制限にかかっても大丈夫です。`--continue`を使えば、中断した場所から正確に生成を再開できます。
- 📝 **Markdownサポート**: 見出し、コードブロック、基本的なフォーマットを保持します。
- 🌍 **Wikipediaヘルパー**: 学習用にWikipediaの記事を簡単に取得・整形するスクリプトが付属しています。

## 📚 ドキュメント

詳しいインストール方法、CLIオプション、チュートリアルについては、公式ドキュメントをご覧ください。

👉 **[https://sekika.github.io/langreader/](https://sekika.github.io/langreader/)**

- [**利用ガイド**](https://sekika.github.io/langreader/usage/): スタイル設定、生成の再開、メタデータなどのオプションについて。
- [**チュートリアル**](https://sekika.github.io/langreader/tutorial/): Wikipediaの記事からリーダーを作成する手順の解説。
- [**音声設定**](https://sekika.github.io/langreader/tts/): デバイス上で高品質な音声を有効にする設定方法。

## インストール

```bash
pip install md-llm-lang-reader
```

*注意: このツールを利用するには、LLMプロバイダ（OpenAI, Anthropicなど）にアクセスするために [multiai](https://sekika.github.io/multiai/) の設定が必要です。*

## クイックスタート

1.  **Markdownファイル（`input.md`）を作成します**:
    ```markdown
    # Bonjour
    Ceci est un exemple de phrase pour l'apprentissage.
    ```

2.  **生成コマンドを実行します**:
    ```bash
    langreader -i input.md -o output.html --src fr --tgt en --provider openai --model gpt-4o-mini
    ```

3.  ブラウザで **`output.html` を開いて**、リーディングとリスニングを始めましょう！

## ライセンス

MIT

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sekika/langreader)
