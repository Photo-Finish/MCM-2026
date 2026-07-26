#Initialize
import numpy as np
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot

#Define the range of variables
x = np.linspace(-2, 2, 10)          
y = np.linspace(-2, 2, 10)          

#Create grid
x_mesh, y_mesh = np.meshgrid(x, y)  

#Differential equation
dx_dt = y_mesh-x_mesh*(x_mesh**2+y_mesh**2-1)
dy_dt = -x_mesh-y_mesh*(x_mesh**2+y_mesh**2-1)

plt.quiver(x_mesh,y_mesh,dx_dt,dy_dt)
plt.show()
