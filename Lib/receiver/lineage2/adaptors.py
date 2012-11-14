import datetime
from Lib.receiver.lineage2.handlers import Lineage2ListLogHandler
from Lib.receiver.core.exceptions import InternalException

__author__ = 'bulat.fattahov'
import sys
from Lib.receiver.core.adaptors import Adaptor, DefaultAdaptor
from Lib.receiver.core.factories import  FromDictFactory
from Lib.receiver.lineage2.pageTypes import PageType
import Lib.receiver.core.adaptors


class Lineage2AdaptorFactory(FromDictFactory):
    names = {PageType.LOGIN_PAGE: "LoginPageAdaptor",
             PageType.LIST_LOG: "ListLogAdaptor",
             PageType.CHANGE_CHARACTER: "ChangeCharacterAdaptor",
             PageType.CHANGE_JOB: "ChangeJobAdaptor",
             PageType.APPROVE_REQUEST: "ApproveRequestAdaptor",
             PageType.APPROVE_REQUEST_SECOND: "ApproveRequestAdaptor",
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
#            todo worldlist
            'worldList': 71
        }

        defaults.update(result)
        return defaults


class ChangeCharacterAdaptor(DefaultAdaptor):
#    changeCharacterParser writes in this array
    defaults = {}

    def adapt(self, params=None):
        result = DefaultAdaptor.adapt(self, params)
        if self.defaults.__len__() == 0:
            return result

        result.update(self.defaults)

        if "modifyWay" in params or params["modifyWay"] == "absolute":
            for field in self.defaults:
                if field in params:
                    result[field] = params[field]
# if relative change
        else:
            for field in self.defaults:
                if field in params:
                    try:
                        result[field] = self.defaults[field] + params[field]
                    except TypeError:
                        continue

#        we will always change absolute because face and hair properties do not save if relative change
        result["modifyWay"] = "absolute"
        if "memo" in params:
            result["memo"] = params["memo"] + " Created by script"
        else:
            result["memo"] = "Created by script"

        return result

class ChangeJobAdaptor(DefaultAdaptor):
    def adapt(self, params=None):
        result =  DefaultAdaptor.adapt(self, params)
        if 'job' in params:
            result.update({"SubJobDropDownList":params["job"],
                           "change":"Change of a sub-class"})
            return result
        raise InternalException(message="Job field is required!")


class ApproveRequestAdaptor(DefaultAdaptor):
    def adapt(self, params=None):
        result = DefaultAdaptor.adapt(self, params)
        if "approve" in params:
            result.update({
                "approve": "Approve"
            })
            return result
        elif "reject" in params:
            result.update({
                "reject" : "Reject"
            })
            return result
        else:
            raise InternalException(message="Approve or reject?")
