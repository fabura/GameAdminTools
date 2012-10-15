import urllib

__author__ = 'bulat.fattahov'
import sys
import receiver.core.receivers
from receiver.core.receivers import Receiver
from receiver.core.factories import FromDictFactory
from receiver.lineage2.pageTypes import PageType


class Lineage2ReceiverFactory(FromDictFactory):
    names = {PageType.LOGIN_PAGE: 'LoginReceiver'}

    # where we will look for receivers: in defaults and in this file
    whereToSeek = [receiver.core.receivers,
                   sys.modules[__name__]]

#=====================================================

class LoginReceiver(Receiver):
    def __init__(self, page):
        Receiver.__init__(self, page)

    #    todo implement checkErrors Method
    def checkErrors(self, response):
        return Receiver.checkErrors(self, response)

    def receive(self, url, params = None):
        Receiver.receive(self, url, params)
        if self.opener:
            if params:
                post_string =  urllib.urlencode(params)
            else:
                post_string = None
            response = self.opener.open(url, post_string)
            return self.checkErrors(response)
