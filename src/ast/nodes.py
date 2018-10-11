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


#-----------------------------------------------------------------------------
# BASE
# ----------------------------------------------------------------------------


class Node(object):
    pass


class Module(Node):
    def __init__(self):
        self.children = []


class Method(Node):
    def __init__(self):
        self.id = None
        self.args = []
        self.rtype = None
        self.body = []


class Object(Node):
    def __init__(self):
        self.id = None
        self.fields = []


class Pragma(Node):
    def __init__(self):
        self.id = None
        self.arg = None


class Type(Node):
    def __init__(self):
        self.id = None
        self.depth = 0


class Label(Node):
    def __init__(self):
        self.id = None


class Try(Node):
    def __init__(self):
        self.body = []
        self.handlers = []


class Except(Node):
    def __init__(self):
        self.what = None
        self.body = []


class Instruction(Node):
    def __init__(self):
        self.opcode = None
        self.arg = None


#-----------------------------------------------------------------------------
# TRANSFORM
# ----------------------------------------------------------------------------


class NoImmediate(Node):
    pass


class ImmediateU8(Node):
    pass


class ImmediateU16(Node):
    pass


class ImmediateU32(Node):
    pass


class ImmediateU64(Node):
    pass


class ImmediateI8(Node):
    pass


class ImmediateI16(Node):
    pass


class ImmediateI32(Node):
    pass


class ImmediateI64(Node):
    pass


class ImmediateF32(Node):
    pass


class ImmediateF64(Node):
    pass


class UnresolvedJump(Node):
    pass


# An arbitrary grouping of statements, introduced during tramsform.
class Group(Node):
    def __init__(self):
        self.children = []