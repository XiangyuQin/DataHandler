#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","root", "qinxiangyu", "spider",charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM puahome_bbs"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   count=0
   for row in results:
      # 打印结果
      if(count==0):
          print row[3]
          count=count+1
except:
   print "Error: unable to fecth data"

# 关闭数据库连接
db.close()