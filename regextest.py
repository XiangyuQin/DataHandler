# -*- coding: UTF-8 -*-
import re
import config
class regexText(object):
    def __init__(self):
        self.contentImages=[]
        self.now=0
        pass
        
    def handleContent(self, content, source):
        result, number=self.regexSubn(content, r'<a href=".+?" target="_blank">', "")
        result, numberImgs=self.regexMethodImage(result, r'<img.+src=".+" .+/>', source)
        finalResult, number=self.regexSubn(result, r'-{3,}[\s\S]+-{3,}[\s\S]+</tbody>', "</tbody>")
        print numberImgs
        return finalResult
    
    def handleImages(self, images):
        return []
        
    def regexSubn(self, content, regex, alternative):
        reobj = re.compile(regex)
        result, number = reobj.subn(alternative, content)
        return  result, number
        
    def regexGroup(self, content, regex):
        m = re.search(regex, content,re.M|re.I)
        print m.groups()
        return m.groups()
        
    def regexMethodImage(self, content, regex, source):
        reobj = re.compile(regex)
        images=reobj.findall(content)
        subnImages = self.generateConImgsAndSubnImgs(images, source)
        print len(subnImages)
        result = content
        for (name, newUrl) in subnImages.items():
            image_regex = r'<img.+src=".+".+%s.+/>' % (name)
            result=self.regexSubn(result, image_regex, newUrl)
        return  result
        
    def generateConImgsAndSubnImgs(self, images, source):
        subnImages={}
        for image in images:
            image, num=self.regexSubn(image, r'static/image/common/none\.gif', "static/images/common/none.gif")
            groups=self.regexGroup(image, r'((data/attachment/forum/)\d*/\d*/(.+?\.jpg))')
            newUrl="static/images/"+groups[2]
            subnImage, num = self.regexSubn(image, r'((data/attachment/forum/)\d*/\d*/(.+?\.jpg))', newUrl)
            subnImages[groups[2]]=subnImage
            contentImage = self.generateContentImage(groups, source)
            self.contentImages.append(contentImage)
        return subnImages
    
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
        
    
    def regexNoneGif(self, image):
        pass
        

if __name__ == '__main__':
    
    regextext = regexText()
    regextext.handleContent(config.content, "www.baidu.com")