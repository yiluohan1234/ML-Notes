#coding=utf-8
'''
Created on 2017年8月4日

@author: cuiyufei

@description: 利用kmeans对航空公司客户价值进行分析
'''
import pandas as pd
from sklearn.cluster import KMeans
import os

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']#用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False#用来正常显示负号
import numpy as np
from radar_chart import radar_factory


def data_explore(path):
    '''
    #数据的初步探索
    '''   
    data = pd.read_csv(path)
    
    #数据的基本统计，并进行转置处理
    explore_data = data.describe(percentiles=[], include='all').T
    explore_data['null'] = len(data) - explore_data['count']
    output_data = explore_data[['max', 'min', 'null']]
    output_data.columns = [u'最大值', u'最小值', u'空值数']
    
    print output_data
    return output_data

def data_clean(path):
    '''
    #根据数据探索的结果，对数据进行处理
    '''   
    data = pd.read_csv(path,encoding='utf-8')
    
    #保留票价非空值
    data = data[(data['SUM_YR_1'].notnull())&(data['SUM_YR_2'].notnull())]
    
    #保留票价非0，或平均折扣率与总飞行公里数同时为0的记录
    index1 = data['SUM_YR_1'] != 0
    index2 = data['SUM_YR_2'] != 0
    index3 = (data['SEG_KM_SUM'] == 0)&(data['avg_discount'] == 0)
    
    data = data[index1|index2|index3]
    
    return data

def decrease_data(data):
    '''
    #根据建模分析，对数据进行降维
    #只留下FF_DATE、LOAD_TIME、FLIGHT_COUNT、AVG_DISCOUNT、SEG_KM_SUM、LAST_TO_END
    ''' 
    #取出与模型相关的属性，FF_DATE、LOAD_TIME、FLIGHT_COUNT、AVG_DISCOUNT、SEG_KM_SUM、LAST_TO_END   
    #L=LOAD_TIME-FFP_DATE
    data['L'] = (pd.to_datetime(data['LOAD_TIME']) - pd.to_datetime(data['FFP_DATE'])).astype('timedelta64[M]')
    data = data[['L', 'LAST_TO_END', 'FLIGHT_COUNT', 'SEG_KM_SUM', 'avg_discount']]
    data.columns = ['L', 'R', 'F', 'M', 'C']
    
    return data
    
def zscore_data(data):
    '''
    #对数据进行标准化
    '''
    #标准化处理
    data = (data - data.mean(axis = 0))/(data.std(axis=0))
    data.columns = ['Z'+i for i in data.columns]
    
    return data

def kmeans_cluster(data):    
    k = 5   
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
    #r = pd.concat([data, pd.Series(kmodel.labels_, index=data.index)], axis=1 )
    #r.columns = list(data.columns) + [u'聚类类别']
    #print r
    ret = pd.DataFrame(kmodel.cluster_centers_)
    ret.columns = list(data.columns)

    return ret
def plot_model(data):
    N = 5
    #初始化
    theta = radar_factory(N, frame='polygon')
 
    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
 
    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate axes
    #['L', 'R', 'F', 'M', 'C']('ZL', 'ZC', 'ZM', 'ZF', 'ZR')
    
    spoke_labels = ('ZL', 'ZC', 'ZM', 'ZF', 'ZR')
    ax = fig.add_subplot(111, projection='radar')
    plt.rgrids([0.1, 0.5, 1, 1.5, 2.0, 2.5])
    ax.set_title(u'客户群分析', weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(data, colors):
        ax.plot(theta, d, color=color)
        ax.fill(theta, d, facecolor=color, alpha=0.25)
    ax.set_varlabels(spoke_labels)
 
    labels = ('1', '2', '3', '4', '5')
    legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
    plt.setp(legend.get_texts(), fontsize='small')
    plt.show()
if __name__ == '__main__':
    inputfile = '../data/7/air_data.csv'
    #data_explore(inputfile)
    data_cleaned = data_clean(inputfile)
    data_decreased = decrease_data(data_cleaned)
    zscore_data = zscore_data(data_decreased)
    r2 = kmeans_cluster(zscore_data)
    data = np.array(r2)
    plot_model(data)
