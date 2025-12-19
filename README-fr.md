# md-llm-lang-reader

Outil pour générer un « lecteur HTML pour l’apprentissage des langues » à partir d’un fichier Markdown (découpage en phrases + traduction via LLM, avec boutons TTS).

- Découpe chaque paragraphe en phrases naturelles
- Ajoute une traduction (langue cible) pour chaque phrase
- Bouton de lecture (TTS) en un clic pour le texte source
- Les blocs de code délimités (``` ou ~~~) ne sont pas envoyés au LLM et sont exportés tels quels en HTML

Le nom du paquet PyPI est `md-llm-lang-reader` et la commande installée est `langreader`.

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/sekika/langreader/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/sekika/langreader/blob/main/README-ja.md)
[![fr](https://img.shields.io/badge/lang-fr-green.svg)](https://github.com/sekika/langreader/blob/main/README-fr.md)

## Fonctionnalités

- Conversion Markdown → HTML (titres + paragraphes, volontairement simple)
- Découpage en phrases par LLM (frontières de phrases plus naturelles)
- Traduction phrase par phrase (source + cible)
- Bouton TTS pour chaque phrase source
- Blocs de code délimités conservés (non traduits)
- Les listes à puces sont traduites (elles sont transmises au LLM comme du texte normal)

## Installation

```bash
pip install md-llm-lang-reader
```

## Configuration de multiai

Cet outil utilise **multiai** en interne pour accéder aux fournisseurs de LLM.
Avant d’utiliser `langreader`, il est nécessaire de configurer **multiai** pour le fournisseur et le modèle que vous souhaitez utiliser.

Les détails concernant les fournisseurs pris en charge et la procédure de configuration sont disponibles ici :

https://sekika.github.io/multiai/

Veuillez suivre la documentation de multiai pour effectuer la configuration requise.

## Démarrage rapide

Créez `input.md` :

```md
# Exemple

Bonjour ! Ceci est un court paragraphe.

```python
# Les blocs de code ne sont pas traduits
print("Hello")
```

- Premier point
- Deuxième point
```

Générez `output.html` :

```bash
langreader \
  -i input.md \
  -o output.html \
  --src fr \
  --tgt en \
  --provider YOUR_PROVIDER \
  --model YOUR_MODEL
```

Ouvrez ensuite `output.html` dans un navigateur et cliquez sur les boutons haut-parleur.

## Utilisation (CLI)

```bash
langreader -i INPUT.md -o OUTPUT.html --src SRC --tgt TGT --provider PROVIDER --model MODEL [-v 0|1|2|3]
```

### Options

- `-i, --input` (obligatoire)  
  Chemin vers le fichier Markdown d’entrée.

- `-o, --output` (obligatoire)  
  Chemin vers le fichier HTML de sortie.

- `--src` (défaut : `fr`)  
  Code de langue de la source (ex. `fr`, `de`, `es`, `ja`).

- `--tgt` (défaut : `en`)  
  Code de langue de la traduction.

- `--provider` (obligatoire)  
  Identifiant du provider à passer à `multiai` (dépend de votre configuration `multiai`).

- `--model` (obligatoire)  
  Nom/identifiant du modèle à passer à `multiai`.

- `-v, --verbose` (défaut : `1`)  
  Niveau de verbosité :
  - `0` : silencieux
  - `1` : titres uniquement
  - `2` : aperçu du paragraphe (environ les 5 premiers mots)
  - `3` : paragraphe source complet

### Exemples

Français → Anglais :

```bash
langreader -i alsace.md -o alsace.html --src fr --tgt en --provider ... --model ...
```

Allemand → Anglais :

```bash
langreader -i berlin.md -o berlin.html --src de --tgt en --provider ... --model ...
```

Japonais → Anglais :

```bash
langreader -i news.md -o news.html --src ja --tgt en --provider ... --model ...
```

## Principe de fonctionnement

Pour chaque paragraphe, l’outil demande au LLM :

1. de découper le paragraphe en phrases naturelles (sans couper abusivement sur des abréviations)
2. de traduire chaque phrase vers la langue cible
3. de retourner uniquement du JSON valide (sans Markdown, sans commentaire)

Schéma JSON attendu :

```json
[
  { "src": "…", "tgt": "…" }
]
```

Le JSON est ensuite validé et transformé en HTML : phrase source + bouton TTS, puis la traduction en dessous.

## À propos de la synthèse vocale (TTS)

- La TTS utilise l’API Web Speech du navigateur (`speechSynthesis`).
- Les voix disponibles dépendent du système d’exploitation et du navigateur.
- La langue de lecture est définie via `--src` (par ex. `fr`).
  Si vous souhaitez préciser une locale (par ex. `fr-FR`), il faut pour l’instant modifier le HTML généré (une option CLI pourra être ajoutée plus tard).

## Support Markdown (actuel)

Pris en charge :
- Titres : `#`, `##`, `###`, `####`
- Paragraphes : lignes non vides concaténées avec des espaces ; séparation par lignes vides
- Blocs de code délimités : ``` / ~~~ (les info strings sont acceptées)

Non pris en charge (pas de rendu spécifique) :
- Citations, tableaux, images
- Mise en forme inline (liens, emphase, etc.) : le texte est traité comme du texte brut

Si vous avez besoin d’un rendu Markdown complet, envisagez l’intégration d’un parseur Markdown et une stratégie pour préserver la correspondance entre texte original et rendu HTML.

## Sécurité

- Le texte est échappé lors de la génération HTML.
- Le texte n’est pas injecté directement dans des handlers `onclick`. Les boutons stockent le texte dans un attribut `data-speak="..."` et un écouteur d’événements JS le lit, ce qui évite les problèmes de guillemets et réduit le risque XSS.

Si votre Markdown d’entrée n’est pas de confiance, considérez le HTML généré comme potentiellement non fiable.

## Développement

Installation en mode editable :

```bash
pip install -e .
```

Tests :

```bash
pytest
```

Build :

```bash
python -m build
```

## Licence

MIT
