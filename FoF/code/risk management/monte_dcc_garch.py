#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:33:00 2020

@author: Roy
"""
import numpy as np
import pandas as pd
import scipy

def monte_dcc_garch(n, alpha_dcc, beta_dcc, sigma_init, rho_init, alpha_grach, 
                    beta_garch, omega_garch, theta_garch, p, weight, mc_round = 10000):
    
    sigma2_garch = np.dot(np.diag(sigma_init), np.ones([2,mc_round])) # sigma dimension  2 assets in the portfolio
    
    np.random.seed(4)
    
    var = pd.DataFrame(index = range(n))
    var['ndays'] = np.arange(1, n + 1)
    var['VaR'] = 0
    var['rho'] = 0
    var.loc[0,'rho'] = rho_init # maybe change to gamma init
    
    # recore portfilio simulation return
    data_r_simulation = pd.DataFrame(index = range(mc_round))
    
    # simulation asset individual in portfolio standard log return
    z = np.random.normal(0,1,size = (2,mc_round)) # 2 assets in the portfolio
    gamma_sqrt = scipy.linalg.sqrtm(gmma_init) # sqrt of correlation matrix gamma

    # correlation series
    z = np.dot(gamma_sqrt,z)

    # real return = standard_return * volatility
    r = np.multiply(np.sqrt(sigma2_garch),z)
    
    # portfolio return
    portfilio_return = r * weight
    data_r_simulation['R_day1'] = portfilio_return

    if n == 1: #'''n days forward''''
        r_ndays = data_r_simulation.iloc[:,:2].sum(axis = 1)
        var.loc[0,'VaR'] = -np.percentile(r_ndays, p)
        
        return var
    
    # n days forward VaR through DCC and GARCH update parameters
    alpha_garch = np.dot(np.diag(alpha_grach), np.ones([2,mc_round]))
    beta_garch = np.dot(np.diag(beta_garch),np.ones([2,mc_round]))
    omega_garch = np.dot(np.diag(omega_garch),np.ones([2,mc_round]))
    theta_garch = np.dot(np.diag(theta_garch),np.ones([2,mc_round]))
    
    # volatility update - GARCH
    sigma2_garch = omega_garch + np.multiply(alpha_garch,(r - np.multiply(theta_garch,np.sqrt(sigma2_garch))))**2 + np.multiply(beta_garch,sigma2_garch)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

