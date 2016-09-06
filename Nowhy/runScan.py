#!/usr/bin/env python 
# -*- coding:utf-8 -*-
'''
#address: http://10.101.1.215/services/scannerTaskService
#user:  admin
#passwd: 123abc

'''
import suds
import subprocess
from suds.sax.element import Element
from suds.client import Client
from suds import WebFault
from suds.transport import TransportError
import urllib2
import logging
import time
import sys
import json
import TasksqlmapClient as SqlClie
import config as cfg
import socket
import os
import base64
logging.getLogger('suds.client').setLevel(logging.CRITICAL)
pcName = socket.gethostname()
ip = socket.gethostbyname(pcName)
pcName = pcName + str(os.getpid())

'''
target = "http://www.gdhuachi.net/news_show.php?id=108"
data = ''
cookie = ''
scan = SqlClie.SqlMclient(config.API_URL,target,'GET',data,cookie)
scan.run()
'''

url = "http://10.101.1.215/services/scannerTaskService?wsdl"

def getClient():
    try:
        code = Element('UserName').setText('admin')
        pwd = Element('PassWord').setText('123abc')
        en = ('RequestSOAPHeader','http://com.appScan.cxf/')
        e = Element('auth',ns = en)
        e.insert(code)
        e.insert(pwd)
        c = Client(url,cache=None)
        c.set_options(soapheaders=e)
        return c
    except urllib2.URLError:#no internet connection
        print "[*]no internet connection. try again[*]"
        time.sleep(2)
        getClient()
    except TransportError:#HTTP Error 500: Internal Server Error
        print "[*]Auth failed. try again[*]"
        time.sleep(2)
        getClient()
    except(KeyboardInterrupt) as Exit:
        print("[*]\nExit[*]")
        sys.exit(0)
    except Exception as e:
        print str(e)
        sys.exit(0)


def sendInfo(client,jsn):
    try:
        client.service.receiveValidateInfo(jsn,ip,pcName)
    except suds.WebFault as detail:
        print "[*]call receiveValidateInfo failed. try again[*]"
        time.sleep(2)
        sendInfo(client,jsn)



def main():
    client = getClient()
    while True:
        text_str = client.service.getVulInfo('GW-G001',ip,pcName)
        json_str = json.loads(text_str)
        # json_str = base64.b64decode(str(json_str))
        # print "***JSON_STR***",json_str
        if json_str:
            jsn = []
            for ret_d in json_str:
                url = ret_d.get('path','[Empty!]')
                arg = ret_d.get('vulScanners','[Empty!]')
                task_id = ret_d.get('id')
                payload=arg[0].get('request')
                payload = base64.b64decode(payload)
                # print "[*]GET没解析之前:[*]:",payload
                if payload.find('GET') > -1:
                    try:
                        get_payload = payload.split("?")[1].split('HTTP')[0]
                        if "'" in get_payload:
                            get_payload = get_payload.split("'")[0]
                        if "%" in get_payload:
                            get_payload = get_payload.split("%")[0]
                        if "&" in get_payload:
                            get_payload = get_payload.split("&")[0]
                        print "[*]GET载荷[*]:",get_payload
                        if get_payload == "":
                            print "获取扫描信息出错，正在重新获取中... "
                            continue
                        get_target = url + "?" + str(get_payload)   #COOKIE > None
                    except Exception as e:
                        continue
                    # print "GET_target>==================:",get_target
                    scan = SqlClie.SqlMclient(cfg.API_URL,get_target,'GET','')
                    result = scan.run()
                    if result.get('data'):
                        data = result.get('data')[0].get('ret')[0][2]
                        jsn.append({"ret":data,"id":task_id,"status":"success"})

                    else:
                        jsn.append({"ret":result['data'],"id":task_id,"status":"failed"})

                elif payload.find('POST') > -1:
                    try:
                        print "[*]POST没解析之前[*]:",payload
                        data = payload.split('*/*')[1].split("'")[0]
                        if "%" in data:
                            data = payload.split('%')[0]
                        print "[*]POST载荷[*]:",data
                    except Exception as e:
                        continue
                    scan = SqlClie.SqlMclient(cfg.API_URL,url,'POST',data,'')
                    result = scan.run()
                    if result.get('data'):
                        data = result.get('data')[0].get('ret')[0][2]
                        jsn.append({"ret":data,"id":task_id,"status":"success"})

                    else:
                        jsn.append({"ret":result['data'],"id":task_id,"status":"failed"})

            sendjsn = json.dumps(jsn)
            print "\t[*][!][!]扫描成功，发送数据[*]:\t",sendjsn
            print "----------------------\n"
            sendInfo(client,sendjsn)

        else:
            print "[*]\t没有漏洞可扫描，等待添加新漏洞...[*]\t"
            time.sleep(2)
            main()


if __name__ == '__main__':
    main()
