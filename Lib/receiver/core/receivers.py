import re
import urllib
from Lib.receiver.core.exceptions import NotLoggedInException, InternalException
from Lib.receiver.core.factories import Factory

__author__ = 'bulat.fattahov'

class Receiver():
    ReceiverFactory = None
    names = {}
    page = None
    opener = None

    @staticmethod
    def getReceiver(page):
        if Receiver.ReceiverFactory:
            object = Receiver.ReceiverFactory.getForPage(page)
            if object:
                return object
        return DefaultReceiver(page)

    def receive(self, url, params = None):
        pass

    def __init__(self, page):
        self.page = page
        self.opener = page.support.getOpener()
        return

    # todo check for common errors
    def checkErrors(self, response):
        return response.read()

    @staticmethod
    def setFactory(factory):
        if not isinstance(factory, Factory):
            raise InternalException('It is not a factory!')
        Receiver.ReceiverFactory = factory


class DefaultReceiver(Receiver):
    def __init__(self, page):
        Receiver.__init__(self, page)

    def receive(self, url, params = None):
        if self.opener:
            if params:
                post_string =  urllib.urlencode(params)
            else:
                post_string = None
            response = self.opener.open(url, post_string)
            return self.checkErrors(response)
        return None


    def checkErrors(self, response):
        page_string = Receiver.checkErrors(self, response)
        if re.search('top.location.href = "Login.aspx"', page_string):
            raise NotLoggedInException()
        return page_string