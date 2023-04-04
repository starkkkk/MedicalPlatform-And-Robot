# Medical Platform And Robot
该项目是基于socket编程的医疗交流平台，并在其中加入了基于知识图谱的医疗领域问答机器人。

首先搭建服务端与客户端实现医患私聊群聊，之后搭建医疗知识图谱，并基于此实现客户端与问答系统的互动。


# 项目效果 #
以下两张图是系统实际运行效果：
![系统运行效果图](https://github.com/zhihao-chen/QASystemOnMedicalGraph/blob/master/img/%E6%95%88%E6%9E%9C%E5%9B%BE.png)

# 项目环境
运行环境：Python3
编译执行：anaconda spyder
前端：Tkinter
后端：Python3 socket编程
数据库：neo4j

# 项目运行方式
由于将Robot函数绑定到Platform进行socket通信时，响应时间长达几分钟，原因未知，因此暂时把两个系统分开运行是最快捷的办法

## Medical Platform

1. 运行时先运行server.py，再分别运行client.py即可
2. 点击左侧在线用户列表中的用户或群聊，可分别进行私聊群聊。

## Robot
1. 首先根据自己neo4j账户密码修改相关设置，之后预训练词向量：这里可以直接从网盘上下载训练好的词向量链接: https://pan.baidu.com/s/1ghn3wv7X3ciVnONtD8WVzg 提取码: uv5x

2. 搭建知识图谱：python build_grapy.py。大概需要3个小时

3. 启动问答测试：python kbqa_test.py


# 项目代码
由于代码较多，不详细介绍，只说明各模块功能：
## Medical Platform
由于采用tkinter写前端，因此前端与socket网络编程写到一个文件内，集成为client和server两个py文件，其余几个文件夹分别存储文件、表情、图片

实现比较简单
## Robot
model：采用tfidf进行信息检索与数据挖掘

data：里面存储从39健康网下载下来的以疾病为中心的病例，有excel形式以及txt形式

build_graph：读取data中的文件，创建相关节点，建立知识图谱

entity_extractor：基于特征词分类的方法来识别用户查询意图

kbqa_test：创建robot实例，输出回答

search_answer：将问题转变为cypher查询语句以及根据意图返回查询结果


### 医疗知识图谱

![知识图谱结构](https://github.com/starkkkk/MedicalPlatform-And-Robot/blob/master/img1/tp.png)

![实际知识图谱展示](https://github.com/starkkkk/MedicalPlatform-And-Robot/blob/master/img1/neo4j.png)

# 总结

本项目实现难度不高，但训练时间较长，socket编程不做赘述，知识图谱是面前比较火热的方向，还是比较值得花费时间来实现，做完收获一定不少。

这次项目的实现也是对中国疫情防治贡献一点自己的力量，响应中央对于远程医疗系统开发的号召，武汉加油！


## 未来改进
加入嵌入式设备来录入病人身体状况(如体温)，方便医生更准确的问诊

爬取其它的健康网站数据以不断扩充知识图谱；增加可以识别的意图类别。

可以将问诊机器人得出的结果发送给需要的在线医生，作为在线问诊的参考

本文参考：https://github.com/zhihao-chen/QASystemOnMedicalKG

欢迎与我讨论：zhengjiaxing@sjtu.edu.cn
