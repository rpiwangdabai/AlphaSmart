#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:31:03 2020

@author: Roy
"""
import numpy as np
import pandas as pd 

def getVaR_Monte(n,alpha_DCC,beta_DCC,sigma_first,rho_first,alpha_garch,beta_garch,omega_garch,theta_garch,p):
    MC = 10000
    sigma2_Garch = np.dot(np.diag(sigma_first),np.ones([2,MC]))

    np.random.seed(4)   

    VaR = pd.DataFrame(index = range(n))
    VaR['ndays'] = np.arange(1,n+1)
    VaR['VaR'] = 0   
    VaR['rho'] = 0
    VaR.loc[0,'rho'] = rho_first


    # 记录组合的模拟收益
    data_R = pd.DataFrame(index = range(MC))

    # 模拟组合中各资产的标准化收益率
    z = np.random.normal(0,1,size = (2,MC))
    gamma_half = np.array([[1,0],[VaR.loc[0,'rho'],(1-VaR.loc[0,'rho']**2)**0.5]])
    # 转换为指定相关系数的序列
    z = np.dot(gamma_half,z)

    # 各资产的真实收益率 = 标准化收益率*波动率
    r = np.multiply(sigma2_Garch**0.5,z)

    # 两资产等权重，总收益率
    data_R['R_day1'] =  np.mean(r,axis = 0)

    if n==1:

        R_ndays = data_R.iloc[:,:2].sum(axis = 1)
        VaR.loc[0,'VaR'] = - np.percentile(R_ndays,p) 
        return VaR

    # 若计算向前多天的VaR,通过DCC,GARCH模型更新参数

    alpha_garch = np.dot(np.diag(alpha_garch),np.ones([2,MC]))
    beta_garch = np.dot(np.diag(beta_garch),np.ones([2,MC]))
    omega_garch = np.dot(np.diag(omega_garch),np.ones([2,MC]))
    theta_garch = np.dot(np.diag(theta_garch),np.ones([2,MC]))    
    # 波动率更新 - Garch模型
    sigma2_Garch = omega_garch + np.multiply(alpha_garch,(r - np.multiply(theta_garch,sigma2_Garch**0.5)))**2 + np.multiply(beta_garch,sigma2_Garch)

    # 相关系数更新 - DCC模型
    q11 = pd.DataFrame(index = range(MC))
    q12 = pd.DataFrame(index = range(MC))
    q22 = pd.DataFrame(index = range(MC))
    q11['day1'] = 1 + alpha_DCC*((z[0,]**2)-1)  
    q12['day1'] = VaR.loc[0,'rho'] + alpha_DCC*(z[0,]*z[1,]- VaR.loc[0,'rho']) + beta_DCC*(VaR.loc[0,'rho'] - VaR.loc[0,'rho'])
    q22['day1']= 1 + alpha_DCC*((z[1,]**2)-1)

    VaR.loc[1,'rho'] = np.mean(q12['day1']/((q11['day1']*q22['day1'])**0.5))
    # gamma更新
    gamma_half = np.array([[1,0],[VaR.loc[1,'rho'],(1-VaR.loc[1,'rho']**2)**0.5]])


    for i in range(2,n):
        # 生成不相关的随机序列，并转换为指定相关系数的随机数
        z = np.random.normal(0,1,size = (2,MC))
        z = np.dot(gamma_half,z)
        r = np.multiply(sigma2_Garch**0.5,z)
        data_R['R_day' + str(i)] =  np.mean(r,axis = 0)        

        sigma2_Garch = omega_garch + np.multiply(alpha_garch,(r - np.multiply(theta_garch,sigma2_Garch**0.5)))**2 + np.multiply(beta_garch,sigma2_Garch)


        q11['day'+str(i)] = 1 + alpha_DCC*((z[0,]**2)-1) + beta_DCC*(q11['day'+str(i-1)]-1)
        q12['day'+str(i)] = VaR.loc[0,'rho'] + alpha_DCC*(z[0,]*z[1,]- VaR.loc[0,'rho'])+beta_DCC*(q12['day' + str(i-1)] - VaR.loc[0,'rho'])
        q22['day'+str(i)] = 1 + alpha_DCC*((z[1,]**2)-1) + beta_DCC*(q22['day'+str(i-1)]-1)

        VaR.loc[i,'rho'] = np.mean(q12['day'+str(i)]/((q11['day'+str(i)]*q22['day'+str(i)])**0.5))
        gamma_half = np.array([[1,0],[VaR.loc[i,'rho'],(1-VaR.loc[i,'rho']**2)**0.5]])

    for i in range(n):
        R_ndays = data_R.iloc[:,:i+1].sum(axis = 1)
        VaR.loc[i,'VaR'] = - np.percentile(R_ndays,p)                

    return(VaR)