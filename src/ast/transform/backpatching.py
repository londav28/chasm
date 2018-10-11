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


@dispatch.base(0)
def visit(node, env=None):
    return node


@dispatch.when(ast.Module)
def visit(node, env=None):
    node.children = acm.visitlist(node.children, visit, env)
    return node


@dispatch.when(ast.Method)
def visit(node, env=None):
    # Again, this wouldn't work with nested methods.
    env['active-method'] = env[node]
    node.body = acm.visitlist(node.body, visit, env)
    return node


@dispatch.when(ast.UnresolvedJump)
def visit(node, env=None):
    m = env['active-method']['labelmap']
    target = node.arg.value
    assert(target in m)
    destination = m[target]
    # Don't forget that all jumps are now absolute!
    result = ast.ImmediateU32()
    result.oplabel = node.opcode.value
    result.op = node.opcode.toktype
    result.arg = destination
    result.ins = node.ins
    return result


@dispatch.when(ast.Group)
def visit(node, env=None):
    node.body = acm.visitlist(node.body, env)
    return node