# -*- coding: utf--*-
"""
Created on Sat Sep 24 04:19:56 2022

@author: School
"""

import constants as cnst
import system
import player

import numpy as np
import matplotlib.pyplot as plt


m, a = 1.0, 5.0
inf_well = system.InfiniteWell(a, m)

# Set up the figure and the axes
fig = plt.figure(figsize = (10, 10))
fig.canvas.manager.set_window_title('The TISE')
ax = fig.add_subplot(autoscale_on = False, xlim = (0, a), ylim = (0, 1.5))
ax.set_title("Particle in an Infinite Square Well")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$|\psi(x)|^2$")
#ax.set_aspect('equal')
ax.grid()

# Set up the plot objects
xs = np.linspace(0, a, 1000)
line, = ax.plot([], [], 'r-', lw = 3)
time_template = 'Time: %.1f s'
time_text = ax.text(0.01, 0.85, '', transform = ax.transAxes)

f = inf_well.create_initial_state(4)
def animate(i):       
    t = cnst.DT * i
    psis = [abs(f(x, t))**2 for x in xs]
    
    line.set_data(xs, psis)
    time_text.set_text(time_template % (i * cnst.DT))
    return line, time_text

ani = player.Player(
    fig, animate, frames = 1000, interval = 1, system = inf_well, axs = ax, blit = True)
plt.show()