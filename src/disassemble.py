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


import src.dsm.nodes as dsc
import src.error as err
import struct
import copy


_csm_magic = bytes('csmx', 'ascii')
_dsm_empty = (None, None)


# Different width settings:
_fmt_indexwidth_u32 = 'I'
_fmt_indexwidth_u64 = 'Q'
_fmt_jumpwidth_i32 = 'i'
_fmt_jumpwidth_i64 = 'q'


_parse_errors = {
    'tiny'      : 'File is too small to contain any meaningful data',
    'magic'     : 'Magic number mismatch',
    'eof'       : 'Reached end of stream while parsing'
}


def _parse_error(error):
    reason = 'Unknown reasion for failure'
    if error in _parse_errors:
        reason = _parse_errors[error]
    print('Disassembler failed to parse:', reason)


# There must be exactly 8 of these, so be careful.
_bytecode_f1 = [
    'bigendian',    # Compiled in big endian format
    'intern64',     # 64-bit immediates are interned in tables
    'nolimits',     # No stack/local limits are set
    'widemode',     # Interned indexes and jumps are 64-bit
    'comptypes',    # Parameter/object type strings are compacted
    'monostream',   # Code is packed into a single instruction stream
    'extended',     # Uses extended instruction set
    'next'          # Uses second status byte
]


_bytecode_f2 = [
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'next'
]


_bytecode_f3 = [
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'next'
]


_bytecode_f4 = [
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused',
    'unused'
]


_flagbyte_lists = [
    _bytecode_f1,
    _bytecode_f2,
    _bytecode_f3,
    _bytecode_f4
]


def _is_bit_set(number, bitpos):
    return (number & (1 << bitpos)) != 0


def _check_magic(bc):
    if len(bc) < 4:
        return False
    return bc[0:4] == _csm_magic


def _advance(format, bc, ofs, env):
    remaining = len(bc) - ofs
    req = 0
    try:
        req = struct.calcsize(format)
    except struct.error:
        err.fatal('Internal error, invalid unpack format', format)
    if remaining < req:
        return (None, )
    items = struct.unpack_from(format, bc, ofs)
    return (ofs + req, *items)


_default_environment = {
    'flags'     : {
        'bigendian'     : False,
        'intern64'      : False,
        'nolimits'      : False,
        'widemode'      : False,
        'comptypes'     : False,
        'monostream'    : False,
        'extended'      : False
    },

    'fmt'       : {
        'indexwidth'    : _fmt_indexwidth_u32,
        'jumpwidth'     : _fmt_jumpwidth_i32
    }
}


def _env_init():
    return copy.deepcopy(_default_environment)


def _stringify_flagbytes(flagbytes):
    result = ''
    for i in range(0, len (flagbytes)):
        fb = flagbytes[i]
        result += 'Flag byte ' + str(i + 1) + ': '
        if fb == 0:
            result += str(hex(fb)) + '\n'
            continue
        result = 'Flags set (' + str(hex(fb)) + '):\n'
        flags = _flagbyte_list[i]
        for i in range(0, len(flags)):
            set = _is_bit_set(fb, i)
        if not set:
            continue
        result += flags[i] + '\n'
    return result


def _disassemble_flagbytes(bc, ofs, env):
    ofs, f1, f2, f3, f4 = _advance('bbbb', bc, ofs, env)
    if ofs == None:
        _parse_error('eof')
        return _dsm_empty
    flagbytes = [f1, f2, f3, f4]
    # At this point we need to modify the environment accordingly!
    # For now we'll assume default segments...
    return (ofs, flagbytes)


def _disassemble_method(bc, ofs, env):
    result = ''
    idxw = env['fmt']['indexwidth']
    ofs, methodcount = _advance(idxw, bc, ofs, env)
    if ofs == None:
        _parse_error('eof')
        return _dsm_empty


def _disassemble_object(bc, ofs, env):
    return (ofs, 'object\n')


def _disassemble_string(bc, ofs, env):
    return (ofs, 'string\n')


def _disassemble_module(bc, ofs, env):
    result = dsc.ModuleDescriptor()
    # Read flag bytes [b1, b2, b3, b4], and set environment.
    ofs, flagbytes = _disassemble_flagbytes(bc, ofs, env)
    if ofs == None: return _dsm_empty
    result.flagbytes = flagbytes
    idxw = env['fmt']['indexwidth']
    # Read method count (idx).
    ofs, methodcount = _advance(idxw, bc, ofs, env)
    if ofs == None: return _dsm_empty
    result.methodcount = methodcount
    # Disassemble methods.
    for i in range(0, methodcount):
        ofs, method = _disassemble_method(bc, ofs, env)
        if ofs == None: return _dsm_empty
        result.methods.append(method)
    # Read oject count (idx).
    ofs, objectcount = _advance(idxw, bc, ofs, env)
    if ofs == None: return _dsm_empty
    result.objectcount = objectcount
    # Disassemble objects.
    for i in range(0, objectcount):
        ofs, object = _disassemble_object(bc, ofs, env)
        if ofs == None: return _dsm_empty
        result.objects.append(object)
    # Read string count (idx).
    ofs, stringcount = _advance(idxw, bc, ofs, env)
    if ofs == None: return _dsm_empty
    result.stringcount = stringcount
    for i in range(0, stringcount):
        ofs, string = _disassemble_string(bc, ofs, env)
        if ofs == None: return _dsm_empty
        result.strings.append(string)
    return (ofs, result)


def _entrypoint_default(bc):
    if len(bc) < 4:
        _parse_error('tiny')
        return None
    if not _check_magic(bc):
        _parse_error('magic')
        return None
    env = _env_init()
    ofs = 4
    ofs, result = _disassemble_module(bc, ofs, env)
    if ofs == None:
        return None
    return result


def disassemble(bc, args=None):
    return _entrypoint_default(bc)
