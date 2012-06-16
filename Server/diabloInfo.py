#!/usr/local/bin/python2.7
#coding=utf-8

from sgmllib import SGMLParser
import sys,urllib2,urllib,cookielib

class spider(SGMLParser):
    def __init__(self):
        
        SGMLParser.__init__(self)
        
        self.m_resut_info = {}
        self.m_server_list = []        
        self.m_server_info = {} # m_server_name:m_server_status         
        self.m_server_list_name = '' #服务类型
        self.m_server_status = ''    #服务状态
        self.m_server_name = ''      #服务名

        self.serverDiv = False;
        self.usefulData = False;
        
        self.h3 = False
        self.h4 = False
        
        self.span = False;
        
        self.depth  =0
        
        self.infoClassArray = ['server-list',
                                  'server',
                                  'server alt',
                                     'status-icon up',
                                     'status-icon down',
                                     'Available',
                                     'Maintenance',
                                     'server-name']
        
        self.serverListStart = False        
        
        self.names = ""
        self.dic = {}  
    
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener=urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)       
    
    def parseDiabloServer(self,url):
        req=urllib2.Request(url)
        self.file=urllib2.urlopen(req).read()
        #print self.file
                
    def start_h3(self,attrs):
        for k,v in attrs:
            if k == 'class' and v == 'category':                
                self.h3 = True                
    def end_h3(self):
        self.h3=False
    
    def start_h4(self,attrs):
        for k,v in attrs:
            if k == 'class' and v == 'subcategory':
                self.h4 = True
    def end_h4(self):
        self.h4=False
    
    def start_span(self,attrs):
        for k,v in attrs:
            if k == 'class' and v == 'category':                
                self.span = True                
    def end_span(self):
        self.span = False
    
    def start_div(self,attrs):
        if self.serverDiv == True:
            self.depth += 1
        
        for k,v in attrs:
            if k == 'class':
                if v == 'server-status':
                    self.serverDiv = True;                
                elif self.serverDiv == True:
                    self.usefulData = False
                    if v == 'server-list':
                        self.usefulData = True
                        self.serverListStart = True
                        #print '-----'+v 
                        #这里创建server_list
                        self.m_server_list = []

                    elif v == 'status-icon up' or v == 'status-icon down':
                        self.usefulData = True
                        #这里获取服务状态
                        #print '  '+v 
                        self.m_server_status = v

                    elif v == 'Available' or v == 'Maintenance':
                        self.usefulData = True
                        #本来这里也得获取服务状态，暂时没能获取，不知道为啥
                        print '  '+v 
                    elif v == 'server-name':
                        self.usefulData = True
                        #print v 
                        #这里是获取服务名key
                else:
                    self.serverDiv = False
                    self.usefulData = False
                    break;

    def end_div(self):
        if self.depth == 0:
            self.serverDiv = False
            self.usefulData = False
        if self.serverDiv == True:
            self.depth -= 1
            if self.serverListStart == True:
                if self.h3 == True or self.h4 == True:
                    self.serverListStart = False
                    print '-----'
                

    def handle_data(self,text):
        #服务器地区名
        if self.h3 == True:
            #到这里需要判断下server_list是否空，存一份。           
            if self.m_server_list_name != '':
                print self.m_server_list_name
            if self.m_server_list != []:
                print self.m_server_list
            #这里是服务地区名
            self.m_server_list_name = text.strip()
            #print '=============>>>>>>>>>>>>'+text.strip()   
        #拍卖场
        elif self.h4 == True:
            #到这里需要判断下server_list是否空，存一份。            
            if self.m_server_list_name != '':
                print self.m_server_list_name
            if self.m_server_list != []:
                print self.m_server_list
            #这里是现金拍卖场
            self.m_server_list_name = text.strip()
            #print '========================='+text.strip()

        #拍卖场服务名
        elif self.usefulData == True and text.strip() != '':
            #获取服务名内容
           #print '=====>'+text.strip()   
           self.m_server_name = text.strip()
           #设置好服务字典
           self.m_server_info = {}
           self.m_server_info[self.m_server_name] = self.m_server_status
           self.m_server_list.append(self.m_server_info)
        #self.dic.setdefault(self.names,[]).append(text)
    
    def show(self):
        type = sys.getfilesystemencoding()
        for key in self.dic:
            print ( (''.join(key)).replace(' ','')).decode('utf-8').encode(type), \
                ( (''.join(self.dic[key])).replace(' ','')).decode('utf-8').encode(type)




renrenspider=spider()
renrenspider.parseDiabloServer('http://us.battle.net/d3/en/status')
renrenspider.feed(renrenspider.file)
#renrenspider.show()
