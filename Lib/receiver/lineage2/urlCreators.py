import re
from Lib.receiver.core.exceptions import InternalException
from Lib.receiver.core.factories import  FromDictFactory
from Lib.receiver.core.urlCreators import UrlCreator
from Lib.receiver.lineage2.pageTypes import PageType
import  Lib.receiver.core.urlCreators
import sys

__author__ = 'bulat.fattahov'


class Lineage2UrlCreatorFactory(FromDictFactory):
    names = {PageType.PAGE_WITHOUT_INITIALIZATION: 'WithoutInitializationUrlCreator',
             PageType.LIST_LOG: "ListLogUrlCreator"}

    UrlCreator.urlNameMap = {
        PageType.LOGIN_PAGE: "/L2Admin/Login.aspx",
        PageType.PAGE_WITHOUT_INITIALIZATION: "",
        PageType.LIST_LOG: "/L2Admin/Log/ListLog.aspx",
        PageType.ENTER_WORLD_BY_IP: "/L2Admin/Log/ListLog.aspx",
        PageType.ENTER_WORLD_BY_CHAR_NAME: "/L2Admin/Log/ListLog.aspx",
        PageType.FIND_CHARACTER_BY_ACCOUNT: '/L2Admin/Char/FindCharacterByAccount.aspx',
        PageType.CHARINFO_BY_NAME: "/L2Admin/Char/ListCharacter.aspx",
        PageType.SET_WORLD_ID: "/L2Admin/WorldList.aspx",
        PageType.CHARINFO_BY_NAME_AFTER: "/L2Admin/Char/ViewCharacter.aspx",
        PageType.ITEMS_BY_CHARNAME: "/L2Admin/Char/ListCharacterItem.aspx",
        PageType.CHARITEM_URL: "/L2Admin/Char/ListCharacterItem.aspx",
        PageType.CHARACTER_BY_ACCOUNT: "/L2Admin/Char/ListCharacter.aspx",
        PageType.COUNT_OF_ITEMS_FOR_ID: "/L2Admin/Item/ListItemByType.aspx",
        PageType.FIND_ITEM: "/L2Admin/Char/FindItem.aspx?key=ITEM_TO_ADD&itemName=",
        PageType.CHARACTER_BY_ACCOUNT_ON_ALL_SERVERS: "/L2Admin/Char/FindCharacterAtAllServer.aspx",
        PageType.CHARACTER_BY_NAME_ON_ALL_SERVERS: "/L2Admin/Char/FindCharacterAtAllServer.aspx",
        PageType.SERVER_MONITORING_AT_ONE_PAGE: "/L2Admin/ServerStat/ServerMonitoringAtOnePage.aspx",
        PageType.AMOUNT_BY_ITEM_TYPE_AND_SERVER: "/L2Admin/Item/ListItemByType.aspx",
        PageType.WORLDS_LIST: "/L2Admin/WorldList.aspx",
        PageType.LIST_REQUEST: "/L2Admin/Request/ListRequest.aspx",
    }

    def __init__(self):
        self.whereToSeek = [Lib.receiver.core.urlCreators,
                            sys.modules[__name__]]

    def getForPage(self, page):
        object = FromDictFactory.getForPage(self, page)
    # provide our default url creator if not found
        if not object:
            return Lineage2DefaultUrlCreator(page)
        return object

class Lineage2DefaultUrlCreator(UrlCreator):
    defaultServerId = '71'

    def createUrl(self, params):
        serverId = (str)(params['worldList']) if (params and 'worldList' in params) else self.defaultServerId
        return UrlCreator.createUrl(self, params) + '?WorldId=' + serverId


class ListLogUrlCreator(UrlCreator):
    naviUrl = None

    def setNaviUrl(self, naviUrl):
        self.naviUrl = naviUrl

    def createUrl(self, params):
        url_base = UrlCreator.createUrl(self, params)
        if not self.naviUrl:
            return url_base + '?WorldId=' + (str)(params['worldList'])
        else:
            if 'page_number' in params:
                page_number = params['page_number']
                linkPattern = 'PageIndex=\d+'
                return re.sub(linkPattern, 'PageIndex=' + page_number, self.naviUrl)
