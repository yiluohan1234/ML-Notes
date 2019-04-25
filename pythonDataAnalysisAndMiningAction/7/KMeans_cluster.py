#coding=utf-8
'''
Created on 2017年8月4日

@author: cuiyufei

@description: 利用kmeans进行分类
'''
import pandas as pd
from sklearn.cluster import KMeans
import os
import matplotlib.pyplot as plt


def kmeans_cluster():
    inputfile = '../data/tmp/zscoreddata.xls'
    k = 5
    #读取数据
    data = pd.read_excel(inputfile)
    
    #调用kmeans算法，训练模型  
    kmodel = KMeans(n_clusters=k, n_jobs=1)
    kmodel.fit(data)
    
    #print kmodel.cluster_centers_
    #print kmodel.labels_
    
    #画出类别中心和数量
    r1 = pd.Series(kmodel.labels_).value_counts()
    r2 = pd.DataFrame(kmodel.cluster_centers_)
    r = pd.concat([r2, r1], axis=1)
    r.columns = list(data.columns)+[u'类别数目']
    print r
    
    #类别加入到原数据
    r = pd.concat([data, pd.Series(kmodel.labels_, index=data.index)], axis=1 )
    r.columns = list(data.columns) + [u'聚类类别']
    print r

if __name__ == '__main__':
    kmeans_cluster()
