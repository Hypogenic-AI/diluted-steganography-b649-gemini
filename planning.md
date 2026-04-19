# Research Plan: Diluted Steganography

## Motivation & Novelty Assessment

### Why This Research Matters
As data generation becomes cheaper and more prolific, the dilution of meaningful signals within large corpora is likely to become a significant issue. Steganography is often used to hide information, and current LLMs are quite good at detecting simple patterns. However, "diluted" signals—where the information is sparse and tied to rare events—might be much harder to detect. This has implications for AI safety (e.g., hidden instructions in training data) and digital forensics.

### Gap in Existing Work
Existing steganography research (e.g., LLM-Stega, Hide and Seek) focuses on high-capacity or embedding-level hiding. There is limited research on the "dilution limit"—the point where a signal becomes so sparse that it is indistinguishable from noise for a general-purpose LLM, even if the LLM is prompted to look for it.

### Our Novel Contribution
We systematically investigate the "Dilution Factor" (frequency of signal-carrying tokens) and its impact on LLM detection and extraction performance. We specifically look at trigger-word-based dilution, which is more realistic for "needle-in-a-stack" scenarios.

### Experiment Justification
- **Experiment 1 (Detection):** Tests if LLMs can identify the presence of a hidden message at various dilution levels. This establishes the "visibility" threshold.
- **Experiment 2 (Extraction):** Tests if LLMs can recover the message when the rule is provided. This measures the "recoverability" under sparsity.

---

## Research Question
How does signal dilution (specifically trigger-word-based sparsity) affect the ability of Large Language Models to detect and extract steganographic messages?

## Hypothesis Decomposition
1. **Detection Degradation:** The probability of an LLM correctly identifying steganographic text decreases as the dilution factor increases (i.e., as the trigger word becomes rarer).
2. **Extraction Resilience:** If the rule is known, LLM extraction accuracy (Bit Error Rate) will remain relatively stable until extreme dilution levels where context windows or attention mechanisms might fail to link distant signal tokens.
3. **Zero-shot vs. Few-shot:** Few-shot prompting will significantly improve detection of diluted signals compared to zero-shot, but will still struggle with high dilution.

## Proposed Methodology

### Approach
We will use a "Trigger-Word Steganography" method. A secret bit is encoded in the properties of the word immediately following a "trigger word". 
- **Rule:** If bit is 0, the next word starts with [a-m]. If bit is 1, it starts with [n-z].
- **Dilution:** Controlled by selecting trigger words of varying frequencies in the WikiText-103 dataset.
    - Level 1 (Dense): Trigger = "the" (approx. 7% of tokens)
    - Level 2 (Medium): Trigger = "of" (approx. 3% of tokens)
    - Level 3 (Sparse): Trigger = "which" (approx. 0.5% of tokens)
    - Level 4 (Very Sparse): Trigger = "nevertheless" or similar (approx. 0.01% of tokens)

### Experimental Steps
1. **Data Prep:** Extract samples from WikiText-103. Identify occurrences of target trigger words.
2. **Encoding:** Generate "Stego-Text" by modifying the words following triggers to encode a random bitstream. Ensure the resulting text remains fluent (using an LLM to "re-write" or "fill in" while respecting the constraint).
3. **Detection Baseline:** Use GPT-4o / Claude 3.5 Sonnet to detect stego-text vs. original text.
4. **Extraction Baseline:** Use the same models to extract the bitstream given the trigger word and encoding rule.

### Baselines
- **Negative Control:** Original WikiText samples.
- **Positive Control:** High-density steganography (e.g., every first letter of every word).

### Evaluation Metrics
- **Detection:** Accuracy, F1-score, False Positive Rate.
- **Extraction:** Bit Error Rate (BER).
- **Fluency:** Perplexity (using a local model like GPT-2 or a small Llama if available, or just qualitative LLM scoring).

## Success Criteria
- Successful completion of the "Dilution vs. Performance" curve for at least two major LLMs.
- Identification of the "Dilution Threshold" where detection drops to near-chance levels.
