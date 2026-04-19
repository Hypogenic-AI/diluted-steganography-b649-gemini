import os
import re
import json
import random
from tqdm import tqdm
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bitstream(text_len):
    """Generate a random bitstream of given length."""
    return [random.randint(0, 1) for _ in range(text_len)]

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def get_replacement_word(prev_text, current_word, target_bit, model="gpt-4o-mini"):
    """
    Get a contextually appropriate replacement for current_word that satisfies the stego-rule.
    Rule: 0 -> [a-m], 1 -> [n-z]
    """
    range_desc = "[a-m]" if target_bit == 0 else "[n-z]"
    prompt = f"""
    Sentence so far: "{prev_text}"
    Original next word: "{current_word}"
    Constraint: The replacement for "{current_word}" MUST start with a letter in the range {range_desc} (case-insensitive).
    Task: Provide ONLY the replacement word that is contextually appropriate and fluent. 
    If "{current_word}" already satisfies the constraint, you can just return it.
    If you must change it, ensure it fits well.
    Output ONLY the word.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    new_word = response.choices[0].message.content.strip().strip('"').strip("'")
    # Basic validation
    first_char = new_word[0].lower()
    if target_bit == 0:
        if not ('a' <= first_char <= 'm'):
            # Fallback to a simple common word if LLM fails
            return "amazing" if target_bit == 0 else "nice"
    else:
        if not ('n' <= first_char <= 'z'):
            return "wonderful" if target_bit == 1 else "great"
    return new_word

def encode_stego(text, trigger_word, bitstream):
    """
    Encode bitstream into text after trigger_word.
    Returns the stego-text and the number of bits actually encoded.
    """
    tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
    stego_tokens = []
    bit_idx = 0
    
    for i in range(len(tokens)):
        stego_tokens.append(tokens[i])
        if tokens[i].lower() == trigger_word.lower() and i + 1 < len(tokens) and bit_idx < len(bitstream):
            next_word = tokens[i+1]
            # If it's a word, we can encode
            if re.match(r'\w+', next_word):
                target_bit = bitstream[bit_idx]
                prev_text = " ".join(stego_tokens[-10:]) # last 10 tokens for context
                new_word = get_replacement_word(prev_text, next_word, target_bit)
                # We replace in the NEXT iteration? No, we skip the next word if we replace it now.
                # Actually, let's just handle it here.
                # tokens[i+1] will be processed in the next loop. 
                # Better: modify the list in place or use a different loop.
                pass # see below
    
    # Re-implementing with index to handle replacement
    stego_tokens = []
    bit_idx = 0
    i = 0
    while i < len(tokens):
        token = tokens[i]
        stego_tokens.append(token)
        if token.lower() == trigger_word.lower() and i + 1 < len(tokens) and bit_idx < len(bitstream):
            # Check if tokens[i+1] is a word
            if re.match(r'\w+', tokens[i+1]):
                target_bit = bitstream[bit_idx]
                prev_context = " ".join(stego_tokens[-10:])
                replacement = get_replacement_word(prev_context, tokens[i+1], target_bit)
                stego_tokens.append(replacement)
                bit_idx += 1
                i += 2 # skip original next word
                continue
        i += 1
    
    return " ".join(stego_tokens), bit_idx

def main():
    # Test
    sample_text = "The quick brown fox jumps over the lazy dog."
    trigger = "the"
    bits = [0, 1]
    stego, count = encode_stego(sample_text, trigger, bits)
    print(f"Original: {sample_text}")
    print(f"Trigger: {trigger}, Bits: {bits}")
    print(f"Stego: {stego}")
    print(f"Bits encoded: {count}")

if __name__ == "__main__":
    main()
