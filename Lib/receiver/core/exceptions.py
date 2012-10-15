__author__ = 'bulat.fattahov'

class PageReceiverException(BaseException):
    def __unicode__(self):
        if self.message:
            return self.message
        else:
            return __name__

    def __str__(self):
        return self.__unicode__()


class LoginException(PageReceiverException):
    message = 'Cannot log in system'


class NotLoggedInException(PageReceiverException):
    message = 'Not logged in!'


class InternalException(PageReceiverException):
    def __init__(self, message):
        self.message = message
