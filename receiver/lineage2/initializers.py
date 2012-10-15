__author__ = 'bulat.fattahov'
import sys
import receiver.core.initializers
from receiver.core.factories import FromDictFactory
from receiver.lineage2.pageTypes import PageType


class Lineage2InitializerFactory(FromDictFactory):
    names = {PageType.PAGE_WITHOUT_INITIALIZATION : "WithoutInitialization"}

    # where we will look for initializers: in defaults and in this file
    whereToSeek = [receiver.core.initializers,
                   sys.modules[__name__]]

#=====================================================

