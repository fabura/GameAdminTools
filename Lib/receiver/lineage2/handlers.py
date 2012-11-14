# coding=utf-8
import re
from Lib.receiver.core.strategy import Page
from Lib.receiver.lineage2.pageTypes import PageType

__author__ = 'bulat.fattahov'
import sys
import Lib.receiver.core.handlers
from Lib.receiver.core.handlers import  DefaultHandler
from Lib.receiver.core.factories import FromDictFactory


class Lineage2HandlerFactory(FromDictFactory):
    names = {PageType.LIST_LOG: 'Lineage2ListLogHandler',
             PageType.APPROVE_REQUEST: "Lineage2ApproveRequestHandler",
             PageType.CHANGE_CHARACTER: "Lineage2ChangeCharacterHandler"}

    # where we will look for handlers: in defaults and in this file
    whereToSeek = [Lib.receiver.core.handlers,
                   sys.modules[__name__]]

#=====================================================


class Lineage2ListLogHandler(DefaultHandler):
    LOGS_BY_PAGE = 500

    def __init__(self, page):
        Lib.receiver.core.handlers.DefaultHandler.__init__(self, page)

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

# for change character page
class Lineage2ChangeCharacterHandler(DefaultHandler):
    def __init__(self, page):
        DefaultHandler.__init__(self, page)

    def handle(self, params=None):
        # Загружаем страницу изменения персонажа
        init_page = self.initializer.initPage(params)
        # парсим её, сохраняем предыдущие параметры чара
        previous_params = self.parser.parse(init_page)
        params["CharName"] = previous_params["CharName"]
        #  создаем подходящую урлу
        url = self.urlCreator.createUrl(params)

        self.adaptor.defaults = previous_params
        adapted_params = self.adaptor.adapt(params)
        #        пробуем получить страницу
        page_string = self.receiver.receive(url, adapted_params)
        if re.search(r"Completed character change request.", page_string):
            return True
        return False

class Lineage2ApproveRequestHandler(DefaultHandler):
    def __init__(self, page):
        DefaultHandler.__init__(self, page)

    def handle(self, params=None):
        init_page = self.initializer.initPage(params)
        url  = self.urlCreator.createUrl(params)
#        первая страница реквеста
        adapted_params = self.adaptor.adapt(params)
        page_string = self.receiver.receive(url, adapted_params)
        print(page_string)
        page2 = Page(self.page.support, PageType.APPROVE_REQUEST_SECOND)
        page2_handler = page2.handler
        page2_handler.parser.parse(page_string)
        page2_url = page2_handler.urlCreator.createUrl(params)
        page2_adapted_params = page2_handler.adaptor.adapt(params)
        return page2_handler.receiver.receive(page2_url, page2_adapted_params)