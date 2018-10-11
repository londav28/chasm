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


import src.dispatch as dispatch
import src.ast.nodes as ast
import src.ast.common as acm


def _flatten_groups(body, env):
    result = []
    for s in body:
        if not isinstance(s, ast.Group):
            result.append(s)
            continue
        flat = visit(s, env)
        result += flat
    return result


@dispatch.base(0)
def visit(node, env=None):
    return node


@dispatch.when(ast.Module)
def visit(node, env=None):
    node.children = acm.visitlist(node.children, visit, env)
    return node


@dispatch.when(ast.Method)
def visit(node, env=None):
    node.body = _flatten_groups(node.body, env)
    return node


@dispatch.when(ast.Group)
def visit(node, env=None):
    result = _flatten_groups(node.children, env)
    return result
