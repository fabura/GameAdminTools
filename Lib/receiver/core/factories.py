from Lib.receiver.core.exceptions import InternalException

__author__ = 'bulat.fattahov'


class Factory():
    def getForPage(self, page):
        return None

class FromDictFactory(Factory):
    names = {}
    whereToSeek = []

    def getForPage(self, page):
        Factory.getForPage(self, page)

    def getForPage(self, page):
        Factory.getForPage(self, page)
        pageName = page.pageName
        if pageName in self.names.keys():
            class_name = self.names[pageName]

            if not self.whereToSeek:
                raise InternalException(message= 'WhereToSeek is not defined!')

            for module in self.whereToSeek:
                try:
                    object = getattr(module, class_name)(page)
                except:
                    continue
                else:
                    return object
            raise InternalException(message= class_name +' is not found in ' + self.whereToSeek)
        return None