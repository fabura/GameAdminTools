import datetime
from Lib.receiver.lineage2.handlers import Lineage2ListLogHandler

__author__ = 'bulat.fattahov'
import sys
from Lib.receiver.core.adaptors import Adaptor, DefaultAdaptor
from Lib.receiver.core.factories import  FromDictFactory
from Lib.receiver.lineage2.pageTypes import PageType
import Lib.receiver.core.adaptors


class Lineage2AdaptorFactory(FromDictFactory):
    names = {PageType.LOGIN_PAGE: "LoginPageAdaptor",
             PageType.LIST_LOG: "ListLogAdaptor",
             PageType.PAGE_WITHOUT_INITIALIZATION: "WithoutInitializationAdaptor"}

    # where we will look for adaptors: in defaults and in this file
    whereToSeek = [Lib.receiver.core.adaptors,
                   sys.modules[__name__]]

#=====================================================
class LoginPageAdaptor(DefaultAdaptor):
    def adapt(self, params=None):
        result = DefaultAdaptor.adapt(self, params)
        result['loginSubmit'] = 'Login'
        result['id'] = self.page.support.getLogin()
        result['password'] = self.page.support.getPassword()
        return result

    def __init__(self, page):
        Adaptor.__init__(self, page)


class ListLogAdaptor(DefaultAdaptor):
    def adapt(self, params=None):
    #         result is a sum of system info (Viewstate and so on) and params
        result = DefaultAdaptor.adapt(self, params)
        current_time = datetime.datetime.now()
        to_date = current_time.strftime("%Y-%m-%d %H:%M")
        #       for last day
        from_date = (current_time - datetime.timedelta(1)).strftime("%Y-%m-%d %H:%M")

        defaults = {
#            'action': '803',
            'search': 'Search',
            'rowsPerPage': Lineage2ListLogHandler.LOGS_BY_PAGE,
            'SearchTarget': "targetChar",
            'toDate': to_date,
            'fromDate': from_date,
            'worldList': 71
        }

        defaults.update(result)
        return defaults