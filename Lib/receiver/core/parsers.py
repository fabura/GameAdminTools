# coding=utf-8
__author__ = 'bulat.fattahov'
from Lib.receiver.core.exceptions import InternalException
from Lib.receiver.core.factories import Factory


class Parser():
    ParserFactory = None
    names = {}
    page = None
    lxmldoc = None

    @staticmethod
    def getParser(page):
        if Parser.ParserFactory:
            object = Parser.ParserFactory.getForPage(page)
            if object:
                return object
        return DefaultParser(page)

    def parse(self, page_str):
        pass

    def __init__(self, page):
        self.page = page
        self.lxmldoc = None
        return

    @staticmethod
    def setFactory(factory):
        if not isinstance(factory, Factory):
            raise InternalException('It is not a factory!')
        Parser.ParserFactory = factory


class DefaultParser(Parser):
    def __init__(self, page):
        Parser.__init__(self, page)

    #по умолчанию просто возвращаем страницу
    def parse(self, page_str):
        Parser.parse(self, page_str)
        return page_str




