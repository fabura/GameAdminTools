from Lib.receiver.core.exceptions import InternalException
from Lib.receiver.core.factories import Factory

__author__ = 'bulat.fattahov'

class Initializer():
    InitializerFactory = None
    names = {}
    page = None

    @staticmethod
    def getInitializer(page):
        if Initializer.InitializerFactory:
            object = Initializer.InitializerFactory.getForPage(page)
            if object:
                return object
        return DefaultInitializer(page)

    def __init__(self, page):
        self.page = page

    def initPage(self, params=None):
        pass

    @staticmethod
    def setFactory(factory):
        if not isinstance(factory, Factory):
            raise InternalException('It is not a factory!')
        Initializer.InitializerFactory = factory


class DefaultInitializer(Initializer):
    def __init__(self, page):
        Initializer.__init__(self, page)
        return

    def initPage(self, params=None):
        page_handler = self.page.handler
        url = page_handler.urlCreator.createUrl(params)
        page_string = page_handler.receiver.receive(url, params)
        page_handler.parser.parse(page_string)
        return


class WithoutInitialization(Initializer):
    def __init__(self, page):
        Initializer.__init__(self, page)
        return

    def initPage(self, params=None):
        return
