# coding=utf-8
import cookielib
import re
import urllib2
from Lib.receiver.core.exceptions import InternalException

__author__ = 'bulat.fattahov'

class Support():
    _baseUrl = ''
    login_name = ''
    password = ''
    opener = None

    def getBaseUrl(self):
        return self._baseUrl

    def __init__(self, login, password):
        self.login_name = login
        self.password = password

    def getOpener(self):
        if not self.opener:
            url = self.getBaseUrl()
            if not url:
                raise InternalException('Base url is not defined!')
            cleared = re.sub(r"\W", r"_", url)
            jar = cookielib.FileCookieJar("cookies" + cleared + self.login_name)
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        return self.opener

    @staticmethod
    def getSupport(name, login='bulat.fattahov', password='1qaz2wsx'):
        if name == 'euro':
            return EuroSupport(login, password)
        elif name == 'ru':
            return RuSupport(login, password)
        return None

    def getLogin(self):
        return self.login_name

    def getPassword(self):
        return self.password

class EuroSupport(Support):
    def __init__(self, login, password):
        Support.__init__(self, login, password)
        self._baseUrl = 'http://10.64.144.50'


class RuSupport(Support):
    def __init__(self, login, password):
        Support.__init__(self, login, password)
        self._baseUrl = 'https://10.33.148.24'


#======================================================
