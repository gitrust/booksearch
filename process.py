#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import sys
import time
import codecs
import random
import os.path

# own modules
import googlebooks
import openlibrary
from book import Book


def isbnlist(isbnfile):
    isbn=[]
    with codecs.open(isbnfile,"r","utf-8") as f:
        for line in f:
            if len(line.strip()) > 0:
                isbn.append(line.strip())
        return isbn
        
def _parseisbn(isbn):
    return isbn.strip().replace("-","")
    
def downloadcover(b):
    if b.imgurl:
        #print("Download image from " + b.imgurl)
        fname = "images/"+b.get_isbn() + ".jpg"
        if not os.path.isfile(fname):
            urllib.request.urlretrieve(b.imgurl,fname)
        
def searchbook(isbn):
    b = googlebooks.searchbook(isbn)
    if not b:
        b = openlibrary.searchbook(isbn)
    
    return b

def clean(s):
    if s:
        return str(s).strip().replace('"',' ')
    return ""

def _imgurl(b):
    return "images/"+b.get_isbn()+".jpg"

def _bookexists(isbn):
    filename = "books/"+isbn+".md"
    return os.path.isfile(filename)
    
def writebook(b):
    filename = "books/"+b.get_isbn()+".md"
    if os.path.isfile(filename):
        return
        
    with codecs.open(filename,"w","utf-8") as f:
        # front
        f.write("+++\n")
        f.write("title = \""+clean(b.title)+"\"\n")
        f.write("author = \""+clean(b.author)+"\"\n")
        f.write("publisher = \""+clean(b.publisher)+"\"\n")
        f.write("publishdate = \""+clean(b.publishdate)+"\"\n")
        f.write("subtitle = \""+clean(b.subtitle)+"\"\n")
        f.write("isbn_10 = \""+clean(b.isbn_10)+"\"\n")
        f.write("isbn_13 = \""+clean(b.isbn_13)+"\"\n")
        f.write("service = \""+clean(b.service)+"\"\n")
        f.write("pages = "+clean(b.pages)+"\n")
        f.write("bookid = \""+clean(b.bookid)+"\"\n")
        f.write("imgurl = \""+clean(_imgurl(b))+"\"\n")
        f.write("bookurl = \""+clean(b.bookurl)+"\"\n")
        f.write("+++\n")
        f.write("\n")
        f.write(clean(b.description)+"\n")
        
        
        
def main():
    isbn = isbnlist(sys.argv[1])
    for i in isbn:
        print("Process " + i)
        if _bookexists(_parseisbn(i)):
            continue
        time.sleep(random.randint(6,11))
        b = searchbook(i)
        if b:
            writebook(b)
            downloadcover(b)
        else:
            print(i + " not found")
    
if __name__ == "__main__":
    main()
        