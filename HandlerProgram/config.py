# -*- coding: UTF-8 -*-
defaultTypeId="0"
defaultFactorsTime="1970-01-01"
defaultCoverImages="/static/images/website.jpg"
defaultIfused=1
defaultIfdown=0
defaultImagesSrc="static/images/"
defaultLevel=0
defaultCtr=0
defaultPn=0
defaultPv=0

contentImageType=2

regexA=r'<a href=".+?" target="_blank">'
regexImages=r'<img.+?/>'
regexAds=r'-{3,}[\s\S]+-{3,}[\s\S]+</tbody>'
regexSpCharSingleQuotes=r"'"
regexNoneGIf=r'static/image/common/none\.gif'
regexImagesUrl=r'((data/attachment/forum/)\d*/\d*/(.+?\.\w{3,4}))'

replacementA=""
replacementAds="</tbody>"
replacementSpCharSingleQuotes="\\'"
replacementNoneGIf="static/images/common/none.gif"

logSrc='log/'
logMaxBytes=10*1024*1024
logBackupCount=5