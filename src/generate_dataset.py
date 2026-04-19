import json
import random
from src.stego_engine import encode_stego, get_bitstream
from tqdm import tqdm

def generate():
    levels = {
        "Dense": "the",
        "Medium": "of",
        "Sparse": "is",
        "Very_Sparse": "however"
    }
    
    with open('datasets/wikitext_test.jsonl') as f:
        all_lines = [json.loads(line)['text'] for line in f if len(json.loads(line)['text']) > 500]
    
    results = []
    
    # Target 5-10 samples per level
    samples_per_level = 10
    
    for level_name, trigger in levels.items():
        print(f"Generating data for level: {level_name} (trigger: '{trigger}')")
        count = 0
        random.shuffle(all_lines)
        for text in tqdm(all_lines):
            if count >= samples_per_level:
                break
                
            # Check if trigger exists in text
            if trigger.lower() not in text.lower():
                continue
            
            # Count occurrences to see how many bits we can hide
            occurrences = len([m.start() for m in re.finditer(f'\\b{trigger}\\b', text, re.IGNORECASE)])
            if occurrences < 3: # Need at least 3 occurrences for a meaningful sparse signal? 
                # For very sparse, maybe 1-2 is okay.
                if level_name != "Very_Sparse" and occurrences < 3:
                    continue
            
            bits = get_bitstream(occurrences)
            stego_text, encoded_count = encode_stego(text, trigger, bits)
            
            if encoded_count > 0:
                results.append({
                    "level": level_name,
                    "trigger": trigger,
                    "original_text": text,
                    "stego_text": stego_text,
                    "bits": bits[:encoded_count],
                    "encoded_count": encoded_count
                })
                count += 1
                
    with open('results/stego_dataset.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Dataset generated with {len(results)} samples.")

if __name__ == "__main__":
    import re
    generate()
