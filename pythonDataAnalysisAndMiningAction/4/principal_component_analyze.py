#coding=utf-8
'''
Created on 2017年7月31日

@author: cuiyufei

@description: 主成分分析降维方法
'''
import pandas as pd
from sklearn.decomposition import PCA

inputfile = '../data/4/principal_component.xls'
outputfile = '../data/tmp/principal_component.xls'

data = pd.read_excel(inputfile)

#pca = PCA(n_components=4,copy=True, whiten=True)
pca = PCA()
pca.fit(data)
print pca.components_#返回模型的特征向量
print '=========================================='
print pca.explained_variance_ratio_#返回各个成分各自的方差百分比

pca = PCA(3)
pca.fit(data)
low_d = pca.transform(data)

pd.DataFrame(low_d).to_excel(outputfile)
da = pca.inverse_transform(low_d)
