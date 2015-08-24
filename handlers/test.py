#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  test.py
# @author   dectinc@icloud.com
# @date     2015-08-24 23:15

from handlers.base import BaseHandler


class TestHandler(BaseHandler):
    def get(self):
        url = ''
        activity = ''
        try:
            url = self.get_argument("url")
            activity = self.get_arguments('activity')
        except:
            self.render('../templates/portal.html', url="", result=[])
            return
        print url
        print activity
        self.render('../templates/portal.html', url=url, result=activity)


class TestHandler2(BaseHandler):
    def get(self):
        print 'say hello'
        items = ["item1", "item2", "item3"]
        # render the corresponding template file, and pass the "**args" to the assigned template
        # not only we can pass the realted parameters, but also can pass the related functions.
        # so extendible and powerful! :)
        items2 = ["item1", "item2"]

        def checked(item):
            return 'checked=checked' if item in items2 else ''

        self.render("../templates/test1.html", items=items, add=add, items2=items2, checked=checked)


# define one "add" customization funcation which will be used in the assigned template file.
def add(x, y):
    return (x + y)