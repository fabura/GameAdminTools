# coding=utf-8
from receiver.core.adaptors import Adaptor
from receiver.core.exceptions import InternalException
from receiver.core.factories import Factory
from receiver.core.initializers import Initializer
from receiver.core.parsers import Parser
from receiver.core.receivers import  Receiver
from receiver.core.urlCreators import UrlCreator

__author__ = 'bulat.fattahov'


class Handler:
    HandlerFactory = None
    names = {}
    page = None
    initializer = None
    urlCreator = None
    adaptor = None
    receiver = None
    parser = None
    pageName = None

    def handle(self, params=None):
        pass

    def __init__(self, page):
        self.page = page

    @staticmethod
    def getHandler(page):
        if Handler.HandlerFactory:
            object = Handler.HandlerFactory.getForPage(page)
            if object:
                return object
        return DefaultHandler(page)

    @staticmethod
    def setFactory(factory):
        if not isinstance(factory, Factory):
            raise InternalException('It is not a factory!')
        Handler.HandlerFactory = factory



class DefaultHandler(Handler):
    def __init__(self, page):
        Handler.__init__(self, page)
        self.initializer = Initializer.getInitializer(page)
        self.adaptor = Adaptor.getAdaptor(page)
        self.urlCreator = UrlCreator.getUrlCreator(page)
        self.receiver = Receiver.getReceiver(page)
        self.parser = Parser.getParser(page)


    def handle(self, params=None):
        #        инициализация страницы
        init_info = self.initializer.initPage(params)
        #        получить параметры для передачи на страницу
        adapted_params = self.adaptor.adapt(params)
        #        создать подходящую урлу
        url = self.urlCreator.createUrl(params)
        #        пробуем получить страницу
        page_string = self.receiver.receive(url, adapted_params)
        #        если кидает на страницу релога
        result = self.parser.parse(page_string)
        return result