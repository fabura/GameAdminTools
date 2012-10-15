# coding=utf-8
__author__ = 'bulat.fattahov'

def log_admin(log_text=None):
    '''
     Используется для логгирования действий админа.
     Объект-хозяин декорируемой функции должен иметь свойство   logger, иначе применяется logger по умолчанию.
     Декоратор может принимать строку, которая будет выдавать в лог, если строка пустая или ее нет, то будет записываться
     название декорируемой функции
    '''
    def outer(fun):
        def inner(*args, **kwargs):
            if hasattr(args[0], 'logger') and args[0].logger is not None:
                logger = args[0].logger
            else:
                logger = SimpleLogger()

            if logger is not None:
                if not log_text:
                    log = fun.__name__
                else:
                    log = log_text

                #log before
                if hasattr(logger, 'log_start'):
                    logger.log_start(log, (args, kwargs))

                result = fun(*args, **kwargs)
                # log after
                if hasattr(logger, 'log_end'):
                    logger.log_end(log, (args, kwargs), result)
                return result
            else:
                return fun(*args, **kwargs)
        return inner
    return outer

class SimpleLogger():

    def log_start(self, log_text, *args, **kwargs):
        print log_text

#    def log_end(self, log_text):
#        print log_text
