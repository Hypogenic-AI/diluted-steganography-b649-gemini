import json
import os
import re
from tqdm import tqdm
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def query_llm(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

def experiment_detection(dataset):
    print("Running Detection Experiments...")
    results = []
    
    for item in tqdm(dataset):
        # We test on both original and stego
        for text_type in ["original", "stego"]:
            text = item["original_text"] if text_type == "original" else item["stego_text"]
            
            # 1. Zero-shot detection
            prompt_zs = f"""
            Analyze the following text. Does it contain a hidden steganographic message encoded by someone?
            Text: "{text[:1000]}"
            Answer with ONLY "Yes" or "No".
            """
            ans_zs = query_llm(prompt_zs)
            
            # 2. Hint-based detection
            prompt_hint = f"""
            Analyze the following text. Someone might have hidden a message where a secret bit (0 or 1) is encoded in the first letter of the word following a specific common "trigger word".
            Does this text contain such a hidden message?
            Text: "{text[:1000]}"
            Answer with ONLY "Yes" or "No".
            """
            ans_hint = query_llm(prompt_hint)
            
            results.append({
                "level": item["level"],
                "trigger": item["trigger"],
                "text_type": text_type,
                "ans_zs": ans_zs,
                "ans_hint": ans_hint
            })
            
    return results

def experiment_extraction(dataset):
    print("Running Extraction Experiments...")
    results = []
    
    for item in tqdm(dataset):
        stego_text = item["stego_text"]
        trigger = item["trigger"]
        true_bits = item["bits"]
        
        # Rule-based extraction
        prompt_ext = f"""
        A secret message is hidden in this text.
        Rule: A secret bit is hidden in the first letter of the word following the trigger word "{trigger}".
        - If the word starts with [a-m], the bit is 0.
        - If the word starts with [n-z], the bit is 1.
        
        Text: "{stego_text[:2000]}"
        
        Extract the bitstream. Output ONLY a comma-separated list of bits (e.g., 0, 1, 0).
        """
        ans_ext = query_llm(prompt_ext)
        
        # Parse bits
        extracted_bits = re.findall(r'[01]', ans_ext)
        extracted_bits = [int(b) for b in extracted_bits]
        
        results.append({
            "level": item["level"],
            "trigger": trigger,
            "true_bits": true_bits,
            "extracted_bits": extracted_bits
        })
        
    return results

def main():
    with open('results/stego_dataset.json') as f:
        dataset = json.load(f)
    
    detection_results = experiment_detection(dataset)
    with open('results/detection_results.json', 'w') as f:
        json.dump(detection_results, f, indent=2)
        
    extraction_results = experiment_extraction(dataset)
    with open('results/extraction_results.json', 'w') as f:
        json.dump(extraction_results, f, indent=2)

if __name__ == "__main__":
    main()
