import scipy
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

fig=plt.figure()
ax = fig.add_subplot(projection='3d')

# Define the system of ODEs
def function(state, t, m, n, g, b, k, F, J):
    phi, psi, omega=state.tolist()
    dphi_dt=omega
    dpsi_dt=n**2*omega**2*np.sin(phi)*np.cos(phi)-g*np.sin(phi)-b/m*psi
    domega_dt=k/J*np.cos(phi)-F/J
    return [dphi_dt, dpsi_dt, domega_dt]

# Initial conditions
initial_state=[0.1, 0.0, 0.0]  # Initial values for phi, psi, omega
# Time points where the solution is computed
time_points=np.linspace(0, 10, 1000)
# Parameters
m=1.0  # mass
n=1.0  # parameter n
g=9.81  # gravitational acceleration
b=0.1  # damping coefficient
k=0.5  # parameter k
F=0.2  # external force
J=0.05  # moment of inertia

# Solve the ODEs
solution=odeint(function, initial_state, time_points, args=(m, n, g, b, k, F, J))

# Extract the results
phi_values=solution[:, 0]
psi_values=solution[:, 1]
omega_values=solution[:, 2]

# Plot the results in 3D
ax.plot(phi_values, psi_values, omega_values)
ax.set_xlabel('Phi')
ax.set_ylabel('Psi')
ax.set_zlabel('Omega')
plt.show()
