#coding=utf-8
'''
Created on 2017年7月31日

@author: cuiyufei

@description: 小波变化的特征提
'''
inputfile = '../data/4/leleccum.mat'

from scipy.io import loadmat
mat = loadmat(inputfile)
signal = mat['leleccum'][0]

import pywt
coeffs = pywt.wavedec(signal, 'bior3.7', level=5)
print coeffs
