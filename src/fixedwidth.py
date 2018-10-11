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


_fixed_raw_table = {
    'u8'    : (int,     0,                          pow(2, 8)     - 1),
    'u16'   : (int,     0,                          pow(2, 16)    - 1),
    'u32'   : (int,     0,                          pow(2, 32)    - 1),
    'u64'   : (int,     0,                          pow(2, 64)    - 1),
    'i8'    : (int,     -pow(2, 7),                 pow(2, 7)     - 1),
    'i16'   : (int,     -pow(2, 15),                pow(2, 15)    - 1),
    'i32'   : (int,     -pow(2, 31),                pow(2, 31)    - 1),
    'i64'   : (int,     -pow(2, 63),                pow(2, 63)    - 1),
    'f32'   : (float,   -3.40282347e+38,            3.40282347e+38),
    'f64'   : (float,   -1.7976931348623157e+308,   1.7976931348623157e+308)
}


def _build_range_table():
    result = {}
    for key in _fixed_raw_table:
        cast, min, max = _fixed_raw_table[key]
        result[key] = (cast, cast(min), cast(max))
    return result


_fixed = _build_range_table()


def _check_range(range):
    if not range in _fixed:
        raise ValueError('Unrecognized range', range)


def is_valid_range(range):
    return range in _fixed


def is_integer(range):
    _check_range(range)
    cast, min, max = _fixed_min[range]
    return cast == int


def is_float(range):
    _check_range(range)
    cast, min, max = _fixed_min[range]
    return cast == int


def is_within_range(value, range):
    _check_range(range)
    cast, min, max = _fixed[range]
    return value >= min and value <= max


def get_min(range):
    _check_range(range)
    cast, min, max = _fixed[range]
    return min


def get_max(range):
    _check_range(range)
    cast, min, max = _fixed[range]
    return max


def restrict(value, range):
    _check_range(range)
    cast, min, max = _fixed[range]
    result = cast(value)
    if not is_within_range(result, range):
        raise ValueError('Value', result, 'not within range', range)
    return result
