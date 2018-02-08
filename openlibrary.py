#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    Simple openlibrary API to search for books by ISBN number
"""

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import sys
from string import Template
from book import Book

isbn_query=Template('http://openlibrary.org/api/things?query={"type":"/type/edition","$isbnkey":"$isbn"}')
get_query='http://openlibrary.org/api/get?key='
cover_query_url="http://covers.openlibrary.org/b/{}/{}-{}.jpg"

def _get_json(url):
    print("Fetching " + url)
    page = urlopen(url).read().decode('utf-8', 'ignore')
    return json.loads(page,encoding="utf-8")

def _is_isbn13(isbn):
    return len(isbn.strip().replace("-",'')) > 10
    
def _search_by_isbn(isbn):
    print("Searching for isbn " + isbn + " in openlibrary...")
    isbn = isbn.replace("-","")
    isbnkey = "isbn_13"
    if len(isbn) < 13:
        isbnkey = "isbn_10"
    url = isbn_query.substitute(isbnkey=isbnkey,isbn=isbn)
    j = _get_json(url)
    if j["status"] != "ok":
        return None
        
    result = j["result"]
    if not result or len(result) < 1:
        return None
     
    bookid = j["result"][0]
    
    # returns /books/OL3315616M
    return bookid

def _get_bookurl(id):
    return get_query + id
    
def _get_info(id):
    return _get_json(_get_bookurl(id))
    
def _get_book_cover_url(book_id):
    """
        Get book cover URL
    """
    size = "L" # M, S
    key = "OLID"
    value = book_id[7:]
    return cover_query_url.format(key,value,size)

def _item2book(json_item,isbn):
    b = Book()
    b.service = "openlibrary"
    
    bookid = _search_by_isbn(isbn)
    b.bookid = bookid
    b.bookurl = _get_bookurl(bookid)

    bookresult = json_item["result"]
    if "title" in bookresult:
        b.title = bookresult["title"]
    if "subtitle" in bookresult:
        b.subtitle = bookresult["subtitle"]
    if "publish_date" in bookresult:
        b.publishdate = bookresult["publish_date"]
    if "publishers" in bookresult:
        b.publisher = bookresult["publishers"][0]
    if "number_of_pages" in bookresult:
        b.pages = bookresult["number_of_pages"]
    if "authors" in bookresult:
        authorkey =  bookresult["authors"][0]["key"]
        b.author = _get_info(authorkey)["result"]["name"]
    if "covers" in bookresult:
        b.imgurl = _get_book_cover_url(bookid)
    if "isbn_10" in bookresult:
        b.isbn_10 = bookresult["isbn_10"][0]
    if "isbn_13" in bookresult:
        b.isbn_13 = bookresult["isbn_13"][0]
    if "description" in bookresult:
        d = bookresult["description"]
        if "value" in d:
            b.description = d["value"]
    return b
    
def searchbook(isbn):
    """
        Search for book by ISDN number (10,13 based)
    """

    bookid = _search_by_isbn(isbn)
    if not bookid:
        return None

    # set book fields
    
    bookinfo = _get_info(bookid)
    if not bookinfo:
        return None
    
    b = _item2book(bookinfo,isbn)
    b.set_isbn(isbn)                
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
