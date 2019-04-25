# 第12章 使用FP-growth算法来高效发现频繁项集

## 一、背景

大家都用过搜索引擎。当我们输入一个单词或单词的一份，搜索引擎就会自动补全查询词项。例如：当我们在百度输入“为什么”时，会出现很多的推荐结果。为了给出这些推荐查词词项，公司的研究人员使用了本本章将要介绍的一个算法--FP-growth算法，高效发现频繁项集的方法。![](E:./pic/百度搜索.jpg)

FP-growth 算法优缺点:

```
优点： 1. 因为 FP-growth 算法只需要对数据集遍历两次，所以速度更快。
        2. FP树将集合按照支持度降序排序，不同路径如果有相同前缀路径共用存储空间，使得数据得到了压缩。
        3. 不需要生成候选集。
        4. 比Apriori更快。
缺点： 1. FP-Tree第二次遍历会存储很多中间过程的值，会占用很多内存。
        2. 构建FP-Tree是比较昂贵的。
适用数据类型：标称型数据(离散型数据)。
```

## 二、FP-growth 算法

在 [第11章](https://github.com/apachecn/AiLearning/blob/dev/blog/ml) 时我们已经介绍了用 `Apriori` 算法发现 `频繁项集` 与 `关联规则`。
本章将继续关注发现 `频繁项集` 这一任务，并使用 `FP-growth` 算法更有效的挖掘 `频繁项集`。

### 1.FP-growth 算法简介

- 一种非常好的发现频繁项集算法。
- 它基于Apriori算法构建，将数据集存储在叫做 `FP树` 的数据结构中。
- FP-growth只能高效地发现频繁项集，不能用于发现关联规则。

### 2.FP-growth 算法步骤

Fp-growth只需对数据进行两次扫描，因此比Apriori速度快

- 基于数据构建FP树

- 从FP树种挖掘频繁项集

### 3.FP树介绍

FP-growth算法将数据存储在FP树的结构中。FP代表频繁模式（Frequent Pattern）

一个元素项可以在FP树中出现多次，相同元素通过链接来连接起来

FP树的节点结构如下:

```
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue     # 节点名称
        self.count = numOccur     # 节点出现次数
        self.nodeLink = None      # 不同项集的相同项通过nodeLink连接在一起
        self.parent = parentNode  # 指向父节点
        self.children = {}        # 存储叶子节点
```

## 三、FP-growth的流程和原理

### 1.FP-growth的一般流程

```
1.收集数据:使用任意方法
2.准备数据：由于存储的集合，所以需要离散数据。如果要处理连续数据，需要将他们量化为离散值
3.分析数：使用任意方法
4.训练算法：构建一个FP树，并对树进行挖掘
5.测试算法：没有测试过程
6.使用算法：可用于识别经常出现的元素项，从而用于制定决策，推荐元素或进行预测等应用中
```

### 2.FP-growth 原理

#### 1）基于数据构建FP树

##### 步骤1:

1. 遍历所有的数据集合，计算所有项的支持度。
2. 丢弃非频繁的项。
3. 基于 支持度 降序排序所有的项。
4. 所有数据集合按照得到的顺序重新整理。
5. 重新整理完成后，丢弃每个集合末尾非频繁的项。 

![](./pic/11FP-growth1.jpg)

##### 步骤2: 

读取每个集合插入FP树中，同时用一个头部链表数据结构维护不同集合的相同项。

过程如下图所示：

![](./pic/11FP-growth2.jpg)

![](./pic/11FP-growth3.jpg)

![](./pic/11FP-growth4.jpg)

![](./pic/11FP-growth5.jpg)

![](./pic/11FP-growth6.jpg)

![](./pic/11FP-growth7.jpg)

![](./pic/11FP-growth8.jpg)

书本中关于r元素的链接是错的。

#### 2）从FP树中挖掘出频繁项集

##### 步骤1:从FP树中获得条件模式基

1. 对头部链表进行降序排序
2. 对头部链表节点从小到大遍历，得到条件模式基，同时获得一个频繁项集。 ![](./pic/11FP-growth9.jpg)

如上图，从头部链表 t 节点开始遍历，t 节点加入到频繁项集。找到以 t 节点为结尾的路径如下: 

![](./pic/11FP-growth10.jpg)

去掉FP树中的t节点，得到条件模式基<左边路径,左边是值>`[z,x,y,s,t]:2，[z,x,y,r,t]:1 `。条件模式基的值取决于末尾节点 t ，因为 t 的出现次数最小，一个频繁项集的支持度由支持度最小的项决定。所以 t 节点的条件模式基的值可以理解为对于以 t 节点为末尾的前缀路径出现次数。

##### 步骤2：利用条件模式基，构建一个条件子树

条件模式基继续构造条件 FP树， 得到频繁项集，和之前的频繁项组合起来，这是一个递归遍历头部链表生成FP树的过程，递归截止条件是生成的FP树的头部链表为空。 根据步骤 2 得到的条件模式基 [z,x,y,s,t]:2，[z,x,y,r,t]:1 作为数据集继续构造出一棵FP树，计算支持度，去除非频繁项，集合按照支持度降序排序，重复上面构造FP树的步骤。最后得到下面 t-条件FP树 : 

![](./pic/11FP-growth11.jpg)

##### 步骤3：迭代重复步骤（1）和（2），直到树包含一个元素为止

然后根据 t-条件FP树 的头部链表进行遍历，从 y 开始。得到频繁项集 ty 。然后又得到 y 的条件模式基，构造出 ty的条件FP树，即 ty-条件FP树。继续遍历ty-条件FP树的头部链表，得到频繁项集 tyx，然后又得到频繁项集 tyxz. 然后得到构造tyxz-条件FP树的头部链表是空的，终止遍历。我们得到的频繁项集有 t->ty->tyz->tyzx，这只是一小部分。

## 3.FP-growth 代码讲解

完整代码地址: <https://github.com/apachecn/AiLearning/blob/master/src/py2.x/ml/12.FrequentPattemTree/fpGrowth.py>

main 方法大致步骤:

```
if __name__ == "__main__":
    simpDat = loadSimpDat()                       #加载数据集。
    initSet = createInitSet(simpDat)              #对数据集进行整理，相同集合进行合并。
    myFPtree, myHeaderTab = createTree(initSet, 3)#创建FP树。
    freqItemList = []
    mineTree(myFPtree, myHeaderTab, 3, set([]), freqItemList) #递归的从FP树中挖掘出频繁项集。
    print freqItemList
```

大家看懂原理，再仔细跟踪一下代码。基本就没有问题了。

感谢[apachecn官网](http://www.apachecn.org/)。

## 参考

[apachecn的AILearning](https://github.com/apachecn/AiLearning)