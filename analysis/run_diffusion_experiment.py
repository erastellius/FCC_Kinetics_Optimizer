import sys
import os
import numpy as np
import pandas as pd

# Allow importing from the core_engine directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core_engine.diffusion import FCCSimulation

def run_experiment(total_steps=10000):
    sim = FCCSimulation(size=(20, 20, 20), temp=600)
    
    # Track the real, unwrapped 3D position (ignoring boundary resets for distance math)
    unwrapped_pos = np.array([0.0, 0.0, 0.0])
    start_grid_pos = np.array(sim.vacancy_pos)
    current_grid_pos = np.array(sim.vacancy_pos)
    
    # Lists to store our data
    time_history = []
    msd_history = []
    
    print(f"Running simulation for {total_steps} KMC steps...")
    
    for _ in range(total_steps):
        # Store the position *before* the jump
        old_grid_pos = current_grid_pos.copy()
        
        # Execute the jump
        dt, new_grid_tuple = sim.step()
        current_grid_pos = np.array(new_grid_tuple)
        
        # Calculate the raw vector change between steps
        delta = current_grid_pos - old_grid_pos
        
        # Correct for Periodic Boundary Conditions mapping
        # If the jump distance looks larger than 1 lattice unit, it wrapped around!
        for i in range(3):
            if delta[i] > sim.size[i] / 2:
                delta[i] -= sim.size[i]
            elif delta[i] < -sim.size[i] / 2:
                delta[i] += sim.size[i]
                
        # Update the unwrapped trajectory
        unwrapped_pos += delta
        
        # Calculate Mean Squared Displacement (squared distance from origin)
        msd = np.sum(unwrapped_pos**2)
        
        # Save records
        time_history.append(sim.time)
        msd_history.append(msd)
        
    # Export results to a CSV file in your data folder
    df = pd.DataFrame({'Time_s': time_history, 'MSD_lattice_units2': msd_history})
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/experiment_results.csv', index=False)
    
    # Calculate final D
    final_time = time_history[-1]
    final_msd = msd_history[-1]
    D = final_msd / (6 * final_time)
    
    print("\n--- Experiment Complete ---")
    print(f"Total Physical Time simulated: {final_time:.4e} seconds")
    print(f"Final Mean Squared Displacement: {final_msd:.2f} lattice units^2")
    print(f"Calculated Diffusion Coefficient (D): {D:.4e} lattice_sites^2/s")

if __name__ == "__main__":
    run_experiment()