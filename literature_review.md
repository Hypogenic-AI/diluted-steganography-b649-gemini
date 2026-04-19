# Literature Review: Diluted Steganography in Large Language Models

## Research Area Overview
Steganography in natural language processing (NLP) has evolved from simple rule-based methods (e.g., zero-width characters) to generative approaches that leverage the probabilistic nature of language models. Recent research focuses on "generative steganography," where secret messages are embedded by subtly altering the probability distribution of generated tokens. The concept of "diluted steganography" or "steganographic sparsity" addresses scenarios where hidden messages are not present in every token but are dispersed (diluted) according to specific patterns (e.g., every $N$-th word or after specific trigger tokens).

## Key Papers

### 1. Hide and Seek in Embedding Space (2026)
- **Authors**: Charles Westphal, K. Navaie, F. Rosas
- **Key Contribution**: Introduces "low-recoverability steganography" using embedding-space geometry. It reduces the chance of a defender recovering the secret without the key by using hyperplane projections in the model's internal embedding space for bit-to-token mappings.
- **Methodology**: Uses random hyperplanes in embedding space to partition tokens into "buckets" for secret bits.
- **Detection**: Proposes mechanistic interpretability (linear probes on internal activations) as a superior detection signal compared to output-level distribution shifts (KL divergence, perplexity), which are often masked by fine-tuning drift.
- **Relevance**: Directly addresses how modern LLMs can be fine-tuned to hide secrets and identifies the limitations of traditional steganalysis.

### 2. GSDFuse (2025)
- **Authors**: Kaibo Huang, Zipei Zhang, et al.
- **Key Contribution**: Addresses "extreme steganographic sparsity" in multi-interaction dialogues (social media).
- **Methodology**: Uses multi-dimensional weak signals and hierarchical multi-modal feature fusion to detect dispersed steganographic content.
- **Relevance**: Provides a framework for detecting "diluted" signals that are spread across contexts rather than concentrated in a single sentence.

### 3. TrojanStego (Meier et al., 2025)
- **Key Contribution**: Demonstrates how LLMs can be fine-tuned to encode secrets in output tokens (e.g., using parity of token IDs) while maintaining fluency.
- **Methodology**: Bit-bucket constrained generation during fine-tuning.
- **Relevance**: Shows the feasibility of persistent, model-internal steganography that can be triggered by specific prompt patterns.

### 4. Generative Text Steganography with Large Language Model (2024)
- **Authors**: Tianhe Lu et al. (LLM-Stega)
- **Key Contribution**: A black-box approach to generative steganography that balances perceptual and statistical imperceptibility.
- **Relevance**: Practical baseline for modern LLM-based steganography.

## Common Methodologies
- **Arithmetic Coding**: Standard for mapping secret bits to tokens according to their predicted probabilities (e.g., Ziegler et al., 2019).
- **Bit Buckets**: Partitioning the vocabulary into sets representing 0 or 1, used in both inference-time and training-time (TrojanStego) attacks.
- **Embedding Geometry**: Using internal representations (hyperplanes) for bucketing instead of arbitrary mappings (Hide and Seek).

## Standard Baselines
- **ADG (Adaptive Dynamic Grouping)**: A common baseline for generative steganography.
- **Arithmetic Coding (AC)**: Baseline for compression-based steganography.
- **HC (Huffman Coding)**: Simpler coding baseline.

## Evaluation Metrics
- **Payload Recoverability**: How easily an unauthorized defender can extract the secret.
- **KL Divergence**: Statistical shift from the base model's distribution.
- **Perplexity (PPL)**: Measures the fluency and naturalness of the steganographic text.
- **Bit Rate (bits per token)**: The amount of information hidden per unit of text.

## Gaps and Opportunities
- **Signal Dilution Detection**: Most current steganalysis assumes a relatively dense signal. Investigating how LLMs handle very sparse signals (e.g., 1 bit per 100 tokens) is an open area.
- **Mechanistic Interpretability for Diluted Signals**: Can linear probes detect steganography if the "trigger" for encoding is very rare?

## Recommendations for Our Experiment
1. **Focus on Signal Sparsity**: Systematically vary the "dilution factor" (e.g., bits per $N$ tokens) to find the threshold where current detection methods fail.
2. **Use Mechanistic Interpretability**: Compare output-level metrics (KL, PPL) with internal probes on late-layer activations, as suggested by Westphal et al. (2026).
3. **Trigger-based Sparsity**: Hide messages only after specific low-frequency tokens to simulate highly targeted exfiltration.

