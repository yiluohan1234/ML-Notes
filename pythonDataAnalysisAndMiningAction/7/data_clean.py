#coding=utf-8
'''
Created on 2017年8月4日

@author: cuiyufei

@description: 数据清洗
'''
import pandas as pd

def data_clean():
    inputfile = '../data/7/air_data.csv'
    cleanfile = '../data/tmp/data_cleaned.xls'
    
    data = pd.read_csv(inputfile,encoding='utf-8')
    
    #保留票价非空值
    data = data[(data['SUM_YR_1'].notnull())&(data['SUM_YR_2'].notnull())]
    
    #保留票价非0，或平均折扣率与总飞行公里数同时为0的记录
    index1 = data['SUM_YR_1'] != 0
    index2 = data['SUM_YR_2'] != 0
    index3 = (data['SEG_KM_SUM'] == 0)&(data['avg_discount'] == 0)
    
    data = data[index1|index2|index3]
    
    data.to_excel(cleanfile)
    print u'数据清理成功！'
def decrease_data():
    inputfile = '../data/tmp/data_cleaned.xls'
    data = pd.read_excel(inputfile,encoding='utf-8')
    modelfile = '../data/tmp/data_model.xls'
    
    #取出与模型相关的属性，FF_DATE、LOAD_TIME、FLIGHT_COUNT、AVG_DISCOUNT、SEG_KM_SUM、LAST_TO_END
    data_model = data[['LOAD_TIME', 'FFP_DATE', 'FLIGHT_COUNT', 'avg_discount', 'SEG_KM_SUM', 'LAST_TO_END']]
    data['L'] = (pd.to_datetime(data['LOAD_TIME']) - pd.to_datetime(data['FFP_DATE'])).astype('timedelta64[M]')
    data = data[['L', 'LAST_TO_END', 'FLIGHT_COUNT', 'SEG_KM_SUM', 'avg_discount']]
    data.columns = ['L', 'R', 'F', 'M', 'C']
    data.to_excel(modelfile,index=False)

    print u'数据精简成功！'
    
if __name__=='__main__':
    decrease_data()
