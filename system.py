# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 07:04:21 2022

@author: School
"""
import constants as cnst

import numpy as np
import random

class InfiniteWell:
    def __init__(self, a, m):
        self.a = a
        self.m = m
        
        self.coeffs = None
    
    def position_factor(self, n):
        return lambda x: (2 / self.a)**(1/2) * np.sin(n * np.pi * x / self.a)
    
    def time_factor(self, n):
        E = self.energy(n)
        return lambda t: np.exp(-1j * E * t / cnst.hbar)
    
    def stationary_state(self, n):
        return lambda x, t: self.position_factor(n)(x) * self.time_factor(n)(t)
    
    def energy(self, n):
        return n**2 * np.pi**2 * cnst.hbar**2 / (2 * self.m * self.a**2)
    
    def create_initial_state(self, num, coeffs = None):
        if coeffs == None:
            self.coeffs = [(1 / num)**(1/2) for _ in range(num)]
        else: 
            if sum([coeff ** 2 for coeff in self.coeffs]) != 1:
                raise RuntimeError("Initial state must be normalizable")
            else:
                self.coeffs = coeffs
                
        return lambda x, t: sum([self.coeffs[n] * self.stationary_state(n + 1)(x, t) for n in range(num)])
        
    
    def measure_energy(self):
        if self.coeffs == None: raise RuntimeError("Can't measure the energy for a nonexistent state")
        probs = [coeff ** 2 for coeff in self.coeffs]
        ns = [i for i in range(1, len(probs) + 1)]
        
        n_choice = random.choices(ns, probs)[0]
        new_psi = self.stationary_state(n_choice)
        E = self.energy(n_choice)
        print(f"The measured energy is E = {E} (associated quantum number n = {n_choice}).")
        return new_psi
    
    def measure_position(self):
        if self.coeffs == None: raise RuntimeError("Can't measure the position for a nonexistent state")
    
    def measure_momentum(self):
        if self.coeffs == None: raise RuntimeError("Can't measure the momentum for a nonexistent state")