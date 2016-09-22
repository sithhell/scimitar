#!/usr/bin/env python
# coding: utf-8
'''
    Scimitar: Ye Distributed Debugger
    ~~~~~~~~
    :copyright:
    Copyright (c) 2016 Parsa Amini
    Copyright (c) 2016 Hartmut Kaiser
    Copyright (c) 2016 Thomas Heller
    :license:
    Distributed under the Boost Software License, Version 1.0. (See accompanying
    file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
'''
import gdb

printer_dict = {}

class TupleMemberPrinter(object):
    def __init__(self, expr, val, tmpl):
        self.val = val
        self.expr = expr
        self.tmpl = [t.strip() for t in tmpl.split(',')]

    def display_hint(self):
        return self.expr

    def to_string(self):
        txt = ''
        try:
            txt = '%s' % gdb.parse_and_eval('_value')
        except gdb.error:
            try:
                txt = '%s' % gdb.parse_and_eval('*(%s *)this' % self.tmpl[1])
            except gdb.error:
                pass
                
        return "(%s) {{ %s }} %#02x" % (self.expr, txt, self.val.address)
printer_dict['hpx::util::detail::tuple_member<(?P<tmpl>.+)>'] = TupleMemberPrinter

class TuplePrinter(object):
    def __init__(self, expr, val, tmpl):
        self.val = val
        self.expr = expr
        self.tmpl = [t.strip() for t in tmpl.split(',')]

    def display_hint(self):
        return self.expr

    def to_string(self):
        parts = ['%s' % gdb.parse_and_eval('(hpx::util::detail::tuple_member<%d,%s,void>&)_impl' % (i, t)) for i, t in enumerate(self.tmpl)]
        txt = ', '.join(parts)
                
        return "(%s) {{ %s }} %#02x" % (self.expr, txt, self.val.address)

    def children(self):
        result = [] 
        for i, t in enumerate(self.tmpl):
            result.extend([
                ('%d' % i, '%s' % gdb.parse_and_eval('(hpx::util::detail::tuple_member<%d,%s,void>&)_impl' % (i, t))),
            ])
                
        return result
printer_dict['hpx::util::tuple<(?P<tmpl>.+)>'] = TuplePrinter
