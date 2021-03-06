import networkx as nx
import random

from divid.Girvan_Newman import GN #引用模块中的函数

#读取文件中边关系，然后成为一个成熟的图
def  ContractDict(dir,G):
    with open(dir, 'r') as f:
        for line in f:
            line1=line.strip().split(",")
            # print (line1)
            G.add_edge(int(float(line1[0])),int(float(line1[1])))
    # print (G.number_of_edges())
    return G


#生成感染图，我们看看感染图是什么样子。



from divid.queue import  Queue

def Algorithm1(G,basesore,sourceList):
    n = 0
    SG=nx.MultiGraph()
    simqueue = Queue()
    for i in range(len(sourceList)):
     simqueue.enqueue(sourceList[i])

    # while(not(simqueue.empty())):
    while (n<100 and simqueue.size()<98):
            print ("这次感染队列列表有个感染点")
            print (simqueue.size())
            sourceItem_=simqueue.dequeue()
            SG.add_node( sourceItem_)
            for sourceNeightor in list(G.neighbors( sourceItem_)):
                if G.node[sourceNeightor]['Cn']==0:
                    G.node[sourceNeightor]['Scn']+=G.nodes[ sourceItem_]['Scn']
                G.add_node(sourceNeightor, Cn=1)
                SG.add_node(sourceNeightor)
                SG.add_edge(sourceItem_,sourceNeightor)
                simqueue.enqueue(sourceNeightor)
            n+=1
    #对所有n<V(就是分数达到阕值的节点感染）算是谣言的不同之处吧。更新。
    for index in  range(1,35):
        if G.node[index]['Scn']>basesore:
            G.add_node(index, Cn=1)

    return  G,SG




#产生head以及tail中的一个随机数。
def  randomNum(head,tail):
    random.random()










#定义函数来进行分区后的谣言定位
'''
parameter：多个社区的分区，以及被传播的节点，现在分别计算度以及中心性，进行源头判断。

'''


def    cal_source(G,infectList):
    #按照分区的来进行判断源点。
    # print (len(infectList))
    # print('感染图，节点总数', G.number_of_nodes())
    # print('感染图，边总数', G.number_of_edges())
    # print('感染图，边总数', G.edges())
    lists = [[] for _ in range(len(infectList))]

    centrality = nx.betweenness_centrality(G)
    # print(sorted((v, '{:0.2f}'.format(c)) for v, c in centrality.items()))
    for v, c in centrality.items():
        for i in range(len(infectList)):
         if  v in infectList[i]:
             lists[i].append([v,c])

    #对lists进行排序。
    for i  in range(len(lists)):
       secList=sorted(lists[i],key=lambda x:(str(x[1]).lower(),x[0]),reverse = True )
       print (secList)
    # for i in range(len(lists)):
    #    print (lists[i])

























#  制造这个图
Ginti = nx.Graph()
#初始化图
for index in range(1,35):
    Ginti.add_node(index)


#构建图
G=ContractDict('karate_[Edges].csv',Ginti)


print ('一开始图的顶点个数',G.number_of_nodes())
print ('一开始图的边个数',G.number_of_edges())

'''
生成若干个感染节点。也就是谣言源点。每个节点有Cn以及Scn属性。
'''

#  先给全体的Cn、Scn的0的赋值。
for index in range(1,35):
    G.add_node(index, Cn=0,Scn=0)
# print (G.nodes[6416])



# 随机产生5个感染点。
sourceList=[]
for index in range(1,6):
    random_RumorSource=0
    random_RumorSource=random.randint(1, 34)
    sourceList.append(random_RumorSource)
    G.add_node(random_RumorSource,Cn=1)
print ('感染点列表',sourceList)





#  图形化还差得远。很烦。
#  开始送入我们的算法中，就G和basesore,还有感染源list三个参数，返回一个是所有图，以及传染图。
GResult,SGResult=Algorithm1(G,5,sourceList)





#打印出所传染的节点个数

Infected_node=[]
for i  in range(1,35):
    if  G.node[i]['Cn']== 1:
        Infected_node.append(i)
print ('感染点计数，以及他们',len(Infected_node),Infected_node)





nx.write_gml(SGResult,'test.gml')


#copy防止引用
import copy

SGResult_copy=copy.deepcopy(SGResult)

print ('感染图，节点总数',SGResult.number_of_nodes())
print  ('感染图，边总数',SGResult.number_of_edges())
print  ('感染图，点显示',SGResult.nodes())
print  ('感染图，边总数',SGResult.edges())



#将感染图构建边文件test.csv以及节点文件test1.csv

import csv

#python2可以用file替代open
with open("test.csv","w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    cout=1
    writer.writerow(["source","target","type"])
    for  u,v  in SGResult.edges():
        cout+=1
        writer.writerow([u,v,"Directed"])


#python2可以用file替代open
with open("test1.csv","w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id","label"])
    for  u  in SGResult.nodes():
        if u in sourceList:
           writer.writerow([u,'1'])
        else:
            writer.writerow([u,'0'])









#  将感染图，进行GN分区。

# algorithm = GN(GInfection)
algorithm = GN(SGResult)
partition, all_Q, max_Q=algorithm.run()
#暂时不需要画图
# algorithm.draw_Q()
algorithm.add_group()
algorithm.to_gml()





# 现在已经知道被感染的节点，那么问题来了，如何在被感染的分区之后的一些节点中找到
#源?

#prepare   parameter：准备参数，也就是我们的。

#计算分区结果，并且打印出中心度最高的节点。判断是不是源点。
cal_source(SGResult_copy,partition)

