#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    Book class
"""

class Book:
    
    def __init__(self):
        self.title = ""
        self.service = ""
        self.bookid = ""
        self.publishdate = ""
        self.author = ""
        self.pages = 0
        self.publisher = ""
        self.isbn_13 = ""
        self.isbn_10 = ""
        self.subtitle = ""
        self.description = ""
        self.imgurl = ""
        self.bookurl = ""
     
    def get_isbn(self):
        if self.isbn_13 != "":
            return self.isbn_13
        return self.isbn_10
    
    def set_isbn(self,isbn):
        if isbn:
            if len(isbn.strip()) > 10:
                self.isbn_13 = isbn.strip().replace("-","")
            else:
                self.isbn_10 = isbn.strip().replace("-","")
        
    def __str__(self):
        s =  "Book [\n title = " + self.title + "\n"
        s += " bookid = " + self.bookid + "\n"
        s += " author = " + self.author + "\n"
        s += " pages = " + str(self.pages) + "\n"
        s += " publishdate = " + self.publishdate + "\n"
        s += " publisher = " + self.publisher + "\n"
        s += " subtitle = " + self.subtitle + "\n"
        s += " isbn_13 = " + self.isbn_13 + "\n"
        s += " isbn_10 = " + self.isbn_10 + "\n"
        s += " imgurl = " + self.imgurl + "\n"
        s += " service = " + self.service + "\n"
        s += " bookurl = " + self.bookurl + "\n"
        s += "]"
        return s
        