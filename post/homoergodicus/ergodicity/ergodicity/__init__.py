"""
   :copyright: (c) 2020 by Gustavo Landfried
   :license: BSD, see LICENSE for more details.
"""
import os
import math
import numpy as np
from numpy.random import normal as rnorm
from matplotlib import pyplot as plt 


__all__ = ["dW","wiener"]


def change_in_utility(w):
    """
    w = np.array(list(map(lambda x: 10.0**x,np.arange(-10,10))) )
    change_in_utility(w)
    """
    return 1/w

def utility(w):
    return np.log(w)

def show_utility(w):
    """
    w = np.arange(-10,10,step=0.1) 
    show_utility(w)
    np.log(10**-10)
    """
    plt.plot(w,(utility(w)))
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    plt.ylabel("Utility", fontsize=16 )
    plt.xlabel("Wealth", fontsize=16 )


def dW(pos=0,step=1):
    return rnorm(pos,step,1)[0]

def wiener(iterations,step_length):
    """
    Norbert Wiener process:
        A real valued continuous time stochastic process 
        of the one-dimensional Brownian motion.
    """
    res = [0]
    for i in range(iterations):
        pos = res[-1]
        res.append(dW(pos,step_length))
    return res

def show_walks(n,iteratons=100,step_length=1):
    """
    Examples
    ---------
    show_walks(10)
    show_walks(10,1000,0.01) # See changes on scale
    """
    
    for i in range(n):
        plt.plot(wiener(iteratons,step_length))
        
def simple_gamble(x):
    r = np.random.random()
    if r <= 0.5:
        res = 1.5*x
    else:
        res = 0.6*x
    return res

def walk_simple_gamble(iteratons):
    res = [1]
    for i in range(iteratons):
        res.append(simple_gamble(res[-1]))
    return res
    
def incest_rule(communities_size,incest=0.05):
    res = []
    migration_per_community = (incest*sum(communities_size))/len(communities_size)
    for c in range(len(communities_size)):
        res.append(communities_size[c]*(1-incest) + migration_per_community)
    return res 

def init_communities(n_communities):
    communities = []
    for i in range(n_communities):
        communities.append(1.0)
    return communities

def walk_incest(iteratons,n_communities,incest=1):     
    communities = init_communities(n_communities)
    history = []
    history.append(communities)
    for i in range(iteratons):
        history.append(list(map(lambda x: simple_gamble(x), incest_rule(history[-1],incest) ) ))
    return history
 
def walk_sharing(iteratons=1000,n_communities=150):
    communities = init_communities(n_communities)
    history = []
    history.append(communities)
    for i in range(iteratons):
        proportion = list(map(lambda x: x/n_communities, history[-1] ))
        shared = sum(history[-1])
        shared = simple_gamble(shared) # El problema es jugar en grupo. Ley de los grandes n\'umeros.
        history.append(list(map(lambda x: shared*x, proportion)))
    return history
    

def multiplicative_process(n,rate,dt):
    wealth = [1]
    time = [0]
    for i in range(n):
        wealth.append(wealth[-1]*rate)
        time.append(time[-1]+dt)
    return time, wealth

def show_mult(n=120,rate=1.01,dt=1/12):
    """
    show_mult(12,1.04,dt=1)
    show_mult(12*12,1.01,dt=1/12)
    """
    x, y = multiplicative_process(n,rate,dt)
    plt.plot(x,np.log10(y))
    
def gr_mult(rate,dt):
    """
    Constant growth rate in a multiplicative process
    
    Examples
    --------
    gr_mult(1.125,1)
    gr_mult(1.01,1/12)
    """
    return np.log(rate)/dt

"""
To perturb the process in a consistent way, we remind ourselves
that what's constant about the process in the absence of noise is the
growth rate
"""

def perturbed_payment(rate=1.01,dt=1/12,sigma=0.1):
    """
    perturbed_payment(1.125,1,1)
    """
    gamma = np.log(rate)/dt
    dv = gamma*dt + sigma*dW(0,dt)
    return dv

def walk_perturbed_payment(n,rate,dt,sigma=100):
    """
    walk_perturbed_payment(1000,1.01,1/12,100)
    """
    wealth = [1]
    for i in range(n):
        dv = perturbed_payment(rate,dt,sigma)
        wealth.append(wealth[-1]+wealth[-1]*dv)
    return wealth
        
def show_walk_perturbed_payment(n=10,iterations=1000,rate=1.005,dt=1/12,sigma=100):
    """
    show_walk_perturbed_payment(n=10,sigma=2)
    show_walk_perturbed_payment(n=1,sigma=0)
    """
    for i in range(n):
        plt.plot(np.log10(walk_perturbed_payment(iterations,rate,dt,sigma)) )
        
        
