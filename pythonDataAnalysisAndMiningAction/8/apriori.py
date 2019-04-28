#!/usr/bin/env python
# coding=utf-8
#######################################################################
#       > File Name: apriori.py
#       > Author: cyf
#       > Mail: XXX@qq.com
#       > Created Time: Tue 23 Apr 2019 06:00:18 AM UTC
#######################################################################

import time
import sys
import pandas as pd
from sklearn.cluster import KMeans
reload(sys)
sys.setdefaultencoding( "utf-8" )
"""
数据预处理
1.数据清洗
2.属性规约
    去除不相关的属性
3.数据变换：
属性构造
    症型系数=该症型得分/该症型总分
数据离散化
    由于Apriori关联规则算法无法处理连续型数值变量，为了将原始数据格式转换为适合建模的格式，需要对数据进行离散化。
    此处采用聚类算法进行离散化处理
discretization-->进行聚类离散化
apriori_rules-->定义关联规则
connect_string-->字符串连接
"""

def discretization(data, typelabel):
    """discretization（聚类离散化）
        Args:
            data 数据
            typelabel 需要聚类列及对应的标签
        Returns:
            result 聚类后的data
    """
    k = 4
    #result = pd.DataFrame()
    
    for key, item in typelabel.items():
        print(u"正在进行%s的聚类..." % key)
        # 进行聚类离散化
        kmodel = KMeans(n_clusters=k, n_jobs=4)
        kmodel.fit(data[[key]].values)

        # 聚类中心
        #r1 = pd.DataFrame(kmodel.cluster_centers_, columns=[item])
        # 分类统计
        #r2 = pd.Series(kmodel.labels_).value_counts()
        #r2 = pd.DataFrame(r2, columns=[item + '_nums'])
        # 合并为一个DataFrame
        #r = pd.concat([r1, r2], axis=1).sort_values(item)

        #r.index = list(range(1, 5))
        # 用来计算相邻两列的均值，以此作为边界点
        #r[item] = pd.Series.rolling(r[item], 2).mean()
        # 将NaN值转为0.0，不用fillna的原因是数值类型是float64
        #r.loc[1, item] = 0.0
        #result = result.append(r.T)
        
        # 将分类标签写入原始数据
        labels = [item+str(l+1) for l in kmodel.labels_]
        data[key] = pd.Series(labels, index=data.index)
    # 以ABCDEF排序
    print "离散化完成."
    #result = result.sort_index()
    #result.to_excel(processedfile)
    #data[typelabel.keys() + [u'TNM分期']].to_csv('../data/8/apriori.csv', index=False)
    return data[typelabel.keys() + [u'TNM分期']]

def apriori_rules(data, support, confidence, ms=u"->"):
    """find_rules（寻找关联规则函数）
        Args:
            data read_csv 数据
            support 支持度
            confidence 置信度
            ms 连接符号
        Returns:
            result 关联规则
    """
    # 自定义连接函数
    def connect_string(x, ms):
        x = list(map(lambda i: sorted(i.split(ms)), x))
        r = []
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                if x[i][:-1] == x[j][:-1] and x[i][-1] != x[j][-1]:
                    r.append(x[i][:-1] + sorted([x[j][-1], x[i][-1]]))
        return r
    # 计时
    start = time.clock()
    print(u"\n转换原始数据至0-1矩阵...")
    # 0-1矩阵的转换
    ct = lambda x: pd.Series(1, index=x[pd.notnull(x)])
    b = list(map(ct, data.as_matrix()))
    data = pd.DataFrame(b).fillna(0)
    end = time.clock()
    print(u"\n转换完毕，用时：%0.2f s" % (end - start))
    # 删除中间变量b，节省内存
    del b
    
    result = pd.DataFrame(index=["support", "confidence"])
    result = pd.DataFrame(index=["support", "confidence"])

    # 第一批支持度筛选
    support_series = 1.0 * data.sum() / len(data)

    column = list(support_series[support_series > support].index)
    k = 0

    while len(column) > 1:
        k = k + 1
        print(u"\n正在进行第%s次搜索..." % k)

        column = connect_string(column, ms)
        print(u"数目%s..." % len(column))
        index_lst = [ms.join(i) for i in column]

        # 新的支持度函数
        sf = lambda i: data[i].prod(axis=1, numeric_only=True)
        # 计算连接后的支持度，开始筛选
        d_2 = pd.DataFrame(list(map(sf, column)), index=index_lst).T
        support_series_2 = 1.0 * d_2[index_lst].sum() / len(data)
        column = list(support_series_2[support_series_2 > support].index)

        support_series = support_series.append(support_series_2)
        column2 = []
        # 遍历所有可能的情况
        for i in column:
            i = i.split(ms)
            for j in range(len(i)):
                column2.append(i[:j] + i[j + 1:] + i[j:j + 1])

        # 置信度序列
        cofidence_series = pd.Series(index=[ms.join(i) for i in column2])

        for i in column2:
            cofidence_series[ms.join(i)] = support_series[ms.join(
                sorted(i))] / support_series[ms.join(i[:-1])]
        # 置信度筛选
        for i in cofidence_series[cofidence_series > confidence].index:
            result[i] = 0.0
            result[i]["confidence"] = cofidence_series[i]
            result[i]["support"] = support_series[ms.join(sorted(i.split(ms)))]

    result = result.T.sort_values(["confidence", "support"], ascending=False)
    print(u"\nresult:")
    print(result)

    return result


def main():
    datafile_d = "../data/8/data.xls"
    data_d = pd.read_excel(datafile_d)
    typelabel = {
        u"肝气郁结证型系数": "A",
        u"热毒蕴结证型系数": "B",
        u"冲任失调证型系数": "C",
        u"气血两虚证型系数": "D",
        u"脾胃虚弱证型系数": "E",
        u"肝肾阴虚证型系数": "F",
    }
    data = discretization(data_d, typelabel)
    # 定义支持度，置信度，连接符号
    support = 0.06
    confidence = 0.75
    ms = "-->"
    # 计时
    start = time.clock()
    print(u"\n开始搜索关联规则...")
    apriori_rules(data, support, confidence, ms)
    end = time.clock()
    print(u"\n搜索完成，用时%0.2f s" % (end - start))


if __name__ == "__main__":
    main()
