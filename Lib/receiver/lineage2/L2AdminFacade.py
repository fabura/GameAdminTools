from Lib.receiver.core.decorators.log_admin import log_admin

__author__ = 'bulat.fattahov'

class L2AdminFacade():
    logger = None

    @log_admin()
    def loggable_operation(self, a, b):
        print( a, b)

#
l2Admin = L2AdminFacade()
l2Admin.loggable_operation(4,5)