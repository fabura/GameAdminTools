import urllib
from receiver.core.exceptions import InternalException
from receiver.core.factories import Factory

__author__ = 'bulat.fattahov'


class UrlCreator():
    UrlCreatorFactory = None
    urlNameMap = { }

    page = None

    @staticmethod
    def getUrlCreator(page):
        if UrlCreator.UrlCreatorFactory:
            object = UrlCreator.UrlCreatorFactory.getForPage(page)
            if object:
                return object
        return DefaultUrlCreator(page)

    def createUrl(self, params):
        url = self.page.support.getBaseUrl()
        if self.urlNameMap[self.page.pageName]:
            url += self.urlNameMap[self.page.pageName]
        return url

    def __init__(self, page):
        self.page = page
        return

    @staticmethod
    def setFactory(factory):
        if not isinstance(factory, Factory):
            raise InternalException('It is not a factory!')
        UrlCreator.UrlCreatorFactory = factory


class DefaultUrlCreator(UrlCreator):
    def __init__(self, page):
        UrlCreator.__init__(self, page)

    def createUrl(self, params):
        url = UrlCreator.createUrl(self, params)
        if params:
            url += "?" + urllib.urlencode(params)
        #        url += "?" + join ((a+'='+str(params[a]) for a in params.keys()),'&')
        return url


class WithoutInitializationUrlCreator(UrlCreator):
    def __init__(self, page):
        UrlCreator.__init__(self, page)


    def createUrl(self, params):
        """
        params - dict
        """
        url = UrlCreator.createUrl(self, params)
        if params and ('url' in params):
            url += params['url']
        else:
            raise InternalException("Url is not defined!")
        return  url