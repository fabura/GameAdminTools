__author__ = 'bulat.fattahov'
import sys
import Lib.receiver.core.initializers
from Lib.receiver.core.factories import FromDictFactory
from Lib.receiver.lineage2.pageTypes import PageType


class Lineage2InitializerFactory(FromDictFactory):
    names = {PageType.PAGE_WITHOUT_INITIALIZATION : "WithoutInitialization"}

    # where we will look for initializers: in defaults and in this file
    whereToSeek = [Lib.receiver.core.initializers,
                   sys.modules[__name__]]

#=====================================================

