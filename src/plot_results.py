import pandas as pd
import matplotlib.pyplot as plt

def plot_results():
    det_df = pd.read_csv('results/detection_summary.csv')
    ext_df = pd.read_csv('results/extraction_summary.csv')
    
    # Reorder levels logically
    level_order = ['Dense', 'Medium', 'Sparse', 'Very_Sparse']
    det_df['Level'] = pd.Categorical(det_df['Level'], categories=level_order, ordered=True)
    ext_df['Level'] = pd.Categorical(ext_df['Level'], categories=level_order, ordered=True)
    det_df = det_df.sort_values('Level')
    ext_df = ext_df.sort_values('Level')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot Detection TPR (Visibility)
    ax1.plot(det_df['Level'], det_df['ZS_TPR'], marker='o', label='Zero-Shot TPR')
    ax1.plot(det_df['Level'], det_df['Hint_TPR'], marker='s', label='Hint-Based TPR')
    ax1.set_ylim(-0.1, 1.1)
    ax1.set_title('Detection Performance (True Positive Rate)')
    ax1.set_ylabel('TPR')
    ax1.legend()
    ax1.grid(True)
    
    # Plot Extraction BER
    ax2.plot(ext_df['Level'], ext_df['BER'], marker='x', color='red', label='Bit Error Rate (BER)')
    ax2.axhline(y=0.5, color='gray', linestyle='--', label='Random Chance')
    ax2.set_ylim(0, 1.1)
    ax2.set_title('Extraction Performance (BER)')
    ax2.set_ylabel('BER')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('results/performance_plot.png')
    print("Plot saved to results/performance_plot.png")

if __name__ == "__main__":
    plot_results()
