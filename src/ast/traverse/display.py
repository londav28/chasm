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
import src.tokentype as tt
import src.ast.nodes as ast


def _tabify(ind=0, tabsize=2):
    if ind <= 0 or tabsize <= 0:
        return ''
    return ' ' * tabsize * ind


def _label(item, ind):
    # Use "instance.__class__.__name__" to avoid qualification.
    print(_tabify(ind) + item.__class__.__name__)


def _value(label, val, ind):
    tabs = _tabify(ind)
    print(tabs + label + ' = ' + str(val))


def _labelvisit(node, ind):
    _label(node, ind)
    visit(node, ind + 1)


def _display_immediate(node, ind):
    _value('opcode', node.opcode, ind)
    _value('arg', node.arg, ind)


@dispatch.base(0)
def visit(node, ind=0):
    _value('error', type(node), ind)


@dispatch.when(ast.Module)
def visit(node, ind=0):
    for c in node.children:
        _labelvisit(c, ind)


@dispatch.when(ast.Method)
def visit(node, ind=0):
    _value('id', node.id, ind)
    for a in node.args:
        _labelvisit(a, ind)
    _labelvisit(node.rtype, ind)
    for b in node.body:
        _labelvisit(b, ind)


@dispatch.when(ast.Object)
def visit(node, ind=0):
    _value('id', node.id, ind)
    for f in node.fields:
        _labelvisit(f, ind)


@dispatch.when(ast.Pragma)
def visit(node, ind=0):
    _value('id', node.id, ind)
    if node.arg:
        _value('arg', node.arg, ind)


@dispatch.when(ast.Type)
def visit(node, ind=0):
    _value('id', node.id, ind)
    _value('depth', node.depth, ind)


@dispatch.when(ast.Label)
def visit(node, ind=0):
    _value('id', node.id, ind)


@dispatch.when(ast.Try)
def visit(node, ind=0):
    for s in node.body:
        _labelvisit(s, ind)
    for h in node.handlers:
        _labelvisit(h, ind)


@dispatch.when(ast.Except)
def visit(node, ind=0):
    _value('type', node.what, ind)
    for s in node.body:
        _labelvisit(s, ind)


@dispatch.when(ast.Instruction)
def visit(node, ind=0):
    _value('opcode', node.opcode, ind)
    if node.arg:
        _value('arg', node.arg, ind)


@dispatch.when(ast.NoImmediate)
def visit(node, ind=0):
    _value('oplabel', node.oplabel, ind)
    _value('op', node.op, ind)
    _value('ins', node.ins, ind)


@dispatch.list([
    ast.ImmediateU8,
    ast.ImmediateU16,
    ast.ImmediateU32,
    ast.ImmediateU64,
    ast.ImmediateI8,
    ast.ImmediateI16,
    ast.ImmediateI32,
    ast.ImmediateI64,
    ast.ImmediateF32,
    ast.ImmediateF64
])
def visit(node, ind=0):
    _value('oplabel', node.oplabel, ind)
    _value('op', node.op, ind)
    _value('arg', node.arg, ind)
    _value('ins', node.ins, ind)


@dispatch.when(ast.UnresolvedJump)
def visit(node, ind=0):
    _value('opcode', node.opcode, ind)
    _value('arg', node.arg, ind)
    _value('ins', node.ins, ind)


@dispatch.when(ast.Group)
def visit(node, ind=0):
    for c in node.children:
        _labelvisit(c, ind)
