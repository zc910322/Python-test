# -*- coding:utf-8 -*-
import socket
import threading
from time import ctime,sleep,time,strftime,localtime
from Queue import Queue


import xml.dom.minidom
def setxml(managerList):

    if managerList[0] == 'setroutetable':
        '''
        1构造路由表
        managerList=[命令，数目，[routeID，源地址，目的地址，下一跳地址]，
        [routeID，源地址，目的地址，下一跳地址],......]
        '''
        doc = xml.dom.minidom.Document()
        root = doc.createElement('routetable')  #设置根节点的属性
        root.setAttribute('xmlns', 'cquptSDN:routetable')   
        #将根节点添加到文档对象中
        doc.appendChild(root)
       
        nodeManager = doc.createElement('num')
        nodeManager.appendChild(doc.createTextNode(str(managerList[1])))
        root.appendChild(nodeManager)
    
        for i in managerList[2:]:
    
            nodeManager = doc.createElement('route')
            nodeName = doc.createElement('ID')
            #给叶子节点name设置一个文本节点，用于显示文本内容
            nodeName.appendChild(doc.createTextNode(str(i[0])))
      
            nodeAge = doc.createElement("src")
            nodeAge.appendChild(doc.createTextNode(str(i[1])))
      
            nodeSex = doc.createElement("dst")
            nodeSex.appendChild(doc.createTextNode(str(i[2])))
    
            nodenext = doc.createElement("next")
            nodenext.appendChild(doc.createTextNode(str(i[3])))
           #将各叶子节点添加到父节点Manager中，
           #最后将Manager添加到根节点Managers中
            nodeManager.appendChild(nodeName)
            nodeManager.appendChild(nodeAge)
            nodeManager.appendChild(nodeSex)
            nodeManager.appendChild(nodenext)
            root.appendChild(nodeManager)
          #开始写xml文档
          #fp = open('xc', 'w')
          #idoc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        
    elif managerList[0] == 'setmappingtable':
        '''
        映射表格式：[命令，映射表数量，[源地址，MAC地址，routeID，源短地址，目的短地址，目的地址，routeID，源短地址，目的短地址]，
        [源地址，MAC地址，routeID，源短地址，目的短地址，目的地址，routeID，源短地址，目的短地址]......]
        '''
        doc = xml.dom.minidom.Document()
        root = doc.createElement('mappingtable')  #设置根节点的属性
        root.setAttribute('xmlns', 'cquptSDN:mappingtable')   
        #将根节点添加到文档对象中
        doc.appendChild(root)
       
        nodeManager = doc.createElement('num')
        nodeManager.appendChild(doc.createTextNode(str(managerList[1])))
        root.appendChild(nodeManager)
    
        for i in managerList[2:]:
    
            nodeManager = doc.createElement('mapping')
            nodeName = doc.createElement('src')
            nodeName2 = doc.createElement('dst')
            #给叶子节点name设置一个文本节点，用于显示文本内容
            nodeip = doc.createElement('ip')
            nodeip.appendChild(doc.createTextNode(str(i[0])))
            nodemac = doc.createElement('macaddress')
            nodemac.appendChild(doc.createTextNode(i[1]))
            nodeAge = doc.createElement("routeID")
            nodeAge.appendChild(doc.createTextNode(str(i[2])))

            nodesrcshortaddr = doc.createElement("srcshortaddr")
            nodesrcshortaddr.appendChild(doc.createTextNode(str(i[3])))
            
            nodedstshortaddr = doc.createElement("dstshortaddr")
            nodedstshortaddr.appendChild(doc.createTextNode(str(i[4])))
                              
            nodeip2 = doc.createElement("ip")
            nodeip2.appendChild(doc.createTextNode(str(i[5])))
            nodemac2 = doc.createElement("macaddress")
            nodemac2.appendChild(doc.createTextNode(i[6]))
            nodenext = doc.createElement("routeID")
            nodenext.appendChild(doc.createTextNode(str(i[7])))
            
            nodesrcshortaddr1 = doc.createElement("srcshortaddr")
            nodesrcshortaddr1.appendChild(doc.createTextNode(str(i[8])))
            
            nodedstshortaddr1 = doc.createElement("dstshortaddr")
            nodedstshortaddr1.appendChild(doc.createTextNode(str(i[9])))
           #将各叶子节点添加到父节点Manager中，
           #最后将Manager添加到根节点Managers中
            nodeName.appendChild(nodeip)
            nodeName.appendChild(nodemac)
            nodeName.appendChild(nodeAge)
            nodeName.appendChild(nodesrcshortaddr)
            nodeName.appendChild(nodedstshortaddr)
            nodeName2.appendChild(nodeip2)
            nodeName2.appendChild(nodemac2)
            nodeName2.appendChild(nodenext)
            nodeName2.appendChild(nodesrcshortaddr1)
            nodeName2.appendChild(nodedstshortaddr1)           
            nodeManager.appendChild(nodeName)
            nodeManager.appendChild(nodeName2)

            root.appendChild(nodeManager)
    elif managerList[0] == 'setsuperframe':
        doc = xml.dom.minidom.Document()
        root = doc.createElement('superframe')  # 设置根节点的属性
        root.setAttribute('xmlns', 'cquptSDN:superframe')
        # 将根节点添加到文档对象中
        doc.appendChild(root)

        nodeManager = doc.createElement('num')
        nodeManager.appendChild(doc.createTextNode(str(managerList[1])))
        root.appendChild(nodeManager)

        for i in managerList[2:]:
            nodesuperframe = doc.createElement('superframe')
            nodeid = doc.createElement('ID')
            nodeid.appendChild(doc.createTextNode(str(i[0])))
            nodeMultiple = doc.createElement('Multiple')
            nodeMultiple.appendChild(doc.createTextNode("1"))
            nodeNumberSlots = doc.createElement('NumberSlots')
            nodeNumberSlots.appendChild(doc.createTextNode("128"))
            nodeActiveFlag = doc.createElement('ActiveFlag')
            nodeActiveFlag.appendChild(doc.createTextNode("1"))
            nodeActiveSlot = doc.createElement('ActiveSlot')
            nodeActiveSlot.appendChild(doc.createTextNode(str(i[1])))

            nodesuperframe.appendChild(nodeid)
            nodesuperframe.appendChild(nodeMultiple)
            nodesuperframe.appendChild(nodeNumberSlots)
            nodesuperframe.appendChild(nodeActiveFlag)
            nodesuperframe.appendChild(nodeActiveSlot)
            nodeManager.appendChild(nodesuperframe)

            root.appendChild(nodeManager)

    return  doc.toprettyxml()    

def net_manager(value):
    data = ''
    if value[0] == 'gettopo':   
        data_1 = "GET /network-topology HTTP\n"
        data_2 = data_1 + "Accept:application/xml\n"
        data_3 = data_2 + "Authentication:\n"
        data  = data_3 + " Content-Length:0"
    elif value[0]  == 'getdeviceinfo':
        data_1 = "GET /device/address/info HTTP/1.1\n"
        data_2 = data_1 + "Accept:application/xml\n"
        data_3 = data_2 + "Authentication:\n"
        data   = data_3 + "Content-Length:0"
    elif value[0] == 'getdevicelist':
        data_1 ="GET /device/HTTP/1.1\n"
        data_2 = data_1 + "Accept:application/xml\n"
        data_3 = data_2 + "Authentication:\n"
        data   = data_3 + "Content-Length:0"
    elif value[0] == 'getdeviceUAO':
        data_1 = "GET /device/shortaddress/uao HHTP/1.1"
        data_2 = data_1 + "Accept:application/xml\n"
        data_3 = data_2 + "Authentication:\n"
        data   = data_3 + "Content-Length:0"
    elif value[0] == 'setroutetable':      
        doc = setroutetablexml(value)          
        data_1 = "PUT /device/shortaddress/routetable HTTP/1.1"
        data_2 = data_1 + "Accept:application/xml\n"
        data_3 = data_2 + "Authentication:\n"
        data_4 = data_3 + "Content-Length:\n" 
        data = data_4 + doc
    return data

def net_connect(c,q,req):
    while True:
        try:
          #  print len(q.get(1))
            stri = q.get(1)
            print "获取到命令%s".decode('gbk').encode('utf-8') %stri
            data = net_manager(stri)
            c.sendall(data)
        except:
            flag = 1
        else:
            redata = c.recv(1024)
            print "接收到回复%s".decode('gbk').encode('utf-8') %redata
            req.put(redata,1)

def TCPServer(q, req, Threadname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8078))
    s.listen(5)
    i = 0
    while True:       
        c,addr = s.accept()
        print strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + "一个WIA-PA系统管理器连接到控制器"
        q.append(Queue(100))
        req.append(Queue(100))
        t3 = threading.Thread(target=net_connect,args=(c,q[i],req[i]))
        t3.start()
        sleep(1)
        i=i+1





##主线程
#global q
#global req
#req = []           
#q = []     #commandlist
#managerList = ["gettopo",{'ID' : '1',  'src' : '27.23.3', 'dst' : '27.54.4'}, 
#               {'ID' : '3', 'src' :  '30.23.5', 'dst' : '30.43.5'},
#               {'ID' : '4', 'src' : '29.23.5', 'dst' : '29.34.6'}]
#t1 = threading.Thread(target = TCPServer,args=(1,))
#t1.setDaemon(True)         #守护线程     
#t1.start()                      
#sleep(1)
#while True:
#    if  len(q) > 0:
#        q[0].put(managerList,1)
#        print req[0].get(1)
#        q[0].put(managerList,1)
#        print req[0].get(1)
#        break   
#print 'wen'
#sleep(100)













        





       











