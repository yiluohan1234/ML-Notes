#coding=utf-8
'''
Created on 2017年8月4日

@author: cuiyufei

@description: 数据探索
'''
import os
import pandas as pd
def data_explore():   
    inputfile = '../data/7/air_data.csv'
    resultfile = '../data/tmp/explore.xls'
    data = pd.read_csv(inputfile)
    
    #数据的基本统计，并进行转置处理
    explore_data = data.describe(percentiles=[], include='all').T
    explore_data['null'] = len(data) - explore_data['count']
    output_data = explore_data[['max', 'min', 'null']]
    output_data.columns = [u'最大值', u'最小值', u'空值数']
    output_data.to_excel(resultfile)
    print u"数据导出成功! 位置：%s" % os.getcwd()
if __name__=='__main__':
    data_explore()
