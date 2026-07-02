import numpy as np

class FCCSimulation:
    def __init__(self, size=(10, 10, 10), temp=600): 
        self.size = size
        self.temp = temp
        self.kb = 8.617e-5  # Boltzmann constant in eV/K
        self.Em = 0.65      # Migration energy for Al in eV
        self.nu_0 = 1e13    # Attempt frequency in s^-1
        
        # Track continuous simulation time
        self.time = 0.0
        
        # Spawn the vacancy precisely in the middle of our 3D grid
        self.vacancy_pos = (size[0] // 2, size[1] // 2, size[2] // 2)
        
    def get_neighbors(self, x, y, z):
        """Returns the 12 nearest neighbor coordinates for an FCC lattice using PBC."""
        fcc_vectors = [
            (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
            (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),
            (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)
        ]
        neighbors = []
        for dx, dy, dz in fcc_vectors:
            nx = (x + dx) % self.size[0]
            ny = (y + dy) % self.size[1]
            nz = (z + dz) % self.size[2]
            neighbors.append((nx, ny, nz))
        return neighbors

    def calculate_rate(self):
        """Returns the single hop rate for Aluminum."""
        return self.nu_0 * np.exp(-self.Em / (self.kb * self.temp))

    def step(self):
        """Perform one complete Kinetic Monte Carlo step."""
        # 1. Look around: Find the 12 neighbors for the vacancy's current spot
        neighbors = self.get_neighbors(*self.vacancy_pos)
        
        # 2. Add up the total rate of escaping this position
        single_rate = self.calculate_rate()
        total_rate = len(neighbors) * single_rate  # 12 * single_rate
        
        # 3. Pick which neighbor to swap with
        # Since this is an unstrained, pure metal, all 12 paths have equal probability
        chosen_index = np.random.randint(0, len(neighbors))
        self.vacancy_pos = neighbors[chosen_index]
        
        # 4. Advance time using the Residence-Time math
        r = np.random.uniform(1e-10, 1.0)  # Avoid exactly 0 to prevent log(0) error
        dt = -np.log(r) / total_rate
        
        self.time += dt
        return dt, self.vacancy_pos

if __name__ == "__main__":
    sim = FCCSimulation()
    print("Starting KMC trajectory loop...")
    print(f"Initial vacancy position: {sim.vacancy_pos}\n")
    
    # Simulate 5 consecutive jumps
    for i in range(1, 6):
        dt, new_pos = sim.step()
        print(f"Jump #{i}: Took {dt:.4e} seconds -> Moved to {new_pos} | Total Time: {sim.time:.4e} s")