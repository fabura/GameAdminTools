# coding=utf-8
from receiver.lineage2.pageTypes import PageType
from receiver.lineage2.urlCreators import ListLogUrlCreator

__author__ = 'bulat.fattahov'
import sys
import receiver.core.handlers
from receiver.core.factories import FromDictFactory


class Lineage2HandlerFactory(FromDictFactory):
    names = {PageType.LIST_LOG: 'Lineage2ListLogHandler'}

    # where we will look for handlers: in defaults and in this file
    whereToSeek = [receiver.core.handlers,
                   sys.modules[__name__]]

#=====================================================


class Lineage2ListLogHandler(receiver.core.handlers.DefaultHandler):
    LOGS_BY_PAGE = 500

    def __init__(self, page):
        receiver.core.handlers.DefaultHandler.__init__(self, page)

    def handle(self, par=None, callbacks=None):
        #        инициализация страницы
        params = par
        init_info = self.initializer.initPage(params)
        result = []
        if callbacks and ('filter' in callbacks):
            filter = callbacks['filter']
        index = 0
        while True:
            index += 1
            last_count = 0
            #        получить параметры для передачи на страницу
            adapted_params = self.adaptor.adapt(params)
            params['page_number'] = index
            url = self.urlCreator.createUrl(params)
            page_string = self.receiver.receive(url, adapted_params)
            temp_result = self.parser.parse(page_string)
            self.urlCreator.setNaviUrl(self.parser.naviUrl)
            last_count = len(result)
            if 'filter' in locals():
                result += filter(temp_result)
            else:
                result += temp_result
            if last_count != self.LOGS_BY_PAGE:
                break
        return result
