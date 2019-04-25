#coding=utf-8
'''
Created on 2017年7月31日

@author: cuiyufei

@description: 逻辑回归模型
'''
import pandas as pd
from sklearn.linear_model import RandomizedLogisticRegression as RLR
from sklearn.linear_model import LogisticRegression as LR
from sklearn.decomposition import PCA



# filename = '../data/5/bankloan.xls'
# data = pd.read_excel(filename)
# x = data.iloc[:,:8].as_matrix()
# y = data.iloc[:,8].as_matrix()

filename = '../data/5/profile.xls'
data = pd.read_excel(filename)
data = data[data['AGE'].notnull()]
x = data.iloc[:,1:6].as_matrix()
y = data.iloc[:,-1].as_matrix()

# rlr = RLR()
# rlr.fit(x, y)
# rlr.get_support()
# print u'训练结束,训练的结果为'
# print u'有效特征为:%s' %','.join(data.columns[rlr.get_support()])
# x = data[data.columns[rlr.get_support()]].as_matrix()
 
lr = LR()
lr.fit(x, y)

print u'模型的平均正确率为：%s' %lr.score(x, y)
# pca = PCA()
# pca.fit(x)
# pca.components_
# print pca.explained_variance_ratio_