# coding=utf-8
from urllib2 import HTTPError
from Lib.receiver.core.adaptors import Adaptor
from Lib.receiver.core.exceptions import LoginException
from Lib.receiver.core.handlers import Handler
from Lib.receiver.core.initializers import Initializer
from Lib.receiver.core.parsers import Parser
from Lib.receiver.core.urlCreators import UrlCreator
from Lib.receiver.lineage2.adaptors import Lineage2AdaptorFactory
from Lib.receiver.lineage2.handlers import Lineage2HandlerFactory
from Lib.receiver.lineage2.initializers import Lineage2InitializerFactory
from Lib.receiver.lineage2.pageTypes import PageType
from Lib.receiver.core.receivers import NotLoggedInException, Receiver
from Lib.receiver.core.strategy import Page
from Lib.receiver.core.supports import EuroSupport
from Lib.receiver.lineage2.parsers import Lineage2ParserFactory
from Lib.receiver.lineage2.receivers import Lineage2ReceiverFactory
from Lib.receiver.lineage2.urlCreators import Lineage2UrlCreatorFactory

UrlCreator.setFactory(Lineage2UrlCreatorFactory())
Adaptor.setFactory(Lineage2AdaptorFactory())
Initializer.setFactory(Lineage2InitializerFactory())
Receiver.setFactory(Lineage2ReceiverFactory())
Parser.setFactory(Lineage2ParserFactory())
Handler.setFactory(Lineage2HandlerFactory())

support = EuroSupport( login='bulat.fattahov', password='1qaz2wsx')

page = Page(support, PageType.LIST_LOG)
try:
#    aspx_ = {'url': "/L2Admin/Default.aspx"}
    params = {'action': "810", "fromDate": "2012-10-07 20:58", "toDate" : "2012-10-08 21:58", "worldList" : 71}
    page.get(params)
except HTTPError as error:
    print error
except NotLoggedInException:
    #            логинимся
    login_page = Page(support, PageType.LOGIN_PAGE)
    try:
        login_page.get()
    except LoginException:
        pass # todo обработку невозможности залогиниться
    else:
        # пробуем еще раз получить страницу
        page_string = page.get(params)
        print page_string