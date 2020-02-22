#!/usr/bin/env python3

import sys
import time
import argparse
from getpass import getpass
from urllib import request, parse
from configparser import ConfigParser

categories = {
    'btech': 22,
    'dual': 62,
    'diit': 21,
    'faculty': 82,
    'integrated': 21,
    'mtech': 62,
    'phd': 61,
    'retfaculty': 82,
    'staff': 21,
    'irdstaff': 21,
    'mba': 21,
    'mdes': 21,
    'msc': 21,
    'msr': 21, 
    'pgdip': 21,
    'visitor': 21,
    'student': 21,
    'guest': 82
}


class LoginManager: 
    def __init__(self, username, password, proxy_category, sessionid=None):
        self.username = username
        self.password = password
        self.proxy_category = proxy_category
        self.proxylogin_url = 'https://proxy{}.iitd.ac.in/cgi-bin/proxy.cgi'.format(categories[proxy_category])
        self.create_session()

    @staticmethod
    def read_page(url):
        return request.urlopen(url).read().decode('utf-8')

    @staticmethod
    def submit_form(url, form):
        return request.urlopen(url, parse.urlencode(form).encode()).read().decode('utf-8')

    def create_session(self):
        page = self.read_page(self.proxylogin_url)
        token = '<input name="sessionid" type="hidden" value="'
        token_index = page.index(token) + len(token)
        sessionid = page[token_index: token_index + 16]
        self.sessionid = sessionid

    def login(self):
        form = {
            'sessionid': self.sessionid, 
            'action': 'Validate', 
            'userid': self.username, 
            'pass': self.password
        }
        self.create_session()
        response = self.submit_form(self.proxylogin_url, form)
        if "Either your userid and/or password does'not match." in response:
            return 'Incorrect credentials'
        elif 'You are logged in successfully as '+self.username in response:
            return 'Success'
        elif 'already logged in' in response:
            return 'Already logged in'
        elif 'Session Expired' in response:
            return 'Session expired'
        else:
            return 'Not Connected'

    def logout(self):
        form = {
            'sessionid': self.sessionid,
            'action':'logout',
            'logout':'Log out'
        }
        self.create_session()
        response = self.submit_form(self.proxylogin_url, form)
        if 'you have logged out from the IIT Delhi Proxy Service' in response:
            return 'Success'
        elif 'Session Expired' in response:
            return 'Session expired'
        else:
            return 'Failed'
        
    def refresh(self):
        form = {
            'sessionid': self.sessionid, 
            'action':'Refresh'
        }
        response = self.submit_form(self.proxylogin_url, form)
        if 'You are logged in successfully' in response:
            if 'You are logged in successfully as '+self.username in response:
                return 'Success'
            else:
                return 'Not logged in'
        elif 'Session Expired' in response:
            return 'Session expired'
        else:
            return 'Not connected'


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--config', help='Configuration INI file containing credentials')
    group.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('-r', '--refresh', action='store_true', help='After logging in, keep running and refreshing')
    parser.add_argument('-s', '--skip-tls-verify', action='store_true', help='Foolishly accept TLS certificates signed by unkown certificate authorities')
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    
    if args.skip_tls_verify:
        import ssl
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

    if args.config:
        config = ConfigParser()
        config.read(args.config)
        login_manager = LoginManager(config['PROXY']['USERNAME'], config['PROXY']['PASSWORD'], config['PROXY']['CATEGORY'])
    else:
        username = input('[*] Username: ')
        password = getpass('[*] Password: ')
        category = input('[*] Category: ')
        login_manager = LoginManager(username, password, category)
    
    login_manager.logout()
    print('[*] Logging in... ', end='')
    status = login_manager.login()
    print(status)
    
    if args.refresh:    
        while True:
            time.sleep(60)
            print('[*] Refreshing... ', end='')
            status = login_manager.login()
            print(status)


if __name__=="__main__":
    main()
