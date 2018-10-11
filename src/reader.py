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


class Reader(object):

    def __init__(self, text):
        self._text = text
        self._lchar = None
        self._pos = 0
        self._linec = 0
        self._charc = 0
        self._queue = []

    def hasnext(self):
        if self._text == None:
            return False
        return self._queue or self._pos < len(self._text)

    def _advance(self):
        result = self._text[self._pos]
        self._pos += 1
        return result

    def peek(self, ahead=1):
        # The first character is always the current last token.
        rest = len(self._queue)
        for i in range(0, ahead - rest):
            self._queue.append(self._advance())
        return [self._lchar] + self._queue[:ahead]

    def next(self, skip=0):
        if not self.hasnext():
            return None
        if self._queue:
            self._lchar = self._queue.pop(0)
        else:
            self._lchar = self._advance()
        self._charc += 1
        if self._lchar == '\n':
            self._charc = 0
            self._linec += 1
        return self._lchar

    def ignoreuntil(self, until):
        char = self.next()
        while char != until and char != None:
            char = self.next()

    def get_col(self):
        return self._charc

    def get_line(self):
        return self._linec


class NoCommentReader(Reader):
    def __init__(self, src, comstart='#'):
        super().__init__(src)
        self._comstart = comstart
        if comstart == ' ':
            self._comstart = None

    def next(self, skip=0):
        result = Reader.next(self, skip)
        if self._comstart == None:
            return result
        while result == self._comstart and result != None:
            self.ignoreuntil('\n')
            result = Reader.next(self, skip)
        return result
