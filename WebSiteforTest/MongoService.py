# -*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

class MongoService(object):
    def __init__(self):
        conn = MongoClient("localhost", 27017)
        self.db = conn["webSite"]

    def getArticles(self, id):
        cursor = self.db.articles
        cursor_doc = cursor.find_one({"id":int(id)})
        if cursor_doc:
            del cursor_doc["_id"]
            return cursor_doc
        else:
            cursor_doc={}
            return cursor_doc