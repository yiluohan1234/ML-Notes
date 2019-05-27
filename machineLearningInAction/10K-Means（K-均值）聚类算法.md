

# 第 10 章 K-Means（K-均值）聚类算法

## 一、概述

### 1.1.聚类的定义

聚类就是对大量未知标注的数据集，按照数据的内在相似性将数据集划分为多个类别，使类别内的数据相似度较大而类别间的相似度较小。

聚类算法的重点就是计算数据间的相似度。

### 1.2.相似度衡量方法

#### 1.2.1.闵可夫斯基距离（Minkowski）

![dist(X,Y) = \sqrt[p]{\sum_{i=1}^{n}|x_{i}-y_{i}|^{p}}](https://latex.codecogs.com/png.latex?dist%28X%2CY%29%20%3D%20%5Csqrt%5Bp%5D%7B%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%7Cx_%7Bi%7D-y_%7Bi%7D%7C%5E%7Bp%7D%7D)

当p=1时，为曼哈顿距离（Manhattan）

![dist(X,Y)=\sum_{i=1}^{n}|x_{i}-y_{i}|](https://latex.codecogs.com/png.latex?dist%28X%2CY%29%3D%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%7Cx_%7Bi%7D-y_%7Bi%7D%7C)

当p=2时，为欧式距离（Euclidean）

![dist(X,Y) = \sqrt{\sum_{i=1}^{n}(x_{i}-y_{i})^{2}}](https://latex.codecogs.com/png.latex?dist%28X%2CY%29%20%3D%20%5Csqrt%7B%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%28x_%7Bi%7D-y_%7Bi%7D%29%5E%7B2%7D%7D)

当p为无穷大时，为切比雪夫距离（Chebyshev）

![dist(X,Y) = max_{i}(|x_{i}-y_{i}|)](https://latex.codecogs.com/png.latex?dist%28X%2CY%29%20%3D%20max_%7Bi%7D%28%7Cx_%7Bi%7D-y_%7Bi%7D%7C%29)

#### 1.2.2.杰卡德相似系数（Jaccard ）

![J(A,B) = \frac{|A\bigcap B|}{|A\bigcup B|}](https://latex.codecogs.com/png.latex?J%28A%2CB%29%20%3D%20%5Cfrac%7B%7CA%5Cbigcap%20B%7C%7D%7B%7CA%5Cbigcup%20B%7C%7D)

杰卡德距离

![dist(A,B) =1-J(A,B)= \frac{|A\bigcup B|-|A\bigcap B|}{|A\bigcup B|}](https://latex.codecogs.com/png.latex?dist%28A%2CB%29%20%3D1-J%28A%2CB%29%3D%20%5Cfrac%7B%7CA%5Cbigcup%20B%7C-%7CA%5Cbigcap%20B%7C%7D%7B%7CA%5Cbigcup%20B%7C%7D)

杰卡德距离用于描述集合之间的不相似度，距离越大，相似度越低。

主要用于比较文本的相似度，用于文本的查重与去重；计算对象间距离，用于数据聚类。

#### 1.2.3.夹角余弦相似度

![cos(\theta )=\frac{a^{T}b}{|a||b|}](https://latex.codecogs.com/png.latex?cos%28%5Ctheta%20%29%3D%5Cfrac%7Ba%5E%7BT%7Db%7D%7B%7Ca%7C%7Cb%7C%7D)

文档的相似度

#### 1.2.4.Pearson相关系数

![\sigma _{xy}=\frac{Cov(X,Y)}{\sqrt{D(X)\sqrt{D(Y)}}}=\frac{E[(X-E(X))(Y-E(Y))]}{\sqrt{D(X)\sqrt{D(Y)}}}=\frac{\sum_{i=0}^{n}(X_{i}-u_{x})(Y_{i}-u_{y})}{\sqrt{\sum_{i=1}^{n}(X_{i}-u_{x})^{2}\sqrt{\sum_{i=1}^{n}(Y_{i}-u_{y})^{2}}}}](https://latex.codecogs.com/png.latex?%5Csigma%20_%7Bxy%7D%3D%5Cfrac%7BCov%28X%2CY%29%7D%7B%5Csqrt%7BD%28X%29%5Csqrt%7BD%28Y%29%7D%7D%7D%3D%5Cfrac%7BE%5B%28X-E%28X%29%29%28Y-E%28Y%29%29%5D%7D%7B%5Csqrt%7BD%28X%29%5Csqrt%7BD%28Y%29%7D%7D%7D%3D%5Cfrac%7B%5Csum_%7Bi%3D0%7D%5E%7Bn%7D%28X_%7Bi%7D-u_%7Bx%7D%29%28Y_%7Bi%7D-u_%7By%7D%29%7D%7B%5Csqrt%7B%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%28X_%7Bi%7D-u_%7Bx%7D%29%5E%7B2%7D%5Csqrt%7B%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%28Y_%7Bi%7D-u_%7By%7D%29%5E%7B2%7D%7D%7D%7D)

![dist(X,Y) =1 - \sigma _{xy}](https://latex.codecogs.com/png.latex?dist%28X%2CY%29%20%3D1%20-%20%5Csigma%20_%7Bxy%7D)

皮尔逊相关系数即将x，y坐标向量各自平移到原点后的夹角余弦。

文档间求距离使用夹角余弦：夹角余弦表征了文档去均值化后的随机向量间的相关系数

#### 1.2.5.KL距离（相对熵）

![D(X||Y)=\sum_{x}P(X)log\frac{P(X)}{P(Y)}](https://latex.codecogs.com/png.latex?D%28X%7C%7CY%29%3D%5Csum_%7Bx%7DP%28X%29log%5Cfrac%7BP%28X%29%7D%7BP%28Y%29%7D)

#### 1.2.6.Hellinger距离

![D_{a}(p||q)=\frac{2}{1-a^{2}}(1-\int p(x)^{\frac{1+a}{2}}q(x)^{\frac{1-a}{2}})dx)](https://latex.codecogs.com/png.latex?D_%7Ba%7D%28p%7C%7Cq%29%3D%5Cfrac%7B2%7D%7B1-a%5E%7B2%7D%7D%281-%5Cint%20p%28x%29%5E%7B%5Cfrac%7B1&plus;a%7D%7B2%7D%7Dq%28x%29%5E%7B%5Cfrac%7B1-a%7D%7B2%7D%7D%29dx%29)



### 1.3.聚类和分类算法的区别

聚类算法是无监督学习，数据是没有标注的。分类算法是监督学习，基于有标注的历史数据进行算法模型构建。

## 二、基本思想

### 2.1.k-means算法的基本原理

k-means算法中的k代表类簇个数，means代表类簇内数据对象的均值（这种均值是一种对类簇中心的描述），因此，k-means算法又称为k-均值算法。k-means算法是一种基于划分的聚类算法，以距离作为数据对象间相似性度量的标准，即数据对象间的距离越小，则它们的相似性越高，则它们越有可能在同一个类簇。数据对象间距离的计算有很多种，k-means算法通常采用欧氏距离来计算数据对象间的距离。

#### 2.1.1.k-means算法的描述如下

对于给定的类别数目k，首先给出初始划分，通过迭代改变样本和簇的隶属关系，使得每一次改进之后的划分方案都较前一次好。

给定一个有N个对象的数据集，构造数据的k个簇，k<=n。满足下列条件：

- 每一个簇至少包含一个对象
- 每一个对象属于且仅属于一个簇
- 将满足以上条件的k个簇称作一个合理划分

假定输入样本为

![S=x_{1},x_{2},...x_{m}](https://latex.codecogs.com/png.latex?S%3Dx_%7B1%7D%2Cx_%7B2%7D%2C...x_%7Bm%7D)

，则算法的步骤为：

- 选择初始的k个类别中心

  ![u_{1},u_{2},...u_{k}](https://latex.codecogs.com/png.latex?u_%7B1%7D%2Cu_%7B2%7D%2C...u_%7Bk%7D)

- 对于每个样本xi，将其标记为距离类别中心最近的类别，即：

  ![label_{i}=arg min_{1<=j<=k}||x_{i}-u_{k}||](https://latex.codecogs.com/png.latex?label_%7Bi%7D%3Darg%20min_%7B1%3C%3Dj%3C%3Dk%7D%7C%7Cx_%7Bi%7D-u_%7Bk%7D%7C%7C)

- 将每个类别中心更新为隶属该类别的所有样本的均值

  ![u_{j}=\frac{1}{|c_{j}|}\sum_{i\epsilon c_{j}}x_{i}](https://latex.codecogs.com/png.latex?u_%7Bj%7D%3D%5Cfrac%7B1%7D%7B%7Cc_%7Bj%7D%7C%7D%5Csum_%7Bi%5Cepsilon%20c_%7Bj%7D%7Dx_%7Bi%7D)

- 重复最后两步，直到类别中心的变化小于某阈值。

终止条件：

- 迭代次数/簇中心变化率/最小平方误差MSE(Minimum Squared Error)

#### 2.1.2.k-means算法的伪代码如下：

- 创建 k 个点作为起始质心（通常是随机选择）
- 当任意一个点的簇分配结果发生改变时（不改变时算法结束）
  - 对数据集中的每个数据点
    - 对每个质心
      - 计算质心与数据点之间的距离
    - 将数据点分配到距其最近的簇
  - 对每一个簇, 计算簇中所有点的均值并将均值作为质心

#### 2.1.3.K-Means 聚类算法代码

```
# k-means 聚类算法
# 该算法会创建k个质心，然后将每个点分配到最近的质心，再重新计算质心。
# 这个过程重复数次，知道数据点的簇分配结果不再改变位置。
# 运行结果（多次运行结果可能会不一样，可以试试，原因为随机质心的影响，但总的结果是对的， 因为数据足够相似，也可能会陷入局部最小值）
def kMeans(dataMat, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataMat)[0]  # 行数
    clusterAssment = mat(zeros(
        (m, 2)))  # 创建一个与 dataMat 行数一样，但是有两列的矩阵，用来保存簇分配结果
    centroids = createCent(dataMat, k)  # 创建质心，随机k个质心
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # 循环每一个数据点并分配到最近的质心中去
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :],
                                  dataMat[i, :])  # 计算数据点到质心的距离
                if distJI < minDist:  # 如果距离比 minDist（最小距离）还小，更新 minDist（最小距离）和最小质心的 index（索引）
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:  # 簇分配结果改变
                clusterChanged = True  # 簇改变
                clusterAssment[
                    i, :] = minIndex, minDist**2  # 更新簇分配结果为最小质心的 index（索引），minDist（最小距离）的平方
        print(centroids)
        for cent in range(k):  # 更新质心
            ptsInClust = dataMat[nonzero(
                clusterAssment[:, 0].A == cent)[0]]  # 获取该簇中的所有点
            centroids[cent, :] = mean(
                ptsInClust, axis=0)  # 将质心修改为簇中所有点的平均值，mean 就是求平均值的
    return centroids, clusterAssment
```

### 2.2.K-Means 聚类算法的缺陷

> 在 kMeans 的函数测试中，可能偶尔会陷入局部最小值（局部最优的结果，但不是全局最优的结果）.

局部最小值的的情况如下:

![](./pic/10kmeans.jpg)



出现这个问题有很多原因，可能是k值取的不合适，可能是距离函数不合适，可能是最初随机选取的质心靠的太近，也可能是数据本身分布的问题。

为了解决这个问题，我们可以对生成的簇进行后处理，一种方法是将具有最大**SSE**值的簇划分成两个簇。具体实现时可以将最大簇包含的点过滤出来并在这些点上运行K-均值算法，令k设为2。

为了保持簇总数不变，可以将某两个簇进行合并。从上图中很明显就可以看出，应该将上图下部两个出错的簇质心进行合并。那么问题来了，我们可以很容易对二维数据上的聚类进行可视化， 但是如果遇到40维的数据应该如何去做？

有两种可以量化的办法：合并最近的质心，或者合并两个使得**SSE**增幅最小的质心。 第一种思路通过计算所有质心之间的距离， 然后合并距离最近的两个点来实现。第二种方法需要合并两个簇然后计算总**SSE**值。必须在所有可能的两个簇上重复上述处理过程，直到找到合并最佳的两个簇为止。

因为上述后处理过程实在是有些繁琐，所以有更厉害的大佬提出了另一个称之为二分K-均值（bisecting K-Means）的算法.

#### 2.2.1.二分 K-Means 聚类算法

该算法首先将所有点作为一个簇，然后将该簇一分为二。
之后选择其中一个簇继续进行划分，选择哪一个簇进行划分取决于对其划分时候可以最大程度降低 SSE（平方和误差）的值。
上述基于 SSE 的划分过程不断重复，直到得到用户指定的簇数目为止。

#### 2.2.2.二分 K-Means 聚类算法伪代码

- 将所有点看成一个簇
- 当簇数目小于 k 时
- 对于每一个簇
  - 计算总误差
  - 在给定的簇上面进行 KMeans 聚类（k=2）
  - 计算将该簇一分为二之后的总误差
- 选择使得误差最小的那个簇进行划分操作

另一种做法是选择 SSE 最大的簇进行划分，直到簇数目达到用户指定的数目位置。 接下来主要介绍该做法的python2代码实现

#### 2.2.3二分 K-Means 聚类算法代码

```
# 二分 KMeans 聚类算法, 基于 kMeans 基础之上的优化，以避免陷入局部最小值
def biKMeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2))) # 保存每个数据点的簇分配结果和平方误差
    centroid0 = mean(dataSet, axis=0).tolist()[0] # 质心初始化为所有数据点的均值
    centList =[centroid0] # 初始化只有 1 个质心的 list
    for j in range(m): # 计算所有数据点到初始质心的距离平方误差
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k): # 当质心数量小于 k 时
        lowestSSE = inf
        for i in range(len(centList)): # 对每一个质心
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:] # 获取当前簇 i 下的所有数据点
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas) # 将当前簇 i 进行二分 kMeans 处理
            sseSplit = sum(splitClustAss[:,1]) # 将二分 kMeans 结果中的平方和的距离进行求和
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1]) # 将未参与二分 kMeans 分配结果中的平方和的距离进行求和
            print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE: # 总的（未拆分和已拆分）误差和越小，越相似，效果越优化，划分的结果更好（注意：这里的理解很重要，不明白的地方可以和我们一起讨论）
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        # 找出最好的簇分配结果    
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) # 调用二分 kMeans 的结果，默认簇是 0,1. 当然也可以改成其它的数字
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit # 更新为最佳质心
        print 'the bestCentToSplit is: ',bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClustAss)
        # 更新质心列表
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0] # 更新原质心 list 中的第 i 个质心为使用二分 kMeans 后 bestNewCents 的第一个质心
        centList.append(bestNewCents[1,:].tolist()[0]) # 添加 bestNewCents 的第二个质心
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss # 重新分配最好簇下的数据（质心）以及SSE
    return mat(centList), clusterAssment
```

### 2.3.K-Means 场景

kmeans，如前所述，用于数据集内种类属性不明晰，希望能够通过数据挖掘出或自动归类出有相似特点的对象的场景。其商业界的应用场景一般为挖掘出具有相似特点的潜在客户群体以便公司能够重点研究、对症下药。

例如，在2000年和2004年的美国总统大选中，候选人的得票数比较接近或者说非常接近。任一候选人得到的普选票数的最大百分比为50.7%而最小百分比为47.9% 如果1%的选民将手中的选票投向另外的候选人，那么选举结果就会截然不同。 实际上，如果妥善加以引导与吸引，少部分选民就会转换立场。尽管这类选举者占的比例较低，但当候选人的选票接近时，这些人的立场无疑会对选举结果产生非常大的影响。如何找出这类选民，以及如何在有限的预算下采取措施来吸引他们？ 答案就是聚类（Clustering)。

那么，具体如何实施呢？首先，收集用户的信息，可以同时收集用户满意或不满意的信息，这是因为任何对用户重要的内容都可能影响用户的投票结果。然后，将这些信息输入到某个聚类算法中。接着，对聚类结果中的每一个簇（最好选择最大簇 ）， 精心构造能够吸引该簇选民的消息。最后， 开展竞选活动并观察上述做法是否有效。

另一个例子就是产品部门的市场调研了。为了更好的了解自己的用户，产品部门可以采用聚类的方法得到不同特征的用户群体，然后针对不同的用户群体可以对症下药，为他们提供更加精准有效的服务。

### 2.4.k-means算法的优缺点

**优点**:

- 属于无监督学习，无须准备训练集
- 原理简单，实现起来较为容易
- 结果可解释性较好

**缺点**:

- **需手动设置k值**。 在算法开始预测之前，我们需要手动设置k值，即估计数据大概的类别个数，不合理的k值会使结果缺乏解释性
- 可能收敛到局部最小值, 在大规模数据集上收敛较慢
- 对于异常点、离群点敏感

## 附录

[余弦定理证明](https://baike.baidu.com/item/%E4%BD%99%E5%BC%A6%E5%AE%9A%E7%90%86/957460?fr=aladdin)

[欧几里得点积公式推到](https://baike.baidu.com/item/%E7%82%B9%E7%A7%AF/9648528?fr=aladdin)

[AiLearning之k-means聚类算法](https://github.com/apachecn/AiLearning/blob/master/docs/ml/10.k-means%E8%81%9A%E7%B1%BB.md)

[机器学习算法之K-means算法](https://baijiahao.baidu.com/s?id=1622412414004300046&wfr=spider&for=pc)
