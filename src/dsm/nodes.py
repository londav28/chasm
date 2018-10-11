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


class Node(object):
    pass


class Module(Node):
    def __init__(self):
        self.status_1 = 0
        self.status_2 = 0
        self.status_3 = 0
        self.status_4 = 0
        self.methodc = 0
        self.methods = []
        self.objectc = 0
        self.objects = []
        self.stringc = 0
        self.strings = []
        self.int64c = 0
        self.int64s = []
        self.flt64c = 0
        self.flt64s = []


class Method(Node):
    def __init__(self):
        self.status_1 = 0
        self.status_2 = 0
        self.name = 0
        self.debugsymbol = 0
        self.paramc = 0
        self.paramblock = 0
        self.rtype = 0
        self.stack_limit = 0
        self.local_limit = 0
        self.instruction_count = 0
        self.streambytec = 0
        self.streambytes = []
        self.exceptionc = 0
        self.exceptions = []


class Object(Node):
    def __init__(self):
        self.status_1 = 0
        self.name = 0
        self.fieldc = 0
        self.fieldblock = 0


class String(Node):
    def __init__(self):
        self.bytec = 0
        self.bytes = []


class ExceptionTableEntry(Node):
    def __init__(self):
        self.object = 0
        self.start = 0
        self.end = 0
        self.target = 0




