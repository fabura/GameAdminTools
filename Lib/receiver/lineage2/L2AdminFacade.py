# coding=utf-8
from Lib.receiver.core.adaptors import Adaptor
from Lib.receiver.core.decorators.log_admin import log_admin
from Lib.receiver.core.exceptions import NotLoggedInException, LoginException, InternalException
from Lib.receiver.core.handlers import Handler
from Lib.receiver.core.initializers import Initializer
from Lib.receiver.core.parsers import Parser
from Lib.receiver.core.receivers import Receiver
from Lib.receiver.core.strategy import Page
from Lib.receiver.core.supports import EuroSupport
from Lib.receiver.core.urlCreators import UrlCreator
from Lib.receiver.lineage2.adaptors import Lineage2AdaptorFactory
from Lib.receiver.lineage2.handlers import Lineage2HandlerFactory
from Lib.receiver.lineage2.initializers import Lineage2InitializerFactory
from Lib.receiver.lineage2.pageTypes import PageType
from Lib.receiver.lineage2.parsers import Lineage2ParserFactory
from Lib.receiver.lineage2.receivers import Lineage2ReceiverFactory
from Lib.receiver.lineage2.urlCreators import Lineage2UrlCreatorFactory

__author__ = 'bulat.fattahov'

#==================================================================================
def tryToLoggedIn():
    def outer(fun):
        def inner(*args, **kwargs):
            try:
            #                пробуем выполнить действие
                return fun(*args, **kwargs)
            #            если не залогинены в админку, то
            except NotLoggedInException:
                # если у объекта-хозяина (L2AdminFacade) есть свойство support, будем использовать его.
                if hasattr(args[0], 'support') and args[0].support is not None:
                    support = args[0].support
                else:
                    raise InternalException(message="Support is not defined!")

                    #            логинимся
                login_page = Page(support, PageType.LOGIN_PAGE)
                try:
                    login_page.get()
                except LoginException as er:
                #                    print("Could not log in L2Admin. Check your params")
                    raise er
                else:
                # пробуем еще раз получить страницу
                    return fun(*args, **kwargs)

        return inner

    return outer

#==================================================================================

class L2AdminFacade():
    logger = None
    support = None

    def __init__(self, support):
        UrlCreator.setFactory(Lineage2UrlCreatorFactory())
        Adaptor.setFactory(Lineage2AdaptorFactory())
        Initializer.setFactory(Lineage2InitializerFactory())
        Receiver.setFactory(Lineage2ReceiverFactory())
        Parser.setFactory(Lineage2ParserFactory())
        Handler.setFactory(Lineage2HandlerFactory())
        self.support = support


    @log_admin()
    def loggable_operation(self, a, b):
        print( a, b)

    # gets adena count
    @tryToLoggedIn()
    def get_adena(self, serverId):
        page = Page(self.support, PageType.AMOUNT_BY_ITEM_TYPE_AND_SERVER)
        params = {
            "keyword": 57,
            "variationType": "includeVariation",
            "viewType": "amountSum",
            "search": "Search",
            "WorldId": serverId}
        amount = page.get(params)
        return amount


#l2facade = L2AdminFacade()
#print l2facade.get_adena()
