from Lib.receiver.core.exceptions import InternalException
from Lib.receiver.core.factories import Factory

__author__ = 'bulat.fattahov'

class Adaptor():
    AdaptorFactory = None
    names = {}
    factory = None
    page = None

    @staticmethod
    def getAdaptor(page):
        if Adaptor.AdaptorFactory:
            object = Adaptor.AdaptorFactory.getForPage(page)
            if object:
                return object
        return DefaultAdaptor(page)

    def adapt(self, params=None):
        return {}

    def __init__(self, page):
        self.page = page
        return

    @staticmethod
    def setFactory(factory):
        if not isinstance(factory, Factory):
            raise InternalException('It is not a factory!')
        Adaptor.AdaptorFactory = factory


#=====================================================
class DefaultAdaptor(Adaptor):
    def __init__(self, page):
        Adaptor.__init__(self, page)

    def adapt(self, params=None):
        result = Adaptor.adapt(self, params)
        if params:
            for k in params.keys(): result[k] = params[k]
        result['__VIEWSTATE'] = self.page.getViewState()
        result['actionKey'] = self.page.getActionKey()
        return result

#=====================================================
class WithoutInitializationAdaptor(Adaptor):
    def adapt(self, params=None):
        if params:
            copy = params.copy()
            if 'url' in copy: del copy['url']
            return  copy
        return params