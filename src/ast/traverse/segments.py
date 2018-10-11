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


# NOTE
# - Consult the "doc/bytecode-format.md" file for the most recent bytecode
#   format (there's only one). It also contains flag values that can be set
#   for different status bytes (module/method/object).
#


import src.error as err
import src.dispatch as dispatch
import src.ast.nodes as ast
import src.ast.common as acm
import src.fixedwidth as fw
import struct


# NOTE: These are formatters for packing functions.
_u8     = 'B'
_u16    = 'H'
_u32    = 'I'
_u64    = 'Q'
_i8     = 'b'
_i16    = 'h'
_i32    = 'i'
_i64    = 'q'
_f32    = 'f'
_f64    = 'd'


_byte_order = '<'
_csm_magic = bytes('csmx', 'ascii')
_null_byte = struct.pack((_byte_order + _u8), 0)


def _packwrapper(fmat, *args):
    rfmat = _byte_order + fmat
    return struct.pack(rfmat, *args)


def _packinto(outlist, fmat, *args):
    packed = _packwrapper(fmat, *args)
    outlist.append(packed)
    return outlist


@dispatch.base(0)
def visit(node, env=None):
    return []


@dispatch.when(ast.Module)
def visit(node, env=None):
    result = []
    m = env[node]
    # Start by inserting the magic number!
    result.append(_csm_magic)
    # NOTE: Append four empty status bytes for now.
    result.append(_null_byte)
    result.append(_null_byte)
    result.append(_null_byte)
    result.append(_null_byte)
    _packinto(result, _u32, m['method-count'])
    for method in m['methods']:
        result += visit(method, env)
    _packinto(result, _u32, m['object-count'])
    for object in m['objects']:
        result += visit(object, env)
    _packinto(result, _u32, m['string-count'])
    for string in m['strings']:
        length = fw.restrict(len(string), 'u32')
        _packinto(result, _u32, length)
        result.append(bytes(string, 'ascii'))
    _packinto(result, _u32, m['int64-count'])
    for int64 in m['int64s']:
        _packinto(result, _i64, int64)
    _packinto(result, _u32, m['flt64-count'])
    for flt64 in m['flt64s']:
        _packinto(result, _f64, flt64)
    return result


@dispatch.when(ast.Method)
def visit(node, env=None):
    result = []
    m = env[node]
    # NOTE: Don't parse status bytes for now.
    result.append(_null_byte)
    result.append(_null_byte)
    _packinto(result, _u32, m['name-string'])
    _packinto(result, _u32, m['debug-symbol'])
    # NOTE: Debugging symbol index unused for now.
    _packinto(result, _u32, m['signature-block'])
    _packinto(result, _u8, m['stack-limit'])
    _packinto(result, _u8, m['local-limit'])
    _packinto(result, _u32, m['ins-byte-count'])
    for b in node.body:
        result += visit(b, env)
    _packinto(result, _u32, m['ete-count'])
    for index, start, end, target in m['ete']:
        _packinto(result, _u32, index)
        _packinto(result, _u32, start)
        _packinto(result, _u32, end)
        _packinto(result, _u32, target)
    return result


@dispatch.when(ast.Object)
def visit(node, env=None):
    result = []
    m = env[node]
    # NOTE: Status byte is unused for now!
    result.append(_null_byte)
    _packinto(result, _u32, m['name-string'])
    _packinto(result, _u32, m['field-block'])
    return result


@dispatch.when(ast.Instruction)
def visit(node, env=None):
    err.fatal('Unclassified instruction while emitting segments:', node)


@dispatch.when(ast.UnresolvedJump)
def visit(node, env=None):
    err.fatal('Unresolved jump while emitting segments:', node)


@dispatch.when(ast.NoImmediate)
def visit(node, env=None):
    return [_packwrapper(_u8, node.op)]


_imd_struct_format_default = {
    ast.ImmediateU8     : 'BB',
    ast.ImmediateU16    : 'BH',
    ast.ImmediateU32    : 'BI',
    ast.ImmediateU64    : 'BQ',
    ast.ImmediateI8     : 'Bb',
    ast.ImmediateI16    : 'Bh',
    ast.ImmediateI32    : 'Bi',
    ast.ImmediateI64    : 'Bq',
    ast.ImmediateF32    : 'Bf',
    ast.ImmediateF64    : 'Bd'
}


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
def visit(node, env=None):
    key = type(node)
    assert(key in _imd_struct_format_default)
    format = _imd_struct_format_default[key]
    result = [_packwrapper(format, node.op, node.arg)]
    return result
