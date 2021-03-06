#!/usr/bin/python

import json
import urllib2
import urllib
import cgi;
import cgitb; cgitb.enable()

fileName = "tmp.txt"

def getYouTubeLinkFromJson(youTubeSearchJson):
    data = json.load(youTubeSearchJson)

    url = ""

    if "entry" in data["feed"]:
        contentDict = data["feed"]["entry"][0]["media$group"]["media$content"]

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

def getSearchTermListFromInput(formInput):
    searchTerms = []
    lines = [s.strip() for s in formInput.splitlines()]
    for line in lines:
        searchTerms.append(line)

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
            f.write(itemHtml.format(item[0], item[1]))
        f.write(endhtml)

def printAjaxHtml(termTuple):
    #print("Content-Type: text/html")
    #print # blank line, end of header
    itemHtml = """
        <h2>{0}</h2>
        <iframe width="420" height="315" src="{1}" frameborder="0" allowfullscreen></iframe>
    """
    noResultHtml = """
        <h2>{0}</h2>
        <h3>No Result found for search term</h3>
    """
    for item in termTuple:
        if len(item[1].strip()) > 0:
            print(itemHtml.format(item[0], item[1]))
        else:
            print(noResultHtml.format(item[0]))
    

def main():
    form = cgi.FieldStorage()
    searchInput = form.getvalue("searchTerms")
    if searchInput:
        searchTerms = getSearchTermListFromInput(searchInput)
    else:
        searchTerms = getSearchTermListFromFile()

    baseUrl = "https://gdata.youtube.com/feeds/api/videos?q={0}&v=2&alt=json&max-results=1"
    termTuple = []
    for term in searchTerms:
        url = baseUrl.format(urllib.quote_plus(term))
        ytJson = urllib2.urlopen(url)
        videoLink = getYouTubeLinkFromJson(ytJson)
        termTuple.append((term, videoLink))
        
    #printHtmlFile(termTuple)
    printAjaxHtml(termTuple)


main()
