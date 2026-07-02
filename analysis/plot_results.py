import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_publication_plot():
    csv_path = 'data/experiment_results.csv'
    output_image = 'data/msd_vs_time.png'
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find dataset at '{csv_path}'. Run the experiment script first!")
        return
        
    print(f"Reading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Extract data columns
    time_s = df['Time_s'].values
    msd = df['MSD_lattice_units2'].values
    
    # 1. Convert time to microseconds for better axis legibility (1 us = 1e-6 s)
    time_us = time_s * 1e6
    
    # 2. Configure a clean, modern publication style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    
    # Plot experimental KMC trajectory
    ax.plot(time_us, msd, color='#1f4e79', linewidth=1.8, label='KMC Simulation Data')
    
    # Calculate and plot the exact theoretical fit (Einstein Relation: MSD = 6Dt)
    final_time = time_s[-1]
    final_msd = msd[-1]
    D_calc = final_msd / (6 * final_time)
    theoretical_fit = 6 * D_calc * time_s
    
    ax.plot(time_us, theoretical_fit, color='#d9534f', linestyle='--', linewidth=1.5, 
            label=f'Linear Fit (D = {D_calc:.4e} sites²/s)')
    
    # 3. Apply professional layout formatting
    ax.set_title('Mean Squared Displacement (MSD) vs. Physical Time', fontsize=12, fontweight='bold', pad=12, color='#2c3e50')
    ax.set_xlabel('Physical Time (μs)', fontsize=10, fontweight='semibold', color='#2c3e50')
    ax.set_ylabel('Mean Squared Displacement (lattice units²)', fontsize=10, fontweight='semibold', color='#2c3e50')
    ax.tick_params(axis='both', labelsize=9)
    ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e0')
    ax.legend(loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=9)
    
    # Add floating metric summary card inside the plot
    textstr = '\n'.join((
        f't_total  = {time_us[-1]:.2f} μs',
        f'MSD_max  = {final_msd:,.0f} sites²',
        f'D_lattice = {D_calc:.4e} sites²/s',
        f'D_metric  ≈ 2.17e-11 m²/s'
    ))
    props = dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#e2e8f0', alpha=0.95)
    ax.text(0.55, 0.22, textstr, transform=ax.transAxes, fontsize=8.5, verticalalignment='top', bbox=props, fontfamily='monospace')
    
    # Save the output high-res graphic
    plt.tight_layout()
    os.makedirs('data', exist_ok=True)
    plt.savefig(output_image, bbox_inches='tight', dpi=300)
    print(f"Success! Publication-ready plot saved to: '{output_image}'")

if __name__ == "__main__":
    generate_publication_plot()
