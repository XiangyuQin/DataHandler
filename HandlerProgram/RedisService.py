# -*- coding: UTF-8 -*-
import redis
import common

class RedisService(object):
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        

    def getFactors(self):
        factors = self.r.hgetall('factors')
        return factors
    
    def setFactors(self, factors):
        try:
            print factors["time"]
            time = common.datetime_toString(factors["time"])
            factors = self.r.hset('factors', 'time' , time)
        except Exception as e:
            print "setFactors: %s" % (e)
        
    def hsetArticles(self, articles):
        try:
            for article in articles:
                self.r.hset('articles', article['id'], article)
            return True
        except Exception as e:
            print "hsetArticles: %s" % (e)
            return False
            


if __name__ == '__main__':
    service = RedisService()
    factor={"time":"2016-02-22"}
    service.setFactors(factor)
    factors = service.getFactors()
    print factors
    article={'id':1, 'url':'www.baidu.com','src':'/status/images/website1.jpg', 'type':1,'sourceArticles':'www.qq.com','ifused':1,'ifdown':1 }
    articles=[]
    articles.append(article)
    service.hsetArticles(articles)