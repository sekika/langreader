# langreader

Générez des lecteurs HTML interactifs pour l'apprentissage des langues depuis Markdown grâce aux LLM.

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sekika/langreader/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/sekika/langreader/blob/main/README-ja.md)
[![fr](https://img.shields.io/badge/lang-fr-green.svg)](https://github.com/sekika/langreader/blob/main/README-fr.md)

## 👀 Démo

Avant d'aller plus loin, découvrez ce que cet outil génère :

👉 **[Démo en direct : Lecteur français (Alsace)](https://sekika.github.io/langreader/examples/alsace.html)**

---

`md-llm-lang-reader` (commande CLI : `langreader`) convertit un texte Markdown standard en un lecteur HTML bilingue. Il utilise de grands modèles de langage (via [multiai](https://github.com/sekika/multiai)) pour diviser intelligemment les paragraphes en phrases naturelles et fournir des traductions, tout en ajoutant des fonctionnalités de synthèse vocale (TTS) à chaque phrase.

## Fonctionnalités

- 🤖 **Traduction par IA** : Divise automatiquement les paragraphes en phrases naturelles et les traduit ligne par ligne.
- 🔊 **Synthèse vocale** : Boutons audio intégrés pour chaque phrase source (utilise l'API Web Speech du navigateur).
- ⏯️ **Génération avec reprise** : Vous avez atteint une limite de l'API ? Utilisez `--continue` pour reprendre la génération exactement là où elle s'est arrêtée.
- 📝 **Support Markdown** : Préserve les titres, les blocs de code et le formatage de base.
- 🌍 **Assistant Wikipedia** : Inclut un script pour récupérer et formater facilement des articles Wikipedia pour l'apprentissage.

## 📚 Documentation

Pour des instructions d'installation détaillées, les options CLI et les tutoriels, veuillez consulter la documentation officielle :

👉 **[https://sekika.github.io/langreader/](https://sekika.github.io/langreader/)**

- [**Guide d'utilisation**](https://sekika.github.io/langreader/usage/) : Options de style, reprise de génération et métadonnées.
- [**Tutoriel**](https://sekika.github.io/langreader/tutorial/) : Guide étape par étape pour créer un lecteur à partir d'un article Wikipedia.
- [**Configuration TTS**](https://sekika.github.io/langreader/tts/) : Comment configurer des voix de haute qualité sur votre appareil.

## Installation

```bash
pip install md-llm-lang-reader
```

*Note : Cet outil nécessite la configuration de [multiai](https://sekika.github.io/multiai/) pour accéder aux fournisseurs de LLM (OpenAI, Anthropic, etc.).*

## Démarrage rapide

1.  **Créez un fichier Markdown (`input.md`)** :
    ```markdown
    # Bonjour
    Ceci est un exemple de phrase pour l'apprentissage.
    ```

2.  **Lancez le générateur** :
    ```bash
    langreader -i input.md -o output.html --src fr --tgt en --provider openai --model gpt-4o-mini
    ```

3.  **Ouvrez `output.html`** dans votre navigateur pour commencer à lire et à écouter !

## Licence

MIT