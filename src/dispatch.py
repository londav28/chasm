# MIT LICENSE Copyright (c) 2018 David Longnecker

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


import inspect


# Inspired by a blogpost...
# https://chris-lamb.co.uk/posts/visitor-pattern-in-python


_dmap_map = {}


def _qname(f): return f.__module__ + '.' + f.__qualname__


def _register_base(pos, f):
    sig = inspect.signature(f)
    qn = _qname(f)
    if not type(pos) is int:
        raise TypeError('Parameter position must be of type int.')
    if pos < 0 or pos >= len(sig.parameters):
        raise ValueError('Bad parameter position ', pos, ' for ', qn)
    if qn in _dmap_map:
        raise NameError('Function ', qn, ' already has a base.')
    _dmap_map[qn] = {
        'pos': pos,
        'dt': {},
        'base': f
    }


def _dmap_fetch(f):
    qn = _qname(f)
    if not qn in _dmap_map:
        raise ValueError('Function ', qn, ' has no base.')
    return _dmap_map[qn]


def _register_when(ftype, f):
    sig = inspect.signature(f)
    dm = _dmap_fetch(f)
    qn = _qname(f)
    if dm['pos'] >= len(sig.parameters):
        raise ValueError('Base ', qn, ' rooted at parameter ', dm['pos'])
    if ftype in dm['dt']:
        raise KeyError('Function ', qn, ' already has entry for ', ftype)
    dm['dt'][ftype] = f


def _lookup(f, *args, **kwargs):
    dm = _dmap_fetch(f)
    ptype = type(args[0][dm['pos']])
    if ptype in dm['dt']:
        # Args 0 contains user args, and the * operator "unwraps" args[0].
        return dm['dt'][ptype](*args[0])
    return dm['base'](*args[0])


# Learned decorators with args from...
# http://scottlobdell.me/2015/04/decorators-arguments-python/


def base(pos):
    def real(f):
        _register_base(pos, f)
        def wrapper(*args, **kwargs):
            return f(args, kwargs)
        return wrapper
    return real


def when(ftype):
    def real(f):
        _register_when(ftype, f)
        def wrapper(*args, **kwargs):
            return _lookup(f, args, kwargs)
        return wrapper
    return real


def list(ftypelist):
    def real(f):
        for ftype in ftypelist:
            _register_when(ftype, f)
        def wrapper(*args, **kwargs):
            return _lookup(f, args, kwargs)
        return wrapper
    return real
