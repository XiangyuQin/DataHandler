# -*- coding: UTF-8 -*-

import datetime
import logging
from logging.handlers import RotatingFileHandler

class Log(object):
    def __init__(self):
        dt = datetime.datetime.now()
        now = dt.strftime("%Y%m%d%H%M%S")
        file_name = 'myapp%s.log' %(now)
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=file_name,
                filemode='w')
        Rthandler = RotatingFileHandler(app_name, maxBytes=10*1024*1024,backupCount=5)
        Rthandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        Rthandler.setFormatter(formatter)
        logging.getLogger('').addHandler(Rthandler)
    
    def test(self):
        for i in range(1, 10):
            logging.debug('This is debug message')

    
if __name__ == '__main__':
    logTest=LogTest()
    logTest.test()