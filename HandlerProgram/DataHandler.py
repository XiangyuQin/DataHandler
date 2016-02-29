# -*- coding:utf-8 -*-

'''
    writer:XiangyuQIn
'''
import config
import common
import re
import datetime
from MysqlService import MysqlService
from RedisService import RedisService

class Application(object):
    '''Application Class handlerData from Spider
    
    handle content:replace image url,statistics the number of image, merge article and cover
    
    Attributes:
        factors:dict,record data while calculating what kinds of articles we need
        images:loading from spider-for-images, using these images for covers of articles
        cotentImages:save images which regex from articles
        now:The program starts running time
    '''
    
    def __init__(self):
        self.factors={}
        self.images=[]
        self.contentImages=[]
        self.now=datetime.datetime.now()

    def run(self):
        articles=self.loadData()
        if (articles!=None or len(articles)>0):
            processedArticles=self.handleArticles(articles)
            self.outputData(processedArticles)


    def loadData(self):
        '''load datas from mysql and redis
        
        load factors from last turn
        load articles from spider-for-PUA
        load images from spider-for-Images
    
        returns:
            qualifiedArticles:the program is going to handle these program
        '''
        
        self.factors=self.loadFactors()
        articles=self.loadArticles(self.factors['time'])
        qualifiedArticles,num=self.articlesFilter(articles, self.factors)
        self.images=self.loadImages(num)
        return qualifiedArticles
        
    def loadArticles(self, time):
        strTime = self.checkTime(time)
        service = MysqlService()
        articles = service.getArticles(strTime)
        return articles

    def checkTime(self, time):
        '''check time format
        
        args:
            time: time in factors

        returns:
            qualifiedArticles:the program is going to handle these program
        '''
        
        if isinstance(time, str):
            return time
        else:
            return "1970-01-17"
        
    def loadFactors(self):
        service = RedisService()
        factors = service.getFactors()
        return factors
    
    def articlesFilter(self, articles, factors):
        '''filte useless articles
        
        args:
            time: time in factors

        returns:
            qualifiedArticles:the program is going to handle these program
        '''
        
        qualifiedArticles=articles
        return qualifiedArticles, len(qualifiedArticles)
        
    def loadImages(self, num):
        service = MysqlService()
        images = service.getImages(num)
        return images
    
    def handleArticles(self, articles):
        processedArticles=[]
        imgs=list(self.images)
        for article in articles:
            article = self.mergeCover(article, imgs)
            processedArticles.append(self.handleArticle(article))
        return processedArticles


    def mergeCover(self, article, imgs):
        if len(imgs)>0:
            article["image"]=imgs[0]["src"]
            imgs[0]["ifused"]=1
            del imgs[0]
        else:
            print "len(imgs): %d" %(len(imgs))
            article["image"]="/static/images/website.jpg"
        return article
        
    def handleArticle(self, article):
        article['content'], article['imageNum'], article['sumImageNum']=self.handleImageInContent(article['content'], article['url'])
        return article
    
    def handleImageInContent(self, content, source):
        '''handle Image Content
        
        main process include:
        a.get rid of '<a />' in content
        b.get rid of ads at the end of the article
        c. regex image in articles,record those images, then replace thoses urls by new urls
        
        args:
            content: article content
            source: article url
            
        returns:
            result: handled content
            numImg: the number of images analysis have been resolved
            sumImag:the number of images include the images can not be resolved and external link images
        '''
        
        result, number=self.regexSubn(content, r'<a href=".+?" target="_blank">', "")
        result, numImg, sumImg=self.regexMethodImage(result, r'<img.+?/>', source)
        result, number=self.regexSubn(result, r'-{3,}[\s\S]+-{3,}[\s\S]+</tbody>', "</tbody>")
        result, numberSpecial=self.regexSubn(result, r"'", "\\'")
        print "special char number: %s" %(numberSpecial)
        return result, numImg, sumImg
    
    def handleImages(self, images):
        return []
        
    def regexSubn(self, content, regex, alternative):
        reobj = re.compile(regex)
        result, number = reobj.subn(alternative, content)
        return  result, number
        
    def regexGroup(self, content, regex):
        m = re.search(regex, content,re.M|re.I)
        if m!=None:
            return m.groups()
        else:
            return ()
        
    def regexMethodImage(self, content, regex, source):
        '''handle Content to collect <img …… /> ,result 
        
        args:
            content: article content
            regex: regex for <img …… />
            source: article url
            
        returns:
            result: handled content
            regexImagesCount: the number of images analysis have been resolved
            len(images):the number of images include the images can not be resolved and external link images
        '''
        
        reobj = re.compile(regex)
        images=reobj.findall(content)
        subnImages, regexImagesCount = self.generateConImgsAndSubnImgs(images, source)
        result = content
        for (name, newUrl) in subnImages.items():
            image_regex = r'<img.+%s.+?/>' % (name)
            result, num=self.regexSubn(result, image_regex, newUrl)
            #print "source:%s;num:%d" %(source,num)
        #print "images:%s,regex_images:%d" %(len(images),regexImagesCount)
        return  result, regexImagesCount, len(images)
        
    def generateConImgsAndSubnImgs(self, images, source):
        '''handle <img …… />
        
        args:
            images: list of <img …… />
            source: article url
            
        returns:
            subnImages: list of handled images, which its type is dict,key:image name;value:image <img ……/>
            regexImagesCount:the number of images which having been resolved
        '''
        
        subnImages={}
        numImg=0
        regexImagesCount=0
        for image in images:
            image, num=self.regexSubn(image, r'static/image/common/none\.gif', "static/images/common/none.gif")
            groups=self.regexGroup(image, r'((data/attachment/forum/)\d*/\d*/(.+?\.\w{3,4}))')
            if groups!=None and len(groups)>2:
                newUrl="static/images/"+groups[2]
                subnImage, numImg = self.regexSubn(image, r'((data/attachment/forum/)\d*/\d*/(.+?\.\w{3,4}))', newUrl)
                subnImages[groups[2]]=subnImage
                contentImage = self.generateContentImage(groups, source)
                #handle images save in content
                self.contentImages.append(contentImage)
                regexImagesCount = regexImagesCount + 1
        return subnImages, regexImagesCount
    
    def generateContentImage(self, groups, source):
        ContentImage={}
        ContentImage["url"]=groups[0]
        ContentImage["type"]=2
        ContentImage["src"]="static/images/"+groups[2]
        ContentImage["sourceArticles"]=source
        ContentImage["ifused"]=1
        ContentImage["ifdown"]=0
        ContentImage["createtime"]=self.now
        return ContentImage
        
        
    def outputData(self, articles):
        redisArticles=self.generateRedisArticles(articles)
        self.factors['time']=self.getLastestDate(articles)
        self.markUsingImages()
        self.outputByRedis(redisArticles)
        self.outputByMysql(articles)
        self.outputFactors()
        '''
        print "images: %s" %(str(self.images))
        print "contentImages: %s" %(str(self.contentImages))
        print "redisArticles:%s" %(str(redisArticles))
        '''

    def getLastestDate(self, articles):
        lastest = common.string_toDatetime(self.factors["time"])
        print type(lastest)
        lastestDateTime = datetime.datetime(*lastest[0:6])
        lastestDate = common.date_toTimestamp(lastestDateTime)
        for article in articles:
            date=common.date_toTimestamp(article['editdate'])
            print date
            if (date > lastestDate):
                lastestDate = date
        lastestDatetime = common.timestamp_toDate(lastestDate)
        return lastestDatetime
        
    def markUsingImages(self):
        self.markCover(self.images)
        self.markContentImages(self.contentImages)
            
    def markCover(self, images):
        '''mark cover image in mysql, change ifused value, ifused=1
        
        '''
        try:
            service = MysqlService()
            service.updateImages(images)
            return True
        except Exception as e:
            print "markCover error: '%s'" %(e)
            return False
    
    def markContentImages(self, images):
        '''save content image in mysql, ifused=1
            
        '''
        try:
            service = MysqlService()
            service.setImages(images)
            return True
        except Exception as e:
            print "markContentImages error: '%s'" %(e)
            return False

    def generateRedisArticles(self, articles):
        redisArticles=[]
        for article in articles:
            redisArticle=self.generateRedisArticle(article)
            redisArticles.append(redisArticle)
        return redisArticles
            
    def generateRedisArticle(self, article):
        redisArticle={}
        redisArticle["id"]=article["id"]
        redisArticle["url"]=article["url"]
        redisArticle["editdate"]=article["editdate"]
        redisArticle["level"]=0
        redisArticle["len"]=len(article["content"])
        redisArticle["ctr"]=0
        redisArticle["pn"]=0
        redisArticle["pv"]=0
        redisArticle["image"]=article["imageNum"]
        redisArticle["sumImage"]=article["sumImageNum"]
        return redisArticle
        
    def outputByRedis(self, articles):
        try:
            service = RedisService()
            return service.hsetArticles(articles)
        except Exception as e:
            print "outputByRedis error: '%s'" %(e)
            return False  
        
    def outputByMysql(self, articles):
        try:
            service = MysqlService()
            service.setArticles(articles)
            return True
        except Exception as e:
            print "outputByMysql error: '%s'" %(e)
            return False
    
    def outputFactors(self):
        try:
            service = RedisService()
            service.setFactors(self.factors)
            return True
        except Exception as e:
            print "outputFactors error: '%s'" %(e)
            return False
	
if __name__ == '__main__':
    application = Application()
    application.run()
