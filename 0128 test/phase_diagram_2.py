import pylab
x,y = pylab.meshgrid(pylab.arange(-2,2,0.01),pylab.arange(-2,2,0.01))
dx_dt = y-x*(x**2+y**2-1)
dy_dt = -x-y*(x**2+y**2-1)
pylab.streamplot(x,y,dx_dt,dy_dt)
pylab.show()