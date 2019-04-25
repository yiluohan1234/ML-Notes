#coding=utf-8
'''
Created on 2017年8月1日

@author: cuiyufei

@description: tsne提供了一种有效数据降维的方式
'''
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
plt.rcParams['font.sans-serif'] = ['SimHei']#用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False#用来正常显示负号

inputfile = '../data/5/consumption_data.xls'
outputfile = '../data/tmp/data_type.xls'

k = 3#聚类类别
iteration = 500#聚类最大迭代次数
data = pd.read_excel(inputfile,index_col='Id')
data_zs = 1.0*(data - data.mean())/data.std()#数据标准化

model = KMeans(n_clusters=k, n_jobs=1, max_iter=iteration)
model.fit(data_zs)

r1 = pd.Series(model.labels_).value_counts()
r2 = pd.DataFrame(model.cluster_centers_)
r = pd.concat([r2, r1], axis=1)
print data.columns
r.columns = list(data.columns)+[u'类别数目']
print r

r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1 )
r.columns = list(data.columns) + [u'聚类类别']
r.to_excel(outputfile)

tsne = TSNE()
tsne.fit_transform(data_zs)
tsne = pd.DataFrame(tsne.embedding_, index = data_zs.index)

d = tsne[r[u'聚类类别'] == 0]
plt.plot(d[0], d[1], 'r.')
d = tsne[r[u'聚类类别'] == 1]
plt.plot(d[0], d[1], 'go')
d = tsne[r[u'聚类类别'] == 2]
plt.plot(d[0], d[1], 'b*')
plt.show()