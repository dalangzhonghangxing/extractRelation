# 思路
1. 直接统计每个知识点A对应的百度词条，在其它知识点B中出现的个数，并且给LemmaSummary与mainContent不同的权重，从而得到一个分数。然后给定超参数alpha，如果大于alpha，则说明A是B的前驱。
2. 计算得分的时候，去除以文本长度，考虑频率与relation的关系。
3. 为了避免统计到错误的出现次数，首先对文本进行分词，在统计出现次数或者频率。
4. 考虑到很多知识点其实是同一类（例如“角的概念”与“角的计算”），可以先对知识点做一层抽象，然后在抽象上面找关系。因为“角的概念”与“角的计算”的前驱跟后继肯定是一样的。
5. 由于将第三方知识点映射到百度词条，那考虑是否可以在百度词条上面找关系，从而推断出第三方知识点的关系。
6. 将这个问题转换为分类问题，两两之间生成概念对，然后判断它们的关系。
7. 使用RefD的方法来找关系
8. 用章节名称+内容作为数据，用LDA训练得到topic（固定topic的数量）的概率分布作为特征，然后用逻辑回归分类。（监督）

# 结果分析
1. 方案1的结果很差，环路很多，无关关系很多。
2. 方案2的结果相对改善，但由于没有分词，结果还是很差，无关的关系很多。
3. 方案3的结果要好于方案1与方案2，但是score的阈值不好控制。
4. 实现了方案7，zeta取值为0.025能取得一个比较好的结果，大概找到198条关系
5. 同学用神经网络+w2v跑了个结果，结果不好，可能原因是1、语料质量不好；2、语料太少；3、w2v体现了两个概念在整个概念空间的维度相似性，但是这种关系是偏序关系，直接用来预测关系比较难。