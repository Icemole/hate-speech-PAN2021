# PAN 2021: Profiling Hate Speech Spreaders on Twitter

This repository summarizes the work presented to the shared task ["Profiling Hate Speech Spreaders on Twitter"](https://pan.webis.de/clef21/pan21-web/author-profiling.html).

## What to find in this repository

Implementations to tackle this problem by means of:
- n-grams: `src/ngrams`
- fasttext: `src/fasttext-supervised`
- BERT: `src/simpletransformers-bert`

Please see the next section to check which dependencies you should install before executing the programs.

## Dependencies

The whole project has several dependencies, most of which are covered by executing `pip install -r requirements.txt`:
- `nltk`
- `fasttext`
- `simpletransformers`
- `pandas`
- [KenLM](https://kheafield.com/code/kenlm/) (not covered by `requirements.txt`).
  - Install KenLM through your package manager of choice, or [build it from source](https://medium.com/tekraze/install-kenlm-binaries-on-ubuntu-language-model-inference-tool-33507000f33).
  - Tested: Manjaro Linux (installed through `pamac-manager`, AUR package [here](https://aur.archlinux.org/packages/kenlm/)).

## `data/` structure

`data/plain_text`
- **Raw data: only sentences**
- `{hater}_{lang}.txt`: one sentence for each line
- `{hater}_{lang}_grouped.txt`: all sentences from a writer (100 sents) for each line

`data/tok`
- **Tokenized data by NLTK's `TweetTokenizer`**
- `{hater}_{lang}.tok.txt`: all tokenized sentences
- `{hater}_{lang}.tok.{part}.txt`: sentences divided in partitions
- `{hater}_{lang}_grouped.*`: same but grouped as in data/plain_text