#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  test_pool
# @author   dectinc@icloud.com
# @date     2015-08-28 01:30

def foo(baz):
    return 'a', 'foo' + baz


from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=5)

a = [str(i) for i in range(10)]

_result = []
for _ in a:
    _result.append( pool.apply_async(foo, _))  # tuple of args for foo

# do some other stuff in the main process

for _res in _result:
    return_val = _res.get()  # get the return value from your function.

    print return_val