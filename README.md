# Diluted Steganography Research

This project investigates the limits of Large Language Models (LLMs) in detecting and extracting steganographic signals when they are "diluted" or "sparse" within a text.

## Key Findings
- **Zero Visibility:** State-of-the-art LLMs (GPT-4o) were unable to detect steganography in word-trigger patterns even at high density (e.g., bits after every occurrence of "the"), yielding 0% True Positive Rate.
- **Dilution Defense:** Signal dilution (lower trigger frequency) effectively protects against zero-shot detection.
- **Extraction Bottleneck:** While LLMs can extract local bits (71% accuracy for 1-bit sparse signals), their performance degrades significantly over long sequences (BER > 0.5 for 10-bit dense signals), likely due to context tracking failures.

## Project Structure
- `src/stego_engine.py`: Core steganographic encoding logic.
- `src/generate_dataset.py`: Script to generate stego-text at various dilution levels.
- `src/experiment.py`: Script to evaluate LLMs on detection and extraction tasks.
- `src/analyze_results.py`: Script to calculate accuracy and BER.
- `results/`: Contains experimental datasets and final summary CSVs/plots.

## Reproduction
1. Set up the environment:
   ```bash
   uv venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
2. Generate the dataset:
   ```bash
   python src/generate_dataset.py
   ```
3. Run the LLM experiments:
   ```bash
   export OPENAI_API_KEY="your-key"
   python src/experiment.py
   ```
4. Analyze and plot results:
   ```bash
   python src/analyze_results.py
   python src/plot_results.py
   ```

For full details, see **[REPORT.md](REPORT.md)**.
