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


import src.lexer as lx
import src.error as err
import src.ast.nodes as ast
import src.tokentype as tt


import inspect
import sys


_ws_ignore = [
    tt.t_comment,
    tt.t_spaces,
    tt.t_newline,
    tt.t_tab
]


class ParserOutput(object):

    def __init__(self, src=None, lex = None, tok=None, mod=None, err=None):
        self.src = src
        self.lex = lex
        self.tok = tok
        self.mod = mod
        self.err = err


class Parser(object):

    def __init__(self, trace=False):
        # Has to be first for our trace hack to work!
        self.trace = trace
        self.out = None
        self.queue = []

    def __getattribute__(self, name):
        returned = object.__getattribute__(self, name)
        trace = object.__getattribute__(self, 'trace')
        if ((inspect.isfunction(returned) or inspect.ismethod(returned))
                and trace):
            print('Called: ', returned.__name__)
        return returned

    def _last(self):
        return self.out.tok

    def _stop(self, msg):
        last = self._last()
        out = 'Parser expected ' + msg + ' but found ' + str(last)
        err.fatal(out)

    def _next_skip_ws(self):
        result = self.out.lex.next()
        while result.toktype in _ws_ignore:
            result = self.out.lex.next()
        return result

    def _advance(self, ahead=1):
        result = self.out.tok
        for i in range(0, ahead):
            if self.queue:
                result = self.queue.pop(0)
            else:
                result = self._next_skip_ws()
        self.out.tok = result
        return result

    def _peek(self, ahead=1):
        demand = ahead - len(self.queue)
        for i in range(0, demand):
            tok = self._next_skip_ws()
            self.queue.append(tok)
        result = [self._last()] + self.queue[:ahead]
        return result

    def _accept(self, toktype):
        last = self._last()
        if last.toktype == toktype:
            if self.trace:
                print('Accepting: ', str(last))
            self._advance()
            return True
        return False

    def _yield(self):
        result = self._last()
        self._advance()
        return result

    def _satisfies(self, predicate):
        return predicate(self._last().toktype)

    def _expect(self, toktype):
        disp = tt.get_tokentype_str(toktype)
        result = self._last()
        if self.trace:
            print('Expecting: ', toktype, disp, ', found:', result)
        if result.toktype == toktype:
            self._advance()
            return result
        self._stop(disp)

    def _expect_satisfies(self, predicate):
        result = self._last()
        if self.trace:
            print('Must satisfy: ', predicate, ', found ', result)
        if predicate(result.toktype):
            self._advance()
            return result
        self._stop('token to satisfy ' + str(predicate.__name__))

    def _output_init(self, src):
        result = ParserOutput(
            src,
            lx.Lexer(src),
            None,
            ast.Module(),
            None
        )
        return result

#----------------------------------------------------------------------------#
# BEGIN GRAMMAR                                                              #
#----------------------------------------------------------------------------#

    def m_module(self, src, buildflags=None):
        self.out = self._output_init(src)
        self._advance()
        children = self.out.mod.children
        while not self._accept(tt.t_eof):
            last = self._last()
            if self._accept(tt.t_dollar):
                children.append(self.m_pragma())
                continue
            if self._accept(tt.t_method):
                children.append(self.m_method())
                continue
            if self._accept(tt.t_object):
                children.append(self.m_object())
                continue
            self._stop('pragma, method, or object')
        result = self.out
        self.out = None
        return result

    def m_pragma(self):
        result = ast.Pragma()
        result.id = self._expect(tt.t_symbol)
        if self._accept(tt.t_assign):
            def is_pragma_arg(v):
                return v in [
                    tt.t_str,
                    tt.t_int,
                    tt.t_hex,
                    tt.t_flt,
                    tt.t_symbol
                ]
            result.arg = self._expect_satisfies(is_pragma_arg)
        self._expect(tt.t_semicolon)
        return result

    def m_method(self):
        result = ast.Method()
        result.id = self._expect(tt.t_symbol)
        self._expect(tt.t_less)
        while not self._accept(tt.t_greater):
            result.args.append(self.m_type())
            while self._accept(tt.t_comma):
                result.args.append(self.m_type())
        if not self._accept(tt.t_void):
            result.rtype = self.m_type()
        self._expect(tt.t_lbrace)
        while not self._accept(tt.t_rbrace):
            result.body.append(self.m_statement())
        return result

    def m_object(self):
        result = ast.Object()
        result.id = self._expect(tt.t_symbol)
        self._expect(tt.t_lbrace)
        while not self._accept(tt.t_rbrace):
            result.fields.append(self.m_type())
            while self._accept(tt.t_comma):
                result.fields.append(self.m_type())
        return result

    def m_type(self):
        result = ast.Type()
        while self._accept(tt.t_star):
            result.depth += 1
        result.id = self._expect(tt.t_symbol)
        return result

    def m_statement(self):
        if self._accept(tt.t_dollar):
            return self.m_pragma()
        if self._accept(tt.t_at):
            return self.m_label()
        if self._accept(tt.t_try):
            return self.m_try()
        if self._satisfies(tt.is_instruction):
            return self.m_instruction()
        self._stop('pragma, label, or instruction')

    def m_label(self):
        result = ast.Label()
        result.id = self._expect(tt.t_symbol)
        self._expect(tt.t_colon)
        return result

    def m_try(self):
        result = ast.Try()
        self._expect(tt.t_lbrace)
        while not self._accept(tt.t_rbrace):
            result.body.append(self.m_statement())
        self._expect(tt.t_except)
        result.handlers.append(self.m_except())
        while self._accept(tt.t_except):
            result.handlers.append(self.m_except())
        return result

    def m_except(self):
        result = ast.Except()
        result.what = self._expect(tt.t_symbol)
        self._expect(tt.t_lbrace)
        while not self._accept(tt.t_rbrace):
            result.body.append(self.m_statement())
        return result

    def m_instruction(self):
        if not self._satisfies(tt.is_instruction):
            self._stop('instruction')
        result = ast.Instruction()
        result.opcode = self._yield()
        if not self._accept(tt.t_semicolon):
            def is_instruction_arg(v):
                return v in [
                    tt.t_int,
                    tt.t_hex,
                    tt.t_flt,
                    tt.t_str,
                    tt.t_symbol
                ]
            result.arg = self._expect_satisfies(is_instruction_arg)
            self._expect(tt.t_semicolon)
        return result
