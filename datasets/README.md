# Downloaded Datasets

This directory contains samples and instructions for datasets useful for steganography research. Large datasets should be streamed or downloaded on demand.

## WikiText-103
- **Source**: HuggingFace `wikitext/wikitext-103-v1`
- **Use**: Standard large text corpus for language model fine-tuning and testing.
- **Samples**: `datasets/wikitext_samples.json`
- **Download**:
  ```python
  from datasets import load_dataset
  ds = load_dataset('wikitext', 'wikitext-103-v1')
  ```

## IMDb
- **Source**: HuggingFace `imdb`
- **Use**: Movie reviews for sentiment-preserving steganography.
- **Samples**: `datasets/imdb_samples.json`
- **Download**:
  ```python
  from datasets import load_dataset
  ds = load_dataset('imdb')
  ```

## HuggingFace H4 Help4 (Recommended from literature)
- **Source**: `HuggingFaceH4/helpful_instructions`
- **Use**: For fine-tuning LLMs on instructions with embedded steganographic signals.

## Stanford Alpaca (Recommended from literature)
- **Source**: `tatsu-lab/alpaca`
- **Use**: Another instruction-following dataset for generative steganography.

