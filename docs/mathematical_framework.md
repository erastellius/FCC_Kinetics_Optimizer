# Mathematical & Physical Framework Reference
**Project:** Edge FCC Kinetics Optimizer  
**Domain:** Solid-State Transition State Theory & Stochastic Transport Kinetics

---

## 1. Microscopic Jump Kinetics (Transition State Theory)

At the atomic scale, vacancy self-diffusion is governed by thermally activated rare events. An atom adjacent to a crystal vacancy occupies a local potential energy minimum and vibrates within its atomic cage at an attempt frequency $\nu_0$. For an atom to successfully execute a hop into the vacant site, it must overcome a localized migration energy barrier ($E_m$).

According to **Harmonic Transition State Theory (hTST)**, the transition rate (probability per unit time) $r_{ij}$ for a specific neighboring atom $i$ to jump into vacancy $j$ is defined by the Arrhenius rate law:

$$r_{ij} = \nu_0 \exp\left( -\frac{E_m}{k_B T} \right)$$

Where:
- $\nu_0$: The fundamental atomic vibration attempt frequency (typically on the order of the Debye frequency, $\sim 10^{13} \text{ s}^{-1}$). For Aluminum, modeled at $\sim 1 \times 10^{13} \text{ s}^{-1}$.
- $E_m$: The migration enthalpy barrier ($0.650 \text{ eV}$ for pure FCC Aluminum vacancies).
- $k_B$: The Boltzmann Constant ($8.61733324 \times 10^{-5} \text{ eV/K}$).
- $T$: Isothermal system thermodynamic temperature in Kelvin ($\text{K}$).

---

## 2. Stochastic Time Scaling (The Residence-Time Algorithm)

The simulation engine avoids arbitrary time-stepping by employing the **Bortz-Kalos-Lebowitz (BKL)** Kinetic Monte Carlo (KMC) algorithm. Instead of simulating every atomic vibration, the timeline advances dynamically based on the exact aggregate escape probability of the current state.

### A. Total Escape Rate
In a perfect Face-Centered Cubic (FCC) lattice, a vacancy is surrounded by $z = 12$ immediate coordinate nearest neighbors. The cumulative escape configuration rate $R_{\text{tot}}$ represents the sum of all available local transitions:

$$R_{\text{tot}} = \sum_{i=1}^{z} r_i$$

Because our current framework models a pure, un-strained elemental lattice, all 12 neighboring hop rates are isotropic ($r_i = r$), simplifying the expression to:

$$R_{\text{tot}} = 12 \times r$$

### B. Dynamic Time Increment ($\Delta t$)
The probability distribution for the vacancy remaining in its current state over a duration $t$ decays exponentially according to $P(t) = \exp(-R_{\text{tot}} t)$. To translate an execution step into physical real-world time, a continuous random variable $u_1 \in (0, 1]$ is drawn from a uniform distribution, and the stochastic time advance $\Delta t$ is computed via:

$$\Delta t = -\frac{\ln(u_1)}{R_{\text{tot}}}$$

This architecture ensures that at low temperatures (where transition probabilities are low), $\Delta t$ scales up dynamically, allowing the simulation to seamlessly bridge microseconds of physical timeline without wasting computational overhead on dead frames.

---

## 3. Geometric Lattice Mapping & Trajectory Unwrapping

### A. FCC Nearest-Neighbor Vector Space
An FCC lattice constant $a$ denotes the unit cell edge length. The distance between a vacancy and its 12 nearest neighbors is given by the close-packed direction vectors $\frac{a}{2}\langle 110 \rangle$. In localized simulation units (where neighbor spacing $d_{nn} = 1$), the 12 spatial jump paths $\vec{\delta}_k$ are mapped explicitly as:

$$\{\vec{\delta}_k\} = \frac{1}{2} \times \left\{ \begin{matrix} 
(1, 1, 0), & (1, -1, 0), & (-1, 1, 0), & (-1, -1, 0), \\
(1, 0, 1), & (1, 0, -1), & (-1, 0, 1), & (-1, 0, -1), \\
(0, 1, 1), & (0, 1, -1), & (0, -1, 1), & (0, -1, -1)
\end{matrix} \right\}$$

### B. Periodic Boundary Correction (Trajectory Unwrapping)
To eliminate artificial boundary reflection effects, the system utilizes Periodic Boundary Conditions (PBC) over a finite simulation box size $\vec{L} = (L_x, L_y, L_z)$. 

While the core grid coordinates wrap securely using modular arithmetic ($\vec{r}_{\text{grid}} \pmod{\vec{L}}$), calculating spatial diffusion metrics requires an independent **unwrapped coordinate system** $\vec{R}_{\text{unwrapped}}$. After every stochastic jump vector selection $\vec{\delta}_{\text{selected}}$, the engine checks for boundary crossings and maps true displacement natively:

$$\vec{R}_{\text{unwrapped}}(t + \Delta t) = \vec{R}_{\text{unwrapped}}(t) + \text{MinimumImage}(\vec{\delta}_{\text{selected}}, \vec{L})$$

---

## 4. Macroscopic Transport Extraction (Fickian Diffusion)

### A. Mean Squared Displacement (MSD)
The cumulative net distance the defect migrates away from its absolute spatial coordinates at $t=0$ is evaluated using the Mean Squared Displacement metric:

$$\langle \Delta r^2(t) \rangle = \|\vec{R}_{\text{unwrapped}}(t) - \vec{R}_{\text{unwrapped}}(0)\|^2$$

$$\langle \Delta r^2(t) \rangle = [X_{\text{unwrapped}}(t)]^2 + [Y_{\text{unwrapped}}(t)]^2 + [Z_{\text{unwrapped}}(t)]^2$$

### B. Einstein's Relation
For a 3D isotropic random walk across an infinite timeline, Fick's Second Law dictates that the transport diffusion coefficient ($D$) scales as a linear function of its dimensionality ($d=3$):

$$D = \lim_{t \to \infty} \frac{\langle \Delta r^2(t) \rangle}{2 \cdot d \cdot t} \implies D = \frac{\langle \Delta r^2 \rangle}{6t}$$

---

## 5. Thermodynamic Regression Optimization (Arrhenius Linearization)

To extract unknown kinetic activation states empirically, the solver executes a collection of simulations across an array of temperatures. Because $D$ depends exponentially on $T$, we linearize the global transport system:

$$D(T) = D_0 \exp\left( -\frac{E_m}{k_B T} \right)$$

Taking the natural logarithm of both sides converts the equation into a classic linear system ($y = mx + b$):

$$\ln(D) = \left( -\frac{E_m}{k_B} \right) \left(\frac{1}{T}\right) + \ln(D_0)$$

By assigning:
- Dependent Variable ($y$): $\ln(D)$
- Independent Variable ($x$): $\frac{1}{T}$

The optimizer executes a first-order ordinary least-squares polynomial fit ($\text{polyfit}$) over the simulated coordinate data pairs to isolate the slope ($m$):

$$m = \frac{\partial \ln(D)}{\partial (1/T)} = -\frac{E_m}{k_B}$$

The empirical **Migration Energy ($E_m$)** is then dynamically extracted as:

$$E_m = -m \cdot k_B$$

The convergence error is cross-verified against the theoretical physics inputs to evaluate the absolute statistical deviation of the stochastic sample space ensemble.
