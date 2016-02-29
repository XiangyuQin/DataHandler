# -*- coding:utf-8 -*-
import tornado.web
import config
from MongoService import MongoService
import testData
import re

class ArticleHandler(tornado.web.RequestHandler):
    def get(self, input):
        articleId=input[::1]
        article=self.getArticle(articleId)
		
        regex=r'<a href=".*?" target="_blank">'
        newstring=""
        reobj = re.compile(regex)
        result, number = reobj.subn(newstring, testData.article)
		
        regex_img=r'<img.*src=".*" .*?/>'
        newstring_img="<img src=\"/static/images/12420c1.jpg\" alt=\"12420c1\" width=\"210\"/>"
        reobj_img = re.compile(regex_img)
        result_img, number_img = reobj_img.subn(newstring_img, result)
		
        regex_end=r'-{3,}[\s\S]*-{3,}[\s\S]*</tbody>'
        newstring_end="</tbody>"
        reobj_end = re.compile(regex_end)
        result_end, number_end = reobj_end.subn(newstring_end, result_img)
		
        article['content']=tornado.escape.xhtml_unescape(result_end)
        self.render(
            "article.html",
            article=article,
        )
    def getArticle(self, articleId):
        mongoService = MongoService()
        article = mongoService.getArticles(articleId)
        return article