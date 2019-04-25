#coding=utf-8
'''
Created on 2017年8月1日

@author: cuiyufei

@description: k-means聚类分析
'''
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
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
def density_plot2(data, title):
    plt.figure()
    for i in range(len(data.iloc[0])):
        (data.iloc[:,i].plot(kind='kde', label=data.columns[i], linewidth=2))
    plt.ylabel(u'密度')
    plt.xlabel(u'人数')
    plt.title(u'聚类分别%s个属性的密度曲线' %title)
    plt.legend()
    return plt


def density_plot(data):
    p = data.plot(kind='kde', linewidth=2, subplots= True, sharex=False)
    [p[i].set_ylabel(u'密度') for i in range(k)]
    plt.legend()
    return plt
pic_output = '../data/tmp/pd_'
for i in range(k):
    density_plot(data[r[u'聚类类别'] == i]).savefig(u'%s%s.png' %(pic_output, i))
    