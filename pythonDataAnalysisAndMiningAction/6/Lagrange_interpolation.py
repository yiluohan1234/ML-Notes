#coding=utf-8
'''
Created on 2017年8月2日

@author: cuiyufei

@description: 
'''
import pandas as pd
from scipy.interpolate import lagrange
from random import shuffle
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from sklearn.metrics import confusion_matrix 
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.tree import DecisionTreeClassifier 

def ployinterp_column(s, n, k=5):
    '''
    #s为列向量，n为被插值的位置，k为前后的数据个数
    '''
    y = s[list(range(n-k, n)) + list(range(n+1, n+1+k))]
    y = y[y.notnull()]
    return lagrange(y.index, list(y))(n)

def interpolate_and_save():
    infile = '../data/6/missing_data.xls'
    outfile = '../data/tmp/missing_data_proccessed.xls'
    
    data = pd.read_excel(infile, header=None)

    for i in data.columns:
        for j in range(len(data)):
            if (data[i].isnull())[j]:
                data[i][j] = ployinterp_column(data[i], j)
                print data[i].index
    data.to_excel(outfile, header=None, index=None)

# def train_with_LM():
#     datafile = '../data/6/model.xls'
#     data = pd.read_excel(datafile)
#     data = data.as_matrix()#转换为矩阵
#     
#     shuffle(data)
#     
#     #划分测试集和训练集
#     p = 0.8 #设置训练数据比例
#     train = data[:int(len(data)*p),:]
#     test = data[int(len(data)*p):,:]
#     
#     netfile = '../data/tmp/net.model'
#     
#     net = Sequential() #建立神经网络
#     net.add(Dense(input_dim = 3, units = 10)) #添加输入层（3节点）到隐藏层（10节点）的连接
#     net.add(Activation('relu')) #隐藏层使用relu激活函数
#     net.add(Dense(input_dim = 10, units = 1)) #添加隐藏层（10节点）到输出层（1节点）的连接
#     net.add(Activation('sigmoid')) #输出层使用sigmoid激活函数
#     net.compile(loss = 'binary_crossentropy', optimizer = 'adam', sample_weight_mode = "binary") #编译模型，使用adam方法求解
#     
#     net.fit(train[:,:3], train[:,3], epochs=1000, batch_size=1) #训练模型，循环1000次
#     net.save_weights(netfile) #保存模型
#     
#     
#     
#     predict_result = net.predict_classes(train[:,:3]).reshape(len(train)) #预测结果变形
#     '''这里要提醒的是，keras用predict给出预测概率，predict_classes才是给出预测类别，而且两者的预测结果都是n x 1维数组，而不是通常的 1 x n'''
#     
#     cm = confusion_matrix(train[:,3], predict_result) #混淆矩阵
#        
#     plt.matshow(cm, cmap=plt.cm.Greens) #画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
#     plt.colorbar() #颜色标签
#     
#     for x in range(len(cm)): #数据标签
#       for y in range(len(cm)):
#         plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
#     
#     plt.ylabel('True label') #坐标轴标签
#     plt.xlabel('Predicted label') #坐标轴标签
#     plt.show() #显示作图结果
#     
#     
#     
#     predict_result = net.predict(test[:,:3]).reshape(len(test))
#     fpr, tpr, thresholds = roc_curve(test[:,3], predict_result, pos_label=1)
#     plt.plot(fpr, tpr, linewidth=2, label = 'ROC of LM') #作出ROC曲线
#     plt.xlabel('False Positive Rate') #坐标轴标签
#     plt.ylabel('True Positive Rate') #坐标轴标签
#     plt.ylim(0,1.05) #边界范围
#     plt.xlim(0,1.05) #边界范围
#     plt.legend(loc=4) #图例
#     plt.show() #显示作图结果
#     
# # def train_with_DT():  
#     '''
#     #决策树
#     '''
#     datafile = '../data/6/model.xls' #数据名
#     treefile = '../data/tmp/tree.pkl' #模型输出名字
#     data = pd.read_excel(datafile) #读取数据，数据的前三列是特征，第四列是标签
#     data = data.as_matrix() #将表格转换为矩阵
#     shuffle(data) #随机打乱数据
#     
#     p = 0.8 #设置训练数据比例
#     train = data[:int(len(data)*p),:] #前80%为训练集
#     test = data[int(len(data)*p):,:] #后20%为测试集
#     
#     
#     tree = DecisionTreeClassifier() #建立决策树模型
#     tree.fit(train[:,:3],train[:,3]) #训练
#     #保存模型
#     from sklearn.externals import joblib
#     joblib.dump(tree, treefile) 
#     
#     cm = confusion_matrix(train[:,3], tree.predict(train[:,:3])) #混淆矩阵
#     
#     plt.matshow(cm, cmap=plt.cm.Greens) #画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
#     plt.colorbar() #颜色标签
#     
#     for x in range(len(cm)): #数据标签
#       for y in range(len(cm)):
#         plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
#     
#     plt.ylabel('True label') #坐标轴标签
#     plt.xlabel('Predicted label') #坐标轴标签
#     plt.show() #显示作图结果
#     
#     #导入ROC曲线函数
#     fpr, tpr, thresholds = roc_curve(test[:,3], tree.predict_proba(test[:,:3])[:,1], pos_label=1)
#     plt.plot(fpr, tpr, linewidth=2, label = 'ROC of CART', color = 'green') #作出ROC曲线
#     plt.xlabel('False Positive Rate') #坐标轴标签
#     plt.ylabel('True Positive Rate') #坐标轴标签
#     plt.ylim(0,1.05) #边界范围
#     plt.xlim(0,1.05) #边界范围
#     plt.legend(loc=4) #图例
#     plt.show() #显示作图结果
# train_with_LM()
# train_with_DT()
interpolate_and_save()