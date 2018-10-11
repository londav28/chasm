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


import src.tokentype as tktype
import src.tokenmap as tkmap
import src.reader as reader
import inspect


_charset_alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_charset_num = '0123456789'
_charset_sym = _charset_alpha + _charset_num + '_'
_charset_hex = _charset_num + 'abcdefABCDEF'


_str_break = ', '


_ch_underscore = '_'
_ch_quote = '"'
_ch_newline = '\n'
_ch_tab = '\t'
_ch_space = ' '
_ch_period = '.'
_ch_pound = '#'
_ch_zero = '0'
_ch_x = 'x'
_ch_empty = ''


def _contains(list, str):
    for i in range(0, len(list)):
        if list[i] == str:
            return i
    return None


def _is_of_set(str, against):
    for char in str:
        if _contains(against, char) == None:
            return False
    return True


def _is_alpha(str):
    return _is_of_set(str, _charset_alpha)


def _is_digit(str):
    return _is_of_set(str, _charset_num)


def _is_symbol(str):
    return _is_of_set(str, _charset_sym)


def _is_hex(str):
    return _is_of_set(str, _charset_hex)


def _is_not_quote(str):
    return str != _ch_quote


def _is_not_newline(str):
    return str != _ch_newline


def _is_space(str):
    return str == _ch_space


class Token(object):
    def __init__(self):
        self.toktype = None
        self.value = None
        self.line = None
        self.col = None

    def __str__(self):
        result = _ch_empty
        result += str(self.toktype) + _str_break
        result += tktype.get_tokentype_str(self.toktype) + _str_break
        result += '(' + str(self.line) + ':'
        result += str(self.col) + ')'
        tt = self.toktype
        if tktype.is_non_static(tt) and not tktype.is_whitespace(tt):
            result += _str_break + self.value
        return result

    def has_toktype(self, toktype):
        return self.toktype == toktype


class Lexer(object):

    def __init__(self, src, trace=False):
        # Has to be first for our little call chain hack to work.
        self.trace = trace
        self.reader = reader.Reader(src)
        self.char = self.reader.next()

    def _advance(self, ahead=1):
        for i in range(0, ahead):
            self.char = self.reader.next()
        return self.char

    # Useful to use if there is a bug in the grammar implementation.
    def __getattribute__(self, name):
        returned = object.__getattribute__(self, name)
        disp = object.__getattribute__(self, 'trace')

        if ((inspect.isfunction(returned) or inspect.ismethod(returned))
                and disp):
            print('Called: ', returned.__name__)
        return returned

    def _concatwhile(self, cond):
        result = _ch_empty
        if cond(self.char):
            result = self.char
            while self._advance() != None and cond(self.char):
                result += self.char
        return result

    def _peek(self, ahead=1):
        return self.reader.peek(ahead)

    def _form_symbol_or_keyword(self):
        value = self._concatwhile(_is_symbol)
        if value in tkmap.keyword:
            return (tkmap.keyword[value], value)
        return (tktype.t_symbol, value)

    def _form_numeric(self):
        peek = self._peek(2)
        if peek[0] == _ch_zero and peek[1] == _ch_x:
            self._advance(2)
            if _is_hex(self.char):
                value = self._concatwhile(_is_hex)
                return (tktype.t_hex, value)
            value = self.char
            return (tktype.t_unknown, value)
        # Handle the case of a malformed whole number.
        if peek[0] == _ch_zero and _is_digit(peek[1]):
            value = self._concatwhile(_is_digit)
            return (tktype.t_unknown, value)
        value = self._concatwhile(_is_digit)
        peek = self._peek()
        if peek[0] == _ch_period and _is_digit(peek[1]):
            self._advance()
            value += _ch_period + self._concatwhile(_is_digit)
            return (tktype.t_flt, value)
        return (tktype.t_int, value)

    def _form_string(self):
        self._advance()
        if self.char == None:
            value = _ch_quote
            return (tktype.t_unknown, value)
        value = self._concatwhile(_is_not_quote)
        if self.char != _ch_quote:
            return (tktype.t_unknown, value)
        self._advance()
        return (tktype.t_str, value)

    def next(self):
        result = Token()
        result.line = self.reader.get_line()
        result.col = self.reader.get_col()
        if not self.char:
            result.toktype = tktype.t_eof
            return result
        if self.char == _ch_space:
            result.toktype = tktype.t_spaces
            result.value = self._concatwhile(_is_space)
            return result
        if self.char == _ch_pound:
            result.toktype = tktype.t_comment
            result.value = self._concatwhile(_is_not_newline)
            return result
        transition = None
        if _is_alpha(self.char) or self.char == _ch_underscore:
            transition = self._form_symbol_or_keyword()
        if _is_digit(self.char):
            transition = self._form_numeric()
        if self.char == _ch_quote:
            transition = self._form_string()
        if transition:
            result.toktype = transition[0]
            result.value = transition[1]
            return result
        one = self.char
        # Only take this branch if we are not EOF.
        if self._advance():
            two = one + self.char
            if two in tkmap.lktwo:
                self._advance()
                result.toktype = tkmap.lktwo[two]
                result.value = two
                return result
        if one in tkmap.lkone:
            result.toktype = tkmap.lkone[one]
            result.value = one
            return result
        result.toktype = tktype.t_unknown
        result.value = self.char
        return result
