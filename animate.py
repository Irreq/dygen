import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import numpy as np
import matplotlib.pyplot as plt

prandtl = 10
rho = 28
beta = 8/3

def lorenz_attr(x, y, z):
    x_dot = prandtl*(y - x)
    y_dot = rho*x - y - x*z
    z_dot = x*y - beta*z
    return x_dot, y_dot, z_dot
dt = 0.01
num_steps = 10000

style.use('fivethirtyeight')

fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
ax = fig.gca(projection='3d')
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")

# xs = np.empty(num_steps + 1)
# ys = np.empty(num_steps + 1)
# zs = np.empty(num_steps + 1)
xs = [0.]
ys = [1.]
zs = [1.05]
def animate(1):
    xs, ys, zs = f
    # print(i)
    # x_dot, y_dot, z_dot = lorenz_attr(xs[i], ys[i], zs[i])
    # xs.append(xs[i] + (x_dot * dt))
    # ys.append(ys[i] + (y_dot * dt))
    # zs.append(zs[i] + (z_dot * dt))
    ax.clear()
    ax.plot(xs, ys, zs, lw=0.5)


# # xdata, ydata = [], []
# my_line = ax.plot([], [], [])
#
# # And in your update function, just update this Line2D object.
#
# def animate(i):
#     x_dot, y_dot, z_dot = lorenz_attr(xs[i], ys[i], zs[i])
#     xs.append(xs[i] + (x_dot * dt))
#     ys.append(ys[i] + (y_dot * dt))
#     zs.append(zs[i] + (z_dot * dt))
#     my_line.set_data(xs, ys, zs)


ani = animation.FuncAnimation(fig, animate, (xs, ys, zs), interval=1)
plt.show()
