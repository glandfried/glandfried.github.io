# -*- coding: utf-8 -*-
"""
   Gaussian
   --------

   This module contains basic mathematics functions of Gaussian distribution

   :copyright: (c) 2020 by Gustavo Landfried
   :license: BSD, see LICENSE for more details.

"""

from __future__ import absolute_import
#from scipy.stats import norm
import numpy as np
#import copy
import math
try:
    from numbers import Number
except ImportError:
    Number = (int, float, complex)

#from six import iterkeys


__all__ = ['Gaussian', 'inf']


inf = float('inf')

class Gaussian(object):
    """A model for the normal distribution."""

    #: Precision, the inverse of the variance.
    pi = 0
    #: Precision adjusted mean, the precision multiplied by the mean.
    tau = 0

    def __init__(self, mu=None, sigma=None, pi=0, tau=0):
        
        if mu is not None:
            if isinstance(mu, Gaussian) and sigma is None:
                sigma = mu.sigma
                mu = mu.mu
            elif sigma is None:
                raise TypeError('sigma argument is needed')
            elif sigma <= 0:
                raise ValueError('sigma**2 should be greater than 0')
            
            if isinstance(mu, Gaussian):
                sigma = math.sqrt( mu.sigma ** 2 + sigma**2 )
                mu = mu.mu
            
            pi = sigma ** -2
            tau = pi * mu
            
        self.pi = pi
        self.tau = tau

    @property
    def mu(self):
        """A property which returns the mean."""
        return self.pi and self.tau / self.pi

    @property
    def sigma(self):
        """A property which returns the the square root of the variance."""
        return math.sqrt(1 / self.pi) if self.pi else inf



    @property
    def trunc(self):
        
        def v_win(t, draw_margin=0):
            #t = t - draw_margin
            return (self.pdf(t) / self.cdf(t))# if denom else -x
        
        def w_win(t, draw_margin=0):
            #t = t - draw_margin
            v = v_win(t, draw_margin)
            w = v * (v + t)
            return w
            
        #def v(t,alpha,beta):
        #    return ((norm.pdf(alpha-t)-norm.pdf(beta-t))/(norm.cdf(beta-t)-norm.cdf(alpha-t) ) )
    
        #def w(t,alpha,beta):
        #    return v_win(t,alpha,beta)**2 + ( ((beta-t)*norm.pdf(beta-t)-(alpha-t)*norm.pdf(alpha-t) ) / (norm.cdf(beta-t)-norm.cdf(alpha-t)) )
        
        def mu_trunc(mu_verdadera,sigma_verdadera):
            return mu_verdadera + sigma_verdadera*v_win(mu_verdadera/sigma_verdadera) 
        
        # V(X | a < X < b)
        def sigma_trunc(mu_verdadera,sigma_verdadera):
            return np.sqrt((sigma_verdadera**2) *(1-w_win(mu_verdadera/sigma_verdadera)))
        
        '''
        if ranks[x] == ranks[x + 1]:  # is a tie?
            v_func, w_func = self.v_draw, self.w_draw
        else:
            v_func, w_func = self.v_win, self.w_win
        '''
        
        return Gaussian(mu_trunc(*self) , sigma_trunc(*self))


    def erfc(self, x):
        """Complementary error function (via `http://bit.ly/zOLqbc`_)"""
        z = abs(x)
        t = 1. / (1. + z / 2.)
        r = t * math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (
            0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (
                0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (
                    -0.82215223 + t * 0.17087277
                )))
            )))
        )))
        return 2. - r if x < 0 else r
    
    def cdf(self, x, mu=0, sigma=1):
        """Cumulative distribution function"""
        return 0.5 * self.erfc(-(x - mu) / (sigma * math.sqrt(2)))

    def pdf(self, x, mu=0, sigma=1):
        """Probability density function"""
        return (1 / math.sqrt(2 * math.pi) * abs(sigma) *
            math.exp(-(((x - mu) / abs(sigma)) ** 2 / 2)))

    '''
    def cdf(self, x, mu=0, sigma=1):
        t = x-mu;
        y = 0.5*self.erfc(-t/(sigma*np.sqrt(2.0)));
        if y>1.0:
            y = 1.0;
        return y

    def pdf(self, x, mu=0, sigma=1):
        u = (x-mu)/abs(sigma)
        y = (1/(np.sqrt(2*np.pi)*abs(sigma)))*np.exp(-u*u/2)
        return y
    '''
    
    def modify(self, other):
        self.tau, self.pi = other.tau, other.pi
        
    def __add__(self, other):
        return Gaussian(self.mu+other.mu, math.sqrt(self.sigma**2 + other.sigma**2) )
    
    def __sub__(self, other):
        return Gaussian(self.mu-other.mu, math.sqrt(self.sigma**2 + other.sigma**2) )
    
    def __mul__(self, other):
        pi, tau = self.pi + other.pi, self.tau + other.tau
        return Gaussian(pi=pi, tau=tau)

    def __truediv__(self, other):
        pi, tau = self.pi - other.pi, self.tau - other.tau
        return Gaussian(pi=pi, tau=tau)

    __div__ = __truediv__  # for Python 2

    def __eq__(self, other):
        return self.pi == other.pi and self.tau == other.tau

         
    def __lt__(self, other):
        return self.mu < other.mu

    def __le__(self, other):
        return self.mu <= other.mu

    def __gt__(self, other):
        return self.mu > other.mu

    def __ge__(self, other):
        return self.mu >= other.mu

    def __int__(self):
        return int(self.mu)

    def __float__(self):
        return float(self.mu)

    def __iter__(self):
        return iter((self.mu, self.sigma))

    def __repr__(self):
        return 'N(mu={:.3f}, sigma={:.3f})'.format(self.mu, self.sigma)

    #def _repr_latex_(self):
    #    latex = r'\mathcal{{ N }}( {:.3f}, {:.3f}^2 )'.format(self.mu, self.sigma)
    #    return '$%s$' % latex

