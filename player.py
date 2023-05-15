# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:51:44 2022

@author: School
"""
import matplotlib.animation as animation
import mpl_toolkits.axes_grid1
import matplotlib.widgets
import numpy as np

import system
import constants as cnst

class Player(animation.FuncAnimation):
    def __init__(self, fig, func, frames = None, init_func = None, fargs = None,
                 save_count = None, mini = 0, maxi = 500, pos = (0.125, 0.92), system = None, axs = None,
                 *, cache_frame_data = True, **kwargs):
        self.i = 0
        self.min = mini
        self.max = maxi
        self.runs = True
        self.forwards = True
        
        self.system = system
        self.ax = axs
        
        self.fig = fig
        self.func = func
        self.setup(pos)
        super().__init__(self.fig, self.func, frames = self.play(), init_func = init_func,
                         fargs = fargs, save_count = save_count, **kwargs)
        
    def play(self):
        while self.runs:
            self.i = self.i + self.forwards - (not self.forwards)
            if self.i == 23:
                self.func = self.update_func(lambda x, t: x + t)
            if self.i > self.min and self.i < self.max:
                yield self.i
            else:
                self.stop()
                yield self.i
            
    def update_func(self, f):
        xs = np.linspace(0, self.system.a, 1000)
        line, = self.ax.plot([], [], 'r-', lw = 3)
        time_template = 'Time: %.1f s'
        time_text = self.ax.text(0.01, 0.85, '', transform = self.ax.transAxes)

        def func(i):
            xs = np.linspace(0, self.system.a, 1000)
            t = cnst.DT * i
            psis = [abs(f(x, t))**2 for x in xs]
            
            line.set_data(xs, psis)
            time_text.set_text(time_template % (i * cnst.DT))
            return line, time_text
        
        return func
    
    def start(self):
        self.runs = True
        self.event_source.start()
        
    def stop(self, event = None): 
        self.runs = False
        self.event_source.stop()
        
    def forward(self, event = None):
        self.forwards = True
        self.start()
    def backward(self, event = None):
        self.forwards = False
        self.start()
    def oneforward(self, event = None):
        self.forwards = True
        self.onestep()
    def onebackward(self, event = None):
        self.forwards = False
        self.onestep()
        
    def onestep(self):
        if self.i > self.min and self.i < self.max:
            self.i = self.i + self.forwards - (not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i += 1
        elif self.i == self.max and not self.forwards:
            self.i -= 1
        self.func(self.i)
        self.fig.canvas.draw_idle()
        
    def setup(self, pos):
        button_ax = self.fig.add_axes([pos[0], pos[1], 0.22, 0.04])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(button_ax)
        bax = divider.append_axes("right", size = "80%", pad = 0.05)
        sax = divider.append_axes("right", size = "80%", pad = 0.05)
        fax = divider.append_axes("right", size = "80%", pad = 0.05)
        ofax = divider.append_axes("right", size = "100%", pad = 0.05)
        self.button_oneback = matplotlib.widgets.Button(button_ax, label = u'\u29CF')
        self.button_back = matplotlib.widgets.Button(bax, label = u'\u25C0')
        self.button_stop = matplotlib.widgets.Button(sax, label = u'\u25A0')
        self.button_forward = matplotlib.widgets.Button(fax, label=u'\u25B6')
        self.button_oneforward = matplotlib.widgets.Button(ofax, label=u'\u29D0')
        self.button_oneback.on_clicked(self.onebackward)
        self.button_back.on_clicked(self.backward)
        self.button_stop.on_clicked(self.stop)
        self.button_forward.on_clicked(self.forward)
        self.button_oneforward.on_clicked(self.oneforward)