#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @chaign_c

import contextlib
import os
from contextlib import ContextDecorator
# from functools import wraps

# ==========================================================
# Exception manager based on decorator/context/callback.
# ping me if you like this part, I might push it on pypi.
# Using this we can separate code logic from error handling, 
# the goal would be to reduce code duplication and ease development.
# ==========================================================

def do_exall(fn, exception, callback):
    """ Call *callback* on *exception* when *fn* is called """
    if not isinstance(exception, tuple):
        exception = (exception,)
    def new_function(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except exception as e:
            callback(e)
    new_function.__wrapped__ = fn
    return new_function

class exall(ContextDecorator):
    """
        A context and decorator for do_exall.
        Call *callback* on *exception* when *fn* is called. 
    """
    def __init__(self, fn, exception, callable):
        super().__init__()
        self.fn_module = __import__(fn.__module__)
        self.fn_name = fn.__name__
        self.backup = fn

    def __enter__(self):
        setattr(self.fn_module,  self.fn_name, do_exall(fn, exception, callback))

    def __exit__(self, *exc):
        setattr(self.fn_module,  self.fn_name, self.backup)

# =========================================================
# Callbacks: several basic way of handling exception
# =========================================================

import traceback
from pprint import pprint
import sys

def print_traceback(exception):
    print(exception)
    pprint(traceback.extract_stack()[:-2])

def print_warning(exception):
    location = traceback.extract_stack()[-3]
    print("WARNING: {exception}, ==> {location}".format(exception=exception, location=location))

def ignore(exception):
    pass

def print_error(exception):
    pprint(traceback.extract_stack()[:-2])
    location = traceback.extract_stack()[-3]
    print("ERROR: {exception}, ==> {location}".format(exception=exception, location=location))
    sys.exit(1)
