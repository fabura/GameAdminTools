# coding=utf-8
from Lib.receiver.core.handlers import Handler

__author__ = 'bulat.fattahov'

class Page(object):
    """"Main class. Has handler"""
    #    pageName = None
    handler = None
    pageName = None
    support = None
    page__ViewState = ''
    page__ActionKey = ''

    def getViewState(self):
            return self.page__ViewState

    def setViewState(self, viewState):
            self.page__ViewState = viewState

    def getActionKey(self):
        return self.page__ActionKey

    def setActionKey(self, actionKey):
        self.page__ActionKey = actionKey

    def __init__(self, support, pageName):
        self.pageName = pageName
        self.support = support
        self.handler = Handler.getHandler(self)

    def get(self, params=None):
        return self.handler.handle(params)

    def setPageName(self, pageName):
        self.handler = Handler.getHandler(pageName)

