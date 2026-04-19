import json
import pandas as pd
import numpy as np

def analyze_detection():
    with open('results/detection_results.json') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Map Yes/No to boolean
    df['zs_pred'] = df['ans_zs'].str.contains('Yes', case=False)
    df['hint_pred'] = df['ans_hint'].str.contains('Yes', case=False)
    df['is_stego'] = df['text_type'] == 'stego'
    
    levels = df['level'].unique()
    
    results = []
    for level in levels:
        subset = df[df['level'] == level]
        
        # Zero-shot
        tpr_zs = subset[subset['is_stego']]['zs_pred'].mean()
        fpr_zs = subset[~subset['is_stego']]['zs_pred'].mean()
        acc_zs = (subset['zs_pred'] == subset['is_stego']).mean()
        
        # Hint-based
        tpr_hint = subset[subset['is_stego']]['hint_pred'].mean()
        fpr_hint = subset[~subset['is_stego']]['hint_pred'].mean()
        acc_hint = (subset['hint_pred'] == subset['is_stego']).mean()
        
        results.append({
            "Level": level,
            "ZS_Accuracy": acc_zs,
            "ZS_TPR": tpr_zs,
            "ZS_FPR": fpr_zs,
            "Hint_Accuracy": acc_hint,
            "Hint_TPR": tpr_hint,
            "Hint_FPR": fpr_hint
        })
        
    return pd.DataFrame(results)

def analyze_extraction():
    with open('results/extraction_results.json') as f:
        data = json.load(f)
    
    results = []
    for item in data:
        true_bits = item['true_bits']
        extracted_bits = item['extracted_bits']
        
        # Match lengths for comparison (pad/truncate)
        min_len = min(len(true_bits), len(extracted_bits))
        if min_len == 0:
            ber = 1.0 # Max error if nothing extracted
        else:
            errors = sum(1 for i in range(min_len) if true_bits[i] != extracted_bits[i])
            # Account for missing bits
            total_possible = max(len(true_bits), len(extracted_bits))
            errors += abs(len(true_bits) - len(extracted_bits))
            ber = errors / total_possible
            
        results.append({
            "Level": item['level'],
            "BER": ber,
            "Correct_Bits": min_len - (sum(1 for i in range(min_len) if true_bits[i] != extracted_bits[i]) if min_len > 0 else 0),
            "Total_Bits": len(true_bits),
            "Extracted_Count": len(extracted_bits)
        })
        
    df = pd.DataFrame(results)
    return df.groupby('Level').mean().reset_index()

def main():
    det_df = analyze_detection()
    ext_df = analyze_extraction()
    
    print("\n--- Detection Results ---")
    print(det_df)
    
    print("\n--- Extraction Results (Average BER) ---")
    print(ext_df)
    
    det_df.to_csv('results/detection_summary.csv', index=False)
    ext_df.to_csv('results/extraction_summary.csv', index=False)

if __name__ == "__main__":
    main()
