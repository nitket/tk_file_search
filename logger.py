import logging
class Logger:
    __instance = None
    def __init__(self):
        logging.basicConfig(filename='app_oop.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    def __new__(self):
        if self.__instance is None:
            self.__instance = object.__new__(self)
        return self.__instance
    
    def log(self,log_type,message):
        getattr(logging,log_type)(message)
