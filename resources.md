# Resources Catalog: Diluted Steganography

## Summary
This document catalogs all gathered resources, including papers, datasets, and code repositories, to support research on diluted steganography in LLMs.

## Papers
Total papers downloaded: 8

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Hide and Seek in Embedding Space | Westphal et al. | 2026 | papers/2601.22818v1_... | Low-recoverability, mechanistic detection |
| GSDFuse: Multi-Dimensional Weak Signals | Huang et al. | 2025 | papers/2505.17085v1_... | Extreme steganographic sparsity |
| Provably Secure Generative Steganography | Zhang et al. | 2021 | papers/2106.02011v1_... | Secure ADG (Adaptive Dynamic Grouping) |
| Neural Linguistic Steganography | Ziegler et al. | 2019 | papers/1909.01496v1_... | Arithmetic coding with LMs |
| LLM-Stega | Lu et al. | 2024 | papers/2404.10229v2_... | Modern generative steganography baseline |
| Provably Secure Disambiguating | JavDomGom et al. | 2024 | papers/2403.17524v2_... | Secure disambiguation techniques |
| Near-imperceptible SAAC | Shen et al. | 2020 | papers/2010.00677v1_... | Self-adjusting arithmetic coding |
| Pseudorandom Error-Correcting Codes | Christ et al. | 2024 | papers/2402.09370v2_... | Robust, undetectable watermarking |

See `papers/README.md` for detailed descriptions.

## Datasets
Total datasets referenced: 4

| Name | Source | Task | Location | Notes |
|------|--------|------|----------|-------|
| WikiText-103 | HuggingFace | Fine-tuning/LM | `datasets/wikitext_samples.json` | Large corpus for testing fluency |
| IMDb | HuggingFace | Sentiment-preserving | `datasets/imdb_samples.json` | Useful for content-constrained stego |
| Help4 Team Help4 | HuggingFace | Instruction-tuning | HF Hub: `HuggingFaceH4/helpful_instructions` | Recommended for LLM fine-tuning |
| Stanford Alpaca | HuggingFace | Instruction-following | HF Hub: `tatsu-lab/alpaca` | Standard benchmark for LLM research |

See `datasets/README.md` for more info and download instructions.

## Code Repositories
Total repositories cloned: 3

| Name | Purpose | Location | Notes |
|------|---------|----------|-------|
| Text-Steganography-Benchmark | Evaluating various methods | `code/text-steganography-benchmark/` | Comprehensive baseline scripts |
| LLM-Steganography | LLM-Stega official code | `code/llm-steganography/` | Modern generative implementation |
| TrojanStego | Bit-bucket attack implementation | `code/trojan-stego/` | Reference for training-time steganography |

See `code/README.md` for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
- Used `paper-finder` for relevance-ranked academic papers.
- Conducted targeted GitHub searches for "TrojanStego" and "LLM steganography".
- Browsed HuggingFace for recent steganography/steganalysis datasets and benchmark corpora.

### Selection Criteria
- Priority 1: High-relevance (score >= 2) papers from the last 3 years.
- Priority 2: Established benchmarks and implementations from top-tier research groups (Redwood Research, etc.).
- Priority 3: Datasets commonly cited in the downloaded literature.

### Gaps and Workarounds
- No dedicated "diluted steganography" dataset exists. Workaround: Sampled large corpora like WikiText-103 and IMDb to create custom, sparsely-embedded test cases in the next phase.

## Recommendations for Experiment Design

1. **Primary Dataset**: Use `WikiText-103` for broad text and `IMDb` for sentiment-constrained testing.
2. **Baseline Method**: Use `LLM-Stega` and `Arithmetic Coding` (from `text-steganography-benchmark`).
3. **Evaluation Metrics**: Measure `Payload Recoverability`, `KL Divergence`, `Perplexity`, and `Detection Accuracy` using internal activation probes (as suggested in "Hide and Seek").
4. **Code to Adapt**: Use `text-steganography-benchmark` for standard metrics and `trojan-stego` for fine-tuning-based attacks.

