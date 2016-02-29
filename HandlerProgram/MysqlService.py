# -*- coding: UTF-8 -*-

import MySQLdb
import common
import config
import MySQLdb.cursors

class MysqlService(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost","root", "qinxiangyu", "spider",charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)

    def getArticles(self, date):
        cursor = self.db.cursor()
        sql = "select *,COUNT(distinct title) AS disItem from puahome_bbs WHERE Date(editdate) > '%s' GROUP BY title order by Date(editdate) desc" % (date)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                print common.datetime_toString(row['editdate'])
            return results
        except Exception as e:
            print "getArticles: %s" % (e)
            return []
    
    def getImages(self, num):
        cursor = self.db.cursor()
        sql = "select *,COUNT(distinct url) AS disItem from images WHERE ifused = 0 AND ifdown > 0 GROUP BY url order by createdate asc limit %d" % (num)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print "getImages: %s" % (e)
            return []
            
    def setArticles(self, articles):
        cursor = self.db.cursor()
        sql_test=""
        try:
            for article in articles:
                sql="INSERT INTO articles(id, \
                title, url, image, date, type_id, writer, content) \
                VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (article['id'], article['title'], article['url'], article['image'], article['editdate'], config.defaultTypeId, article['writer'], article['content'])
                sql_test=sql
                cursor.execute(sql)
                self.db.commit()
            return True
        except Exception as e:
            print "setArticles: %s" % (e)
            print "sql: %s" % (sql_test)
            return False
            
    def updateImages(self, images):
        cursor = self.db.cursor()
        try:
            for image in images:
                sql="UPDATE images SET ifused = '%d' \
                          WHERE id = '%d'" % (image['ifused'], image['id'])
                cursor.execute(sql)
                self.db.commit()
            return True
        except Exception as e:
            print "updateImages: %s" % (e)
            return False
    
    def setImages(self, images):
        cursor = self.db.cursor()
        try:
            for image in images:
                sql="INSERT INTO images(\
                url, src, type, sourceArticles, ifused, ifdown) \
                VALUES ('%s', '%s', '%s', '%s', '%d', '%d')" % \
                (image['url'], image['src'], image['type'], image['sourceArticles'], image['ifused'], image['ifdown'])
                cursor.execute(sql)
                self.db.commit()
            return True
        except Exception as e:
            print "setImages: %s" % (e)
            return False
            
    def closeDb(self):
        self.db.close()
    

if __name__ == '__main__':
    service = MysqlService()
    article1={'id':1,"title":"示例文章","url":"www.baiu.com", "image":"/status/image/hello.jpg","date":"2016-02-17","brief":"和咯","type_id":"1","writer":"hello","content":"合理"}
    article2={'id':2,"title":"示例文章","url":"www.baiu.com", "image":"/status/image/hello.jpg","date":"2016-02-17","brief":"和咯","type_id":"1","writer":"hello","content":"合理"}
    articles=[]
    articles.append(article1)
    articles.append(article2)
    image1={"id":1,"url":"www.baidu.com","src":"/status/images/hello.jpg","type":1,"sourceArticles":1,"ifused":1,"ifdown":1}
    image2={"id":2,"url":"www.baidu.com","src":"/status/images/hello.jpg","type":1,"sourceArticles":1,"ifused":2,"ifdown":1}
    images=[]
    images.append(image1)
    images.append(image2)
    print service.getImages()
    '''
    if service.setArticles(articles):
        print "setArticles ok"
    if service.updateImages(images):
        print "setImages ok"
    '''