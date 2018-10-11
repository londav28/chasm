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
#
# - We avoid redundant asserts of interned data and INS length by instead
#   asserting that the values are valid at the end, IE - if the final INS
#   length or interned table length is good, then everything else is, too.
#
# - In some cases we need the asserts, IE when adding a value to the flt64
#   table we need to make sure the value is within width.


import src.tokentype as tt
import src.dispatch as dispatch
import src.ast.nodes as ast
import src.error as err
import src.fixedwidth as fw
import src.ast.common as acm


def _cast_to_integer(node):
    t = node.toktype
    assert(t in [tt.t_int, tt.t_hex])
    result = None
    # TODO;: Automate the conversion process!
    if t == tt.t_hex:
        result = int(node.value, 16)
    if t == tt.t_int:
        result = int(node.value)
    return result


def _cast_to_float(node):
    t = node.toktype
    assert(t in [tt.t_flt, tt.t_hex])
    result = None
    # TODO;: Automate the conversion process!
    if t == tt.t_hex:
        # Reinterpretation of the raw bits as per here!
        # https://stackoverflow.com/questions/1592158/convert-hex-to-float
        from ctypes import pointer, cast
        v = int(node.value, 16)
        intp = pointer(c_int(v))
        fltp = cast(intp, POINTER(c_float))
        result = fltp.contents.value
    if t == tt.t_int:
        result = float(node.value)
    return result


# Yes these three methods are redundant.
def _intern_str(s, env):
    assert(isinstance(s, str))
    m = env['interned-str']
    if s not in m:
        m[s] = len(m)
    result = m[s]
    return result


# Yes these three methods are redundant.
def _intern_int64(node, env):
    m = env['interned-int64']
    v = _cast_to_integer(node)
    assert(fw.is_within_range(v, 'i64'))
    if v not in m:
        m[v] = len(m)
    result = m[v]
    return result


# Yes these three methods are redundant.
def _intern_flt64(node, env):
    m = env['interned-flt64']
    v = _cast_to_float(node)
    assert(fw.is_within_range(v, 'f64'))
    if v not in m:
        m[v] = len(m)
    result = m[v]
    return result


def _listify_intern_map(m):
    result = len(m) * [None]
    for v, index in m.items():
        result[index] = v
    return result


def _imd_remap(node, constructor, converter, width):
    result = constructor()
    result.oplabel = node.opcode.value
    result.op = node.opcode.toktype
    result.arg = converter(node.arg.value)
    assert(fw.is_within_range(result.arg, width))
    return result


def _validate_u8(node, env):
    return _imd_remap(node, ast.ImmediateU8, int, 'u8')


def _validate_u16(node, env):
    return _imd_remap(node, ast.ImmediateU16, int, 'u16')


def _validate_u32(node, env):
    v = node.opcode.toktype
    # We can exit early if we get a jump.
    if tt.is_jump(v):
        result = ast.UnresolvedJump()
        result.opcode = node.opcode
        assert(node.arg.toktype == tt.t_symbol)
        result.arg = node.arg
        return result
    if not tt.has_interned_arg(v):
        return _imd_remap(node, ast.ImmediateU32, int, 'u32')
    # Switch on possible intern types here.
    ofs = None
    if v == tt.t_op_psh_q:
        ofs = _intern_int64(node.arg, env)
    elif v == tt.t_op_psh_f:
        ofs = _intern_flt64(node.arg, env)
    else:
        # NOTE: This method expects a string literal!
        ofs = _intern_str(node.arg.value, env)
    result = ast.ImmediateU32()
    result.oplabel = node.opcode.value
    result.op = v
    result.arg = ofs
    return result


def _validate_u64(node, env):
    return _imd_remap(node, ast.ImmediateU64, int, 'u64')


def _validate_i8(node, env):
    return _imd_remap(node, ast.ImmediateI8, int, 'u64')


def _validate_i16(node, env):
    return _imd_remap(node, ast.ImmediateI16, int, 'u64')


def _validate_i32(node, env):
    v = node.opcode.toktype
    return _imd_remap(node, ast.ImmediateI32, int, 'i32')


def _validate_i64(node, env):
    return _imd_remap(node, ast.ImmediateI64, int, 'i64')


def _validate_f32(node, env):
    return _imd_remap(node, ast.ImmediateF32, float, 'i64')


def _validate_f64(node, env):
    return _imd_remap(node, ast.ImmediateF64, float, 'f64')


def _validate_noi(node, env):
    assert(node.arg == None)
    result = ast.NoImmediate()
    result.oplabel = node.opcode.value
    result.op = node.opcode.toktype
    return result


_immediate_lookup_table = [
    (tt.has_immediate_u8,   _validate_u8,       1),
    (tt.has_immediate_u16,  _validate_u16,      2),
    (tt.has_immediate_u32,  _validate_u32,      4),
    (tt.has_immediate_u64,  _validate_u64,      8),
    (tt.has_immediate_i8,   _validate_i8,       1),
    (tt.has_immediate_i16,  _validate_i16,      2),
    (tt.has_immediate_i32,  _validate_i32,      4),
    (tt.has_immediate_i64,  _validate_i64,      8),
    (tt.has_immediate_f32,  _validate_f32,      4),
    (tt.has_immediate_f64,  _validate_f64,      8)
]


_scope_method = 1
_scope_object = 2


def _env_init(env):
    env['active-method-map'] = None
    env['active-object-map'] = None
    env['interned-str'] = {}
    env['interned-int64'] = {}
    env['interned-flt64'] = {}
    env['methods'] = []
    env['objects'] = []
    env['context-level'] = []


def _env_push_context(node, env):
    env['context-level'].append(node)


def _env_pop_context(env):
    env['context-level'].pop()


def _env_in(what, env):
    ct = env['context-level']
    if not ct:
        return False
    last = ct[-1]
    return (type(last) == what)


def _env_in_oneof(many, env):
    ct = env['context-level']
    if not ct:
        return False
    last = ct[-1]
    return type(last) in many


def _env_in_module(env):
    return _env_in(ast.Module, env)


def _env_in_method(env):
    return _env_in(ast.Method, env)


def _env_in_object(env):
    return _env_in(ast.Object, env)


def _env_fetch_create(node, env):
    if not node in env:
        env[node] = {}
    return env[node]


@dispatch.base(0)
def visit(node, env=None):
    return node


@dispatch.when(ast.Module)
def visit(node, env=None):
    if env is None:
        env = {}
    _env_init(env)
    _env_push_context(node, env)
    node.children = acm.visitlist(node.children, visit, env)
    m = _env_fetch_create(node, env)
    m['methods'] = env['methods']
    m['objects'] = env['objects']
    # Build and attach the string/int64/flt64 tables.
    m['strings'] = _listify_intern_map(env['interned-str'])
    m['int64s'] = _listify_intern_map(env['interned-int64'])
    m['flt64s'] = _listify_intern_map(env['interned-flt64'])
    # NOTE: Bounds checks we were talking about!
    m['method-count'] = fw.restrict(len(env['methods']), 'u32')
    m['object-count'] = fw.restrict(len(env['objects']), 'u32')
    m['string-count'] = fw.restrict(len(m['strings']), 'u32')
    m['int64-count'] = fw.restrict(len(m['int64s']), 'u32')
    m['flt64-count'] = fw.restrict(len(m['flt64s']), 'u32')
    _env_pop_context(env)
    return node


def _init_method_map(m):
    m['labelmap'] = {}
    m['ins'] = 0
    m['inc'] = 0
    # NOTE: These properties can be overriden by pragmas.
    m['pragmas'] = {
        'limstack'      : 0,
        'limlocal'      : 0,
        'debugsym'      : 0,
        'debugset'      : False
    }
    m['eranges'] = []
    m['exceptions'] = []


def _make_type_glob(node):
    assert(type(node) == ast.Type)
    result = ('*' * node.depth) + node.id.value
    return result


def _make_sig_block(node):
    assert(type(node) == ast.Method)
    result = ''
    for i in range(0, len(node.args) -1):
        result += _make_type_glob(node.args[i]) + '/'
    if node.args:
        result += _make_type_glob(node.args[-1])
    if node.rtype:
        result += ':'
        result += _make_type_glob(node.rtype)
    return result


def _make_field_block(node):
    assert(type(node) == ast.Object)
    result = ''
    for i in range(0, len(node.fields) - 1):
        result += _make_type_glob(node.args[i]) + '/'
    if node.args:
        result += _make_type_glob(node.args[-1])
    return result


@dispatch.when(ast.Method)
def visit(node, env=None):
    # NOTE: Preliminary context setup.
    _env_push_context(node, env)
    env['methods'].append(node)
    m = _env_fetch_create(node, env)
    _init_method_map(m)
    env['active-method-map'] = m
    # Iterate over method body.
    node.body = acm.visitlist(node.body, visit, env)
    # Generate a signature block for the arguments and return type.
    typeblock = _make_sig_block(node)
    # Compute flag metadata.
    m['status-0'] = {
        'isvoid'    : (node.rtype == None),
        'noparams'  : (len(node.args) == 0),
        'nothrow'   : (len(m['exceptions']) == 0),
        'debugsym'  : m['pragmas']['debugset']
    }
    # NOTE: Not all data prepared, some NONE entries for completeness.
    m['status-1'] = {}
    m['name-string'] = _intern_str(node.id.value, env)
    m['debug-symbol'] = m['pragmas']['debugsym']
    m['signature-block'] = _intern_str(typeblock, env)
    m['stack-limit'] = m['pragmas']['limstack']
    m['local-limit'] = m['pragmas']['limlocal']
    m['ins-byte-count'] = fw.restrict(m['ins'], 'u32')
    m['ins-bytes'] = None
    m['ete-count'] = fw.restrict(len(m['exceptions']), 'u32')
    m['ete'] = m['exceptions']
    _env_pop_context(env)
    return node


@dispatch.when(ast.Object)
def visit(node, env=None):
    _env_push_context(node, env)
    env['objects'].append(node)
    env['active-object-map'] = _env_fetch_create(node, env)
    m = env['active-object-map']
    fieldstring = ''
    fieldblock = 0
    for field in node.fields:
        fieldstring += _make_type_glob(field)
    if fieldstring:
        fieldblock = _intern_str(fieldstring, env)
    # NOTE: Setting properties as per the bytecode format.
    m['name-string'] = _intern_str(node.id.value, env)
    m['field-block'] = fieldblock
    _env_pop_context(env)
    return node


# NOTE: Whether or not an argument is not required/optional/required.
_arg_n    = 0
_arg_o    = 1
_arg_y    = 2


_arg_parse_map = {


}


_module_pmap = {}


_method_pmap = {
    
    # NAME          TYPE            WIDTH       REQUIRED    DEFAULT
    'debugsym'  : ( 'string',       None,       _arg_y,     None    ),
    'limstack'  : ( 'int',          'u8',       _arg_y,     None    ),
    'limlocal'  : ( 'int',          'u8',       _arg_y,     None    )

}


_object_pmap = {}


def _parse_pragma_arg(node, ptype, pwidth, env):
    assert(ptype in ['symbol', 'int', 'flt', 'string'])
    result = None
    if ptype == 'symbol' or ptype == 'string':
        result = _intern_str(node.value, env)
        return result
    elif ptype == 'int':
        result = _cast_to_integer(node)
    elif ptype == 'flt':
        result = _cast_to_float(node)
    if pwidth:
        result = fw.restrict(result, pwidth)
    assert(result != None)
    return result
    

def _handle_module_pragmas(node, env):
    err.fatal('No module level pragmas yet.')
    return


def _insert_pragma_value(k, v, m):
    assert(k in m['pragmas'])
    m['pragmas'][k] = v
    return


def _handle_method_pragmas(node, env):
    k = node.id.value
    if not k in _method_pmap:
        err.fatal('Unrecognized method pragma:', node.id)
    m = env['active-method-map']
    ptype, pwidth, preq, pdefault = _method_pmap[k]
    # NOTE: Check to see if we don't take an arg.
    if node.arg and preq == _arg_n:
        err.fatal('Pragma', node.id, 'does not take value', node.arg)
        return
    if not node.arg and preq == _arg_y:
        err.fatal('Pragma', node.id, 'requires value')
        return
    if not node.arg and preq == _arg_n:
        v = True
        _insert_pragma_value(k, v, m)
        return
    if not node.arg and preq == _arg_o:
        v = pdefault
        _insert_pragma_value(k, v, m)
        return
    if node.arg:
        v = _parse_pragma_arg(node.arg, ptype, pwidth, env)
        _insert_pragma_value(k, v, m)
        return
    assert('Should never reach here.' == None)
    return


def _handle_object_pragmas(node, env):
    err.fatal('No object level pragmas yet.')
    return


@dispatch.when(ast.Pragma)
def visit(node, env=None):
    _accepted = [ ast.Module, ast.Method, ast.Object ]
    assert(_env_in_oneof(_accepted, env))
    if _env_in_module(env):
        _handle_module_pragmas(node, env)
    elif _env_in_method(env):
        _handle_method_pragmas(node, env)
    elif _env_in_object(env):
        _handle_object_pragmas(node, env)
    else:
        assert('Should never reach here.' == None)
    return None


@dispatch.when(ast.Label)
def visit(node, env=None):
    m = env['active-method-map']
    lmap = m['labelmap']
    assert(not node.id.value in lmap)
    lmap[node.id.value] = m['ins']
    return None


@dispatch.when(ast.Try)
def visit(node, env=None):
    result = ast.Group()
    m = env['active-method-map']
    start = m['ins']
    result.children += acm.visitlist(node.body, visit, env)
    end = m['ins']
    erange = (start, end)
    m['eranges'].append(erange)
    node.handlers = acm.visitlist(node.handlers, visit, env)
    for handler in node.handlers:
        # All except blocks now converted to groups of instructions!
        assert(isinstance(handler, ast.Group))
        result.children += handler.children
    m['eranges'].pop()
    return result


# Add an entry to the exception table for the current method.
def _add_exception_entry(node, env):
    m = env['active-method-map']
    index = _intern_str(node.what.value, env)
    target = m['ins']
    start, end = m['eranges'][-1]
    # NOTE: As per the bytecode format!
    entry = (index, start, end, target)
    m['exceptions'].append(entry)


@dispatch.when(ast.Except)
def visit(node, env=None):
    result = ast.Group()
    _add_exception_entry(node, env)
    result.children += acm.visitlist(node.body, visit, env)
    return result


@dispatch.when(ast.Instruction)
def visit(node, env=None):
    result = None
    width = 0
    if not tt.has_immediate(node.opcode.toktype):
        if node.arg:
            err.fatal('Opcode:', node, 'cannot have arg:', node.arg)
        result = _validate_noi(node, env)
    else:
        for predicate, validator, bts in _immediate_lookup_table:
            if predicate(node.opcode.toktype):
                assert(node.arg)
                result = validator(node, env)
                width = bts
                break
    m = env['active-method-map']
    result.ins = m['ins']
    m['ins'] += width + 1
    m['inc'] += 1
    return result

