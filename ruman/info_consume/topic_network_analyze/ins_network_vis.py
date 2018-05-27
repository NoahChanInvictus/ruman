#-*-coding: utf-8-*-
"""
windows 上安装说明：
1. 安装pygraphviz
访问http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz下载cp27 win_amd64.whl，然后用管理员权限cmd进入下载路径，pip install 这个文件名

2. 安装graphviz
访问http://www.graphviz.org/Download_windows.php，下载graphviz-2.38.msi，双击安装，完了之后把Program_files中graphviz-2.38下的bin路径下到系统的环境变量PATH中

3. 安装matplotlib
访问http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib，下载cp27 win_amd64.whl，然后用管理员权限cmd进入下载路径，pip install 这个文件名

4. 安装networkx
pip install networkx
"""


import re
from pylab import *
import networkx as nx
from networkx.generators.atlas import *
import matplotlib.pyplot as plt
import random

mpl.rcParams[u'font.sans-serif'] = ['YouYuan'] # Microsoft YaHei,FangSong,YouYuan,SimHei,STKaiti,STSong,SimSun-ExtB,Webdings 

ins_posfix = set()
with open("ins_dict.txt") as f:
    for line in f:
        ins_posfix.add(line.strip().decode("utf-8"))


def is_nt(text):
    """text: unicode
    """
    def check(text):
        isins = False
        for i in range(0, 4):
            length = 4 - i
            if text[-length:] in ins_posfix and u":" not in text:
                isins = True
                break
        return isins

    isins = check(text)
    
    if not isins:
        isins = check(text.split(u"（")[0])

    return isins

def add_local_neighbor(center, lis, G):
    G.add_node(center)
    G.add_nodes_from(lis)
    for i in lis:
        G.add_edge(center, i)

    return G

def find_friends(nodes, G):
    result = set()
    for node in nodes:
        result.add(node)
        if node in G:
            for nd in G[node]:
                result.add(nd)

    return result

def dict2graph(targetins_list, insdict, hops=1):
    G=nx.Graph()

    for ins, rs in insdict.iteritems():
        # if ins in targetins_list:
        G = add_local_neighbor(ins, rs, G)
        
        """
        if len(list(set(rs) & set(targetins_list))) > 0:
            G = add_local_neighbor(ins, rs, G)
        """

    local_nodes = set(targetins_list)
    for hop in range(0, hops):
        local_nodes = local_nodes | find_friends(local_nodes, G)

    local_G = G.subgraph(list(local_nodes))


    # cities = {0:"Toronto",1:"London",2:"Berlin",3:"New York"}
    # H=nx.relabel_nodes(G,cities)

    #nx.draw(G)
    #plt.savefig("simple_path.png") # save as png
    #plt.show() # display

    print("graph has %d nodes with %d edges"\
          %(nx.number_of_nodes(local_G), nx.number_of_edges(local_G)))

    try:
        import pygraphviz
        from networkx.drawing.nx_agraph import graphviz_layout
    except ImportError:
        try:
            import pydotplus
            from networkx.drawing.nx_pydot import graphviz_layout
        except ImportError:
            raise ImportError("This example needs Graphviz and either "
                              "PyGraphviz or PyDotPlus")

    plt.figure(1, figsize=(18, 9))
    draw_graphviz = True
    try:
        # layout graphs with positions using graphviz neato, twopi, fdp
        pos = graphviz_layout(local_G, prog="twopi")
    except:
        draw_graphviz = False
    # color nodes the same in each connected subgraph
    C = nx.connected_component_subgraphs(local_G)
    for g in C:
        c = [random.random()] * nx.number_of_nodes(g) # random color...
        if draw_graphviz:
            nx.draw(g,
             pos,
             node_size=40,
             node_color=c,
             vmin=0.0,
             vmax=1.0,
             with_labels=True
             )
        else:
            nx.draw(g,
                node_size=40,
                node_color=c,
                vmin=0.0,
                vmax=1.0,
                with_labels=True)
    plt.savefig("demo.png", dpi=75)
    plt.show()

if __name__ == '__main__':
    ins_pattern = re.compile(r'\[\[(\S+?)\]\]')
    f = open("ins2ins.txt")
    ins = ""
    ins2ins_dict = dict()
    for line in f:
        inss = re.findall(ins_pattern, line.strip())
        if len(inss) and "*" not in line:
            ins = inss[0].decode("utf-8")
            ins2ins_dict[ins] = []
        else:
            _ins = line.strip().split("：")[0].replace("*", "").strip().split("（")[0].decode("utf-8")
            """
            if len(_ins) < 30 and is_nt_v2(_ins.encode("utf-8")):
                ins2ins_dict[ins].append(_ins)
            """
            if is_nt(_ins):
                ins2ins_dict[ins].append(_ins)
            
            
    f.close()

    ins_list = [u"中华人民共和国国家发展和改革委员会", u"国家发改委"] # 
    total_hops = 2
    dict2graph(ins_list, ins2ins_dict, hops=total_hops)
