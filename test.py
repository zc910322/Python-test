# -*- coding:UTF-8 -*-
'''
Created on 2016年11月21日
@author: Administrator
'''
import httplib2  
import xml.dom.minidom
import copy
import networkx as nx
import multhreading_new
from urllib import urlencode

class WIAPAnetwork(object):

    def __init__(self, deviceinfo, topology, panID, ipaddress = None):
        self.deviceinfo = deviceinfo
        self.topology = topology
        self.panID = panID
        self.graph = nx.DiGraph()
        self.pathlist = [] #路径列表
        self.routeIDlist = {} #{path:routeID,.....}
        self.ipaddress = ipaddress
        self.macaddress = None

    def get_panID(self):
        return self.panID
    def get_deviceinfo(self):
        return self.deviceinfo
    def get_topology(self):
        return self.topology
    def get_routeID(self, path):

        for key in self.pathlist:
            if isinstance(path, list) and path == key:
                return self.routeIDlist[tuple(key)]
            if isinstance(path, str) and path == key[0]:
                return self.routeIDlist[tuple(key)]

        return None

    def set_deviceinfo(self, deviceinfo):
        self.deviceinfo = deviceinfo
    def set_topology(self, topology):
        self.topology = topology

    def routeID_calculation(self, path):

        if(path[0] == "0001"):
            if(self.deviceinfo[path[-1]] == "2"):
                routeID_down = (((int(path[-1]) << 1) >> 8) - 1) << 8
                routeID_up = (int(path[-1]) << 1)
            if(self.deviceinfo[path[-1]] == "3"):
                routeID_down = (int(path[-1]) & 0xff00) | (((int(path[-1]) << 1) - 1) & 0x00ff)
                routeID_up = (int(path[-1]) & 0xff00) | ((int(path[-1]) << 1) & 0x00ff)
        else:
            print "路径起始地址错误！"

        self.routeIDlist[tuple(path)] = [routeID_up, routeID_down]

    def shortest_path_creat(self, target):

        for key in self.topology:
            self.graph.add_edge(key[0], key[1], weight=1)
        for key in self.deviceinfo:
            if self.deviceinfo[key] == "1":
                generator = nx.shortest_simple_paths(self.graph, source=key,
                                                     target=target, weight='weight')
                path = []
                k = 1
                try:
                    for path in generator:
                        if k <= 0:
                            break
                        k -= 1
                        print("PATH: %s" % path)
                        self.pathlist.append(path)
                        self.routeID_calculation(path)
                except:
                    print("No path between %s and %s" % (key, target))



# h = httplib2.Http(".cache")
# resp, content = h.request("http://127.0.0.1:12345/", "GET")
# print resp
# print content
deviceinfo = {}
topologyinfo = {}
schedulinginfo = {}
dom = xml.dom.minidom.parse("index.xml")
# collection = DOMTree.documentElement
# dom = xml.dom.minidom.parseString(content)
def analysis_topology(dom):

    deviceinfo = {}
    topologyinfo = []


    table  =  dom.getElementsByTagName( "topology" )[0]
    namelist  =  table.getElementsByTagName( "edge" )

    for name in namelist:
        categorylist = name.getElementsByTagName("category")
        addresslist = name.getElementsByTagName("address")
        for i in range(2):
            category = categorylist[i]
            textNode = category.childNodes[0].nodeValue.replace('\t','').replace('\n','').replace(' ','')
            address = addresslist[i]
            textNode1 = address.childNodes[0].nodeValue.replace('\t','').replace('\n','').replace(' ','')
            deviceinfo[textNode1] = textNode

    for tmp in namelist:
        edge = []
        src = tmp.getElementsByTagName("src")
        dst = tmp.getElementsByTagName("dst")

        srcaddr = src[0].getElementsByTagName("address")
        dstaddr = dst[0].getElementsByTagName("address")

        srcaddress = srcaddr[0].childNodes[0].nodeValue.replace('\t','').replace('\n','').replace(' ','')
        dstaddress = dstaddr[0].childNodes[0].nodeValue.replace('\t','').replace('\n','').replace(' ','')

        edge.append(srcaddress)
        edge.append(dstaddress)
        topologyinfo.append(edge)

    return deviceinfo, topologyinfo

deviceinfo, topologyinfo = analysis_topology(dom)
for key in deviceinfo:
    print(key, 'corresponds to', deviceinfo[key])
for key in topologyinfo:
    print(key[0], 'corresponds to', key[1])

network_1 = WIAPAnetwork(deviceinfo, topologyinfo, 1, '192.168.1.2')
network_1.macaddress = "01:02:03:04:05:06"
network_2 = WIAPAnetwork(deviceinfo, topologyinfo, 2, '192.168.1.3')
network_2.macaddress = "01:02:03:04:05:07"
network_1.shortest_path_creat('0004')
network_2.shortest_path_creat('0004')
print("routeID: %s" %network_1.routeIDlist)
schedulinginfo[(network_1.ipaddress, network_1.macaddress,tuple(network_1.get_routeID('0001')))]\
    = (network_2.ipaddress, network_2.macaddress,tuple(network_2.get_routeID('0001')))
for key in schedulinginfo:
    print(key, 'corresponds to', schedulinginfo[key])
def createMappingtable(info, src, dst):
    '''
    函数名：createMappingtable
输入参数：routeid对应信息
输出参数：列表
功能：生成映射表
映射表格式：[命令，映射表数量，[源地址，MAC地址，routeID，源短地址，目的短地址，目的地址，routeID，源短地址，目的短地址]，
[源地址，MAC地址，routeID，源短地址，目的短地址，目的地址，routeID，源短地址，目的短地址]......]
    '''
    mapping = []
    num = 0
    
    mapping.append("setmappingtable")
    mapping.append(num)
    
    for key in schedulinginfo:
        table = []
        table.append(key[0])
        table.append(key[1])
        table.append(key[2][0])
        
        for tmp in src.routeIDlist:
            if src.routeIDlist[tmp][0] == table[2]:
                table.append(tmp[0])
                table.append(tmp[-1])
                break
        else:
            return -1
        table.append(schedulinginfo[key][0])
        table.append(schedulinginfo[key][1])
        table.append(schedulinginfo[key][2][1])
        for tmp in dst.routeIDlist:
            if dst.routeIDlist[tmp][1] == table[7]:
                table.append(tmp[0])
                table.append(tmp[-1])  
                break
        else:
            return -1               
            

        mapping.append(table)
        num = num + 1
    
    mapping[1] = num
    
    return mapping

def createRoutetable(shortaddr, network_n):
    '''
    :param shortaddr:
    :param network_n:
    :return: routetable
    创建路由表列表，添加命令名和数目。
    路径列表是一个包含所有路径的列表，双重循环搜索短地址，搜索到路径，查找routeID,填入路由表表项列表，
    查找源地址目的地址，填入路由表表项列表，查找下一跳地址，填入路由表表项列表，将路由表表项列表添加到路由表列表中，
    路由计数变量加1
    将路由计数变量填入路由表列表中。
    '''

    routetable = []
    path = []
    tablenum = 0
    routetable.append('setroutetable')
    routetable.append(0)

    path = network_n.pathlist
    for i in path:
        for k in i:
            if k == shortaddr:
                table = []
                routeID = network_n.get_routeID(i)
                table.append(routeID[1]) #下行路径
                table.append(i[0])
                table.append(i[-1])
                num = i.index(k)
                table.append(i[num + 1])
                routetable.append(table)
                tablenum = tablenum + 1

                table_1 = []
                table_1.append(routeID[0]) #上行路径
                table_1.append(i[-1])
                table_1.append(i[0])
                num = i.index(k)
                table_1.append(i[num - 1])
                routetable.append(table_1)
                tablenum = tablenum + 1

    if(tablenum == 0):
        return -1
    routetable[1] = tablenum
    return routetable

def ActiveSlot_Calculation(shortaddr, path):

    num = len(path)
    i = 0
    for key in path:
        if(key == shortaddr):
            i = i + 1
            return i
        i = i + 1
    print "shortaddr not found!"
    return -1

def createSuperframe(shortaddr, network_n):
    '''

    :param shortaddr:短地址
    :param network_n: WIA-PA对象
    :return: superframe表，格式为[命令，数量，[短地址，时隙号]，[短地址，时隙号]，.......]
    '''

    superframe = []
    num = 0
    superframe.append("setsuperframe")
    superframe.append(num)

    for key in network_n.pathlist:
        for i in key:
            if(i == shortaddr):
                table = []
                tmp = ActiveSlot_Calculation(shortaddr, key)
                if(tmp == -1):
                    return -1
                table.append(shortaddr)
                table.append(tmp)
                superframe.append(table)
                num = num + 1
    superframe[1] = num
    return superframe

def createLinktable(shortaddr, network_n):
    '''

    :param shortaddr:
    :param network_n:
    :return: 链路表信息，结构为[命令,数量,[短地址,父节点地址],[短地址,父节点地址].....]
    '''
    Linktable = []
    num = 0
    Linktable.append('setlinktable')
    Linktable.append(num)

    for key in network_n.pathlist:
        tmp = 0
        for i in key:
            if(i == shortaddr):
                table = []
                table.append(shortaddr)
                table.append(key[tmp - 1])
                Linktable.append(table)
                num = num + 1
            tmp = tmp + 1
    Linktable[1] = num
    return Linktable
for key in network_1.deviceinfo:
    if(network_1.deviceinfo[key] == '2'):
        routetable = createRoutetable(key, network_1)
        if(routetable != -1):
            print("routetable: %s" % routetable)


# mappingtable = createMappingtable(schedulinginfo, network_1, network_2)
# print("mappingtable: %s" %mappingtable)
# doc = multhreading_new.setxml(mappingtable)
# print("mapping xml: %s" %doc)
# superframe = createSuperframe('0002', network_1)
# print "superframe: %s" %superframe
# doc = multhreading_new.setxml(superframe)
# print "superframe xml: %s" %doc
linktable = createLinktable('0002', network_1)
print "linktable: %s" %linktable
doc = multhreading_new.setxml(linktable)
print "linktable xml: %s" %doc
# doc = multhreading_new.setxml(routetable)
# print("route xml: %s" %doc)
# shortaddress = '002'
# h = httplib2.Http()
# resp, content = h.request("http://[2016::5]:12345/topology", "GET", doc)
# # resp, content = h.request("http://www.baidu.com/")
# print "resp: %s" %resp
# print "content: %s" %content
