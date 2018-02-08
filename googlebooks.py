#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Simple googlebooks API to search for books by ISBN number
"""

import json
import urllib
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    
from book import Book
import sys

__BASE__ = "https://www.googleapis.com/books/v1/volumes?"
__ISBNQUERY__=__BASE__ + "prettyPrint=true&maxResults=1&printType=books&q=isbn:"
__TITLEQUERY__= __BASE__ + "prettyPrint=true&q=intitle:"

def loadjson(url):
    print("Use url "+url)
    x = urlopen(url)
    return json.loads(x.read())
    
def _getbookurl(isbn):
    return __ISBNQUERY__ + isbn
    
def _search_by_isbn(isbn):
    return loadjson(__ISBNQUERY__ + isbn)

def _search_by_title(title):
    return loadjson(__TITLEQUERY__ + urllib.quote(title))

def _parseisbn(isbn):
    return isbn.strip().replace("-","")

def _item2book(json_item):
    bookid = json_item["id"]
    info = json_item["volumeInfo"]

    b = Book()
    b.bookid = bookid
    b.bookurl = json_item["selfLink"]
    b.service = "googlebooks"
    
    if "title" in info:
        b.title = info["title"]
    if "description" in info:
        b.description = info["description"]
    if "publisher" in info:
        b.publisher = info["publisher"]
    if "publishedDate" in info:
        b.publishdate = info["publishedDate"]
    if "pageCount" in info:
        b.pages = info["pageCount"]
    if "authors" in info and len(info["authors"]) > 0:
        b.author = info["authors"][0]
    if "imageLinks" in info:
        b.imgurl = info["imageLinks"]["thumbnail"]
    if "industryIdentifiers" in info:
        for ii in info["industryIdentifiers"]:
            t = ii["type"]
            id = ii["identifier"]
            if t == "ISBN_10":
                b.isbn_10 = id
            if t == "ISBN_13":
                b.isbn_13 = id
                
    return b

def search_title(title):
    jzon = _search_by_title(title)
    books = []
    if jzon["totalItems"] == 0:
        return books
    
    for item in  jzon["items"]:
        b = _item2book(item)
        books.append(b)
        
    return books
    
    
    
def searchbook(isbn):
    """
        Search for a book by ISBN number 
    """
    print("Searching for isbn " + isbn + " in googlebooks...")
    result = _search_by_isbn(isbn)
    
    if result["totalItems"] == 0:
        return None
    
    b = _item2book(result["items"][0])
    return b

def main():
    isbn = sys.argv[1]
    b = searchbook(isbn)
    if not b:
        print ("Not found")
    else:
        print ("Found " + str(b))
    
if __name__ == "__main__":
    main()