import logging

class logs:
    def __init__(self) -> None:
        logging.basicConfig(filename="logs.log",  
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',  
                    filemode='a')  
        
        self.logger=logging.getLogger()     
        self.logger.setLevel(logging.DEBUG) 

    def debug(self, msg):
        self.logger.debug(msg)  

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
  