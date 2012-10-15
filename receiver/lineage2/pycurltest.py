# coding=utf-8
from urllib2 import HTTPError
from receiver.core.adaptors import Adaptor
from receiver.core.exceptions import LoginException
from receiver.core.handlers import Handler
from receiver.core.initializers import Initializer
from receiver.core.parsers import Parser
from receiver.core.urlCreators import UrlCreator
from receiver.lineage2.adaptors import Lineage2AdaptorFactory
from receiver.lineage2.handlers import Lineage2HandlerFactory
from receiver.lineage2.initializers import Lineage2InitializerFactory
from receiver.lineage2.pageTypes import PageType
from receiver.core.receivers import NotLoggedInException, Receiver
from receiver.core.strategy import Page
from receiver.core.supports import EuroSupport
from receiver.lineage2.parsers import Lineage2ParserFactory
from receiver.lineage2.receivers import Lineage2ReceiverFactory
from receiver.lineage2.urlCreators import Lineage2UrlCreatorFactory

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