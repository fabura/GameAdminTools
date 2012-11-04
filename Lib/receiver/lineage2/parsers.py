__author__ = 'bulat.fattahov'

import sys
import lxml.html
import Lib.receiver.core.parsers
from Lib.receiver.core.parsers import  Parser
from Lib.receiver.core.factories import FromDictFactory
from Lib.receiver.lineage2.pageTypes import PageType


class Lineage2ParserFactory(FromDictFactory):
    names = {PageType.LIST_LOG: "ListLogParser",
             PageType.AMOUNT_BY_ITEM_TYPE_AND_SERVER: "ItemAmountParser"}

    # where we will look for parsers: in defaults and in this file
    whereToSeek = [Lib.receiver.core.parsers,
                   sys.modules[__name__]]

    def getForPage(self, page):
        object = FromDictFactory.getForPage(self, page)
        # provide our default parser if not found
        if not object:
            return Lineage2DefaultParser(page)
        return object

#=====================================================

class Lineage2DefaultParser(Parser):
    lxlmldoc = None
    naviUrl = None

    def __init__(self, page):
        Parser.__init__(self, page)

    def parse(self, page_str):
        Parser.parse(self, page_str)
        self.lxlmldoc = lxml.html.document_fromstring(page_str)

        temp = self.lxlmldoc.xpath('//form/input[@name="__VIEWSTATE"]')
        if temp and len(temp): self.page.setViewState(temp[0].value)

        temp = self.lxlmldoc.xpath('//form/input[@name="actionKey"]')
        if temp and len(temp): self.page.setActionKey(temp[0].value)
        return page_str


class ListLogParser(Lineage2DefaultParser):
    def parse(self, page_str):
        page_str = Lineage2DefaultParser.parse(self, page_str)
        table = self.lxlmldoc.xpath('//*[@id="ListLog"]/table[2]')
        if not self.naviUrl:
            naviUrl = self.lxlmldoc.xpath('//*[@id="navigatorView2_navigation"]/table/tr/td/a[1]')
            if naviUrl:
                url = naviUrl[0].attrib['href']
                self.naviUrl = url
        return page_str


class ItemAmountParser(Lineage2DefaultParser):
    def parse(self, page_str):
        page_str = Lineage2DefaultParser.parse(self, page_str)
        no_result = self.lxlmldoc.xpath('//*[@id="ListItemByType"]/table[2]/tbody/tr[3]/td')
        if (no_result and no_result[0].text == 'There is no result.'):
            return 0
        amount = self.lxlmldoc.xpath('//*[@id="ListItemByType"]/table[2]/tr[3]/td[6]')
        if (amount and amount.__len__() and amount[0].text):
            return amount[0].text.replace(',', '')
        return amount
