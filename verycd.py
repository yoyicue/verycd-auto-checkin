#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import requests
import json
import pickle


class VeryCD:

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) Gecko/20100101 Firefox/14.0.1',
           'Referer':'http://www.verycd.com',
           'Host':'www.verycd.com',
           'X-Requested-With':'XMLHttpRequest'}
    login_url = 'http://www.verycd.com/signin'
    check_url = 'http://www.verycd.com/game/ajax/checkin/'

    def __init__(self, username=None, password=None, cookie_file='.verycd_cookies'):
        self.username = username
        self.password = password
        self.cookie_file = cookie_file

    def get_url(self, url, **args):
        return requests.get(url, **args)

    def post_url(self, url, **args):
        return requests.post(url, **args)

    def login_success(self):
        return self.login_request.text == '{"status":"ok"}'

    def checkin_success(self):
        return json.loads(self.checkin_request.text).get('code') == 0

    def cookies_failed(self, request):
        return request.text == '{"code":1,"msg":"\u672a\u767b\u5f55\u7528\u6237"}'

    def save_cookies(self):
        cookies = self.login_request.cookies
        with open(self.cookie_file, 'w') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(cookies), f)

    def get_cookies(self):
        with open(self.cookie_file) as f:
            try:
                cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
                return cookies
            except EOFError:
                self.login()
                return self.login_request.cookies

    def login(self):     
        payload = {'username':self.username,'password':self.password}
        request = self.post_url(self.login_url, 
                                data=payload,
                                headers=self.headers,
                                timeout=2,
                                allow_redirects=True)
        self.login_request = request
        assert self.login_success(), 'login failed'
        self.save_cookies()
        print 'login ok, cookies save!'

    def checkin(self):    
        request = self.get_url(self.check_url, 
                                headers=self.headers, 
                                cookies=self.get_cookies(),
                                timeout=2)
        self.checkin_request = request
        if self.cookies_failed(request):
            self.login()
            request = self.get_url(self.check_url, 
                                   headers=self.headers, 
                                   cookies=self.login_request.cookies,
                                   timeout=2)
            self.checkin_request = request
        assert self.checkin_success(), json.loads(request.text).get('msg').encode('utf-8')
        print 'checkin done!'


def command(args=sys.argv[1:]):

    def usage():
        print """VeryCD Auto Checkin Tool v1.0.0
usage: verycd.py [checkin|login] [-u 'username,password']
"""        
    
    def message(name):
        print "verycd.py %s -u 'username,password'" %name
        sys.exit(1)

    def client(args):
        verycd = VeryCD()
        try:
            if args[1] == '-u' and len(args) == 3:
                account = args[2].split(',')
                if len(account) == 2:
                    verycd = VeryCD(account[0],account[1])
                    verycd.login()
                    if args[0] == 'checkin': verycd.checkin()
                    sys.exit(1)
                else:
                    message(args[0])
            else:
                message(args[0])    
        except IndexError, e:
            if args[0] == 'login': message(args[0])
            pass
        verycd.checkin()

    if not args:
        usage()
        sys.exit(1)
    if args[0] in ('login','checkin'): 
        client(args)
    else:
        usage()
        sys.exit(1)

if __name__ == "__main__":
    command()