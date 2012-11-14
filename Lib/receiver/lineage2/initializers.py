__author__ = 'bulat.fattahov'
import sys
import Lib.receiver.core.initializers
from Lib.receiver.core.factories import FromDictFactory
from Lib.receiver.lineage2.pageTypes import PageType
from Lib.receiver.core.initializers import DefaultInitializer


class Lineage2InitializerFactory(FromDictFactory):
    names = {PageType.PAGE_WITHOUT_INITIALIZATION : "WithoutInitialization",
             PageType.APPROVE_REQUEST_SECOND : "WithoutInitialization",
             PageType.CHANGE_CHARACTER:"Lineage2ChangeCharacterInitializer"}

    # where we will look for initializers: in defaults and in this file
    whereToSeek = [Lib.receiver.core.initializers,
                   sys.modules[__name__]]

#=====================================================

class Lineage2ChangeCharacterInitializer(DefaultInitializer):
    def __init__(self, page):
        DefaultInitializer.__init__(self, page)

    def initPage(self, params=None):
        page_handler = self.page.handler
        url = page_handler.urlCreator.createUrl(params)
        page_string = page_handler.receiver.receive(url, params)
        return  page_string
