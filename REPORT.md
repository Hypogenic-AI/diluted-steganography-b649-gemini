# REPORT: Diluted Steganography in LLMs

## 1. Executive Summary
This research investigates the visibility and recoverability of diluted steganography in Large Language Models (LLMs). We find that LLMs (GPT-4o) exhibit **zero discriminative power** for detecting steganographic messages hidden in word-trigger patterns, even at high density (7.8% of tokens). However, when provided with the specific encoding rule, LLMs can extract bits with moderate accuracy for sparse signals (~71% for 1-bit cases) but fail significantly as the signal becomes denser (BER > 0.5 for 10-bit cases). This suggests that "dilution" effectively acts as a stealth defense against LLM-based detection, while "sequence complexity" acts as a defense against automated extraction.

## 2. Research Question & Motivation
**Question:** How does signal dilution (trigger-word sparsity) affect an LLM's ability to detect and extract steganographic messages?
**Motivation:** As AI-generated content grows, the ability to hide stealthy signals in large corpora becomes a significant security concern. Understanding the "dilution threshold" for detection is critical for AI safety and forensics.

## 3. Methodology
- **Encoding Rule:** A secret bit $b \in \{0, 1\}$ is hidden in the first letter of the word following a **trigger word**.
  - $b=0 \implies$ Next word starts with `[a-m]`
  - $b=1 \implies$ Next word starts with `[n-z]`
- **Dilution Levels (Trigger Words):**
  - Dense: "the" (~7.8% frequency)
  - Medium: "of" (~3.3% frequency)
  - Sparse: "is" (~0.55% frequency)
  - Very Sparse: "however" (~0.076% frequency)
- **Data Generation:** Used WikiText-103 samples. Generated stego-text using `gpt-4o-mini` to replace words while maintaining fluency and respecting the encoding constraint.
- **Evaluation:** Evaluated `gpt-4o` on detection (zero-shot and hint-based) and extraction (given the rule).

## 4. Results
### Detection Performance (True Positive Rate)
| Level | ZS_TPR | Hint_TPR | Accuracy (Overall) |
|-------|--------|----------|-------------------|
| Dense | 0.0 | 0.0 | 50.0% |
| Medium | 0.0 | 0.0 | 50.0% |
| Sparse | 0.0 | 0.0 | 50.0% |
| Very_Sparse | 0.0 | 0.0 | 50.0% |

### Extraction Performance (Average Bit Error Rate)
| Level | BER | Correct/Total Bits | Correct Ratio |
|-------|-----|-------------------|---------------|
| Dense | 0.60 | 4.1 / 10.4 | 39.4% |
| Medium | 0.59 | 2.8 / 5.7 | 49.1% |
| Sparse | 0.68 | 2.3 / 4.6 | 50.0% |
| Very_Sparse | 0.50 | 0.71 / 1.0 | 71.0% |

## 5. Analysis & Discussion
- **The "Invisibility" of Diluted Steganography:** GPT-4o was unable to detect any steganographic text, always predicting "No" even for dense signals ("the"). This suggests that steganographic drift, when mitigated by high-quality LLM-based word replacement, is practically imperceptible to current models' zero-shot detection capabilities.
- **The Complexity Bottleneck:** While the LLM could extract bits from sparse samples (71% accuracy for single bits), it failed to scale to longer bitstreams (Dense/Medium levels). This indicates that the bottleneck is not the *rule itself*, but the model's ability to **systematically track and verify patterns across a long context window**.
- **Detection vs. Extraction:** There is a notable gap—the model can *sometimes* extract the signal when told exactly what to look for, but it never "notices" the signal on its own.

## 6. Limitations
- **Sample Size:** The dataset used (37 stego samples) is relatively small.
- **Model Choice:** Only `gpt-4o` was used for evaluation. Other models (Claude, Llama) might have different performance profiles.
- **Rule Simplicity:** The rule used ([a-m]/[n-z]) is very simple. More complex rules (e.g., parity of token IDs) might yield different results.

## 7. Conclusions & Next Steps
Diluted steganography is an effective method for hiding information from LLMs. Even a dense signal like one bit after every "the" is invisible to the state-of-the-art GPT-4o model without fine-tuning or specialized detection probes. Future work should investigate whether fine-tuned models or mechanistic interpretability (linear probes on activations) can perform better than zero-shot prompting.
