#!/usr/bin/python

import json
import urllib2
import urllib

fileName = "searchTerms2.txt"

def getYouTubeLinkFromJson(youTubeSearchJson):
    data = json.load(youTubeSearchJson)

    contentDict = data["feed"]["entry"][0]["media$group"]["media$content"]

    url = ""
    for mediaDict in contentDict:
        if mediaDict["type"] == "application/x-shockwave-flash":
            url = mediaDict["url"]
            break
    return url

def getSearchTermListFromFile():
    searchTerms = []
    with open(fileName) as f:
        for line in f:
            searchTerms.append(line.strip())

    return searchTerms

def printHtmlFile(termTuple):
    beginHtml = "<html><body>"
    itemHtml = """
        <h2>{0}</h2>
        <iframe width="420" height="315" src="{1}" frameborder="0" allowfullscreen></iframe>
    """
    endhtml = "</body></html>"

    with open("index.html", 'w') as f:
        f.write(beginHtml)
        for item in termTuple:
            f.write(itemHtml.format(urllib.unquote(item[0]), item[1]))
        f.write(endhtml)

def main():
    searchTerms = getSearchTermListFromFile()

    baseUrl = "https://gdata.youtube.com/feeds/api/videos?q={0}&v=2&alt=json&max-results=1"
    termTuple = []
    for term in searchTerms:
        url = baseUrl.format(urllib.quote_plus(term))
        ytJson = urllib2.urlopen(url)
        videoLink = getYouTubeLinkFromJson(ytJson)
        termTuple.append((term, videoLink))
        
    printHtmlFile(termTuple)


main()
