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


# Luckily module initialization code is only run once.
_enum_counter = 0
_enum_strs = []


# So that I can reorder enum values at will.
def _intern(string):
    global _enum_counter
    result = _enum_counter
    _enum_strs.append(string)
    _enum_counter += 1
    return result


# Fetch tokentype name from enum value.
def get_tokentype_str(toktype):
    if toktype >= 0 and toktype < len(_enum_strs):
        return _enum_strs[toktype]
    return None


# These must appear in _strict_ order corresponding to opcode value.
t_op_nop        = _intern('op:nop')
t_op_ldl        = _intern('op:ldl')
t_op_stl        = _intern('op:stl')
t_op_ldg        = _intern('op:ldg')
t_op_stg        = _intern('op:stg')
t_op_lfd        = _intern('op:lfd')
t_op_sfd        = _intern('op:sfd')
t_op_ldsc       = _intern('op:ldsc')
t_op_pop        = _intern('op:pop')
t_op_swp        = _intern('op:swp')
t_op_dup        = _intern('op:dup')
t_op_psh_b      = _intern('op:psh_b')
t_op_psh_s      = _intern('op:psh_s')
t_op_psh_d      = _intern('op:psh_d')
t_op_psh_q      = _intern('op:psh_q')
t_op_psh_f      = _intern('op:psh_f')
t_op_psh_a      = _intern('op:psh_a')
t_op_psh_nil    = _intern('op:psh_nil')
t_op_par_b      = _intern('op:par_b')
t_op_par_s      = _intern('op:par_s')
t_op_par_d      = _intern('op:par_d')
t_op_par_q      = _intern('op:par_q')
t_op_par_f      = _intern('op:par_f')
t_op_par_a      = _intern('op:par_a')
t_op_lai        = _intern('op:lai')
t_op_sai        = _intern('op:sai')
t_op_alen       = _intern('op:alen')
t_op_and        = _intern('op:and')
t_op_or         = _intern('op:or')
t_op_xor        = _intern('op:xor')
t_op_not        = _intern('op:not')
t_op_shl        = _intern('op:shl')
t_op_shr        = _intern('op:shr')
t_op_add_q      = _intern('op:add_q')
t_op_sub_q      = _intern('op:sub_q')
t_op_mul_q      = _intern('op:mul_q')
t_op_div_q      = _intern('op:div_q')
t_op_mod_q      = _intern('op:mod_q')
t_op_neg_q      = _intern('op:neg_q')
t_op_add_f      = _intern('op:add_f')
t_op_sub_f      = _intern('op:sub_f')
t_op_mul_f      = _intern('op:mul_f')
t_op_div_f      = _intern('op:div_f')
t_op_mod_f      = _intern('op:mod_f')
t_op_neg_f      = _intern('op:neg_f')
t_op_cst_qf     = _intern('op:cst_qf')
t_op_cst_fq     = _intern('op:cst_fq')
t_op_cmp_q      = _intern('op:cmp_q')
t_op_cmp_f      = _intern('op:cmp_f')
t_op_refcmp     = _intern('op:refcmp')
t_op_jmp_eqz    = _intern('op:jmp_eqz')
t_op_jmp_nez    = _intern('op:jmp_nez')
t_op_jmp_ltz    = _intern('op:jmp_ltz')
t_op_jmp_lez    = _intern('op:jmp_lez')
t_op_jmp_gtz    = _intern('op:jmp_gtz')
t_op_jmp_gez    = _intern('op:jmp_gez')
t_op_jmp        = _intern('op:jmp')
t_op_typeof     = _intern('op:typeof')
t_op_call       = _intern('op:call')
t_op_ret        = _intern('op:ret')
t_op_leave      = _intern('op:leave')
t_op_break      = _intern('op:break')
t_op_throw      = _intern('op:throw')

# Additional values to be used in the lexer/parser!
t_eof           = _intern('eof')
t_unknown       = _intern('unknown')

# Recognized whitespace tokens.
t_comment       = _intern('comment')
t_spaces        = _intern('spaces')

# LL(1) formatting characters.
t_newline       = _intern('newline')
t_tab           = _intern('tab')

# LL(1) braces and brackets.
t_lparen        = _intern('lparen')
t_rparen        = _intern('rparen')
t_lbrace        = _intern('lbrace')
t_rbrace        = _intern('rbrace')
t_lbracket      = _intern('lbracket')
t_rbracket      = _intern('rbracket')

# LL(1) comparison operators.
t_less          = _intern('less')
t_greater       = _intern('greater')

# LL(1) punctuation characters.
t_semicolon     = _intern('semicolon')
t_comma         = _intern('comma')
t_period        = _intern('period')
t_colon         = _intern('colon')

# LL(1) operators and meta symbols.
t_assign        = _intern('assign')
t_star          = _intern('star')
t_fslash        = _intern('fslash')
t_percent       = _intern('percent')
t_amper         = _intern('amper')
t_at            = _intern('at')
t_dollar        = _intern('dollar')

# Literal values.
t_int           = _intern('int')
t_str           = _intern('str')
t_flt           = _intern('flt')
t_hex           = _intern('hex')
t_bin           = _intern('bin')

# There's gonna be a whole lotta these!
t_symbol        = _intern('symbol')

# Additional assembler keywords.
t_method        = _intern('kw:method')
t_object        = _intern('kw:object')
t_try           = _intern('kw:try')
t_except        = _intern('kw:except')
t_void          = _intern('kw:void')


# Relies on opcode tokens being interned first!
def get_opcode_str(op):
    if op < t_op_nop or op > t_op_eox:
        return 'unknown'
    return get_tokentype_str(op)


_keywords = [
    t_method,
    t_object,
    t_try,
    t_except,
    t_void
]


_whitespace = [
    t_comment,
    t_spaces,
    t_newline,
    t_tab
]


_literals = [
    t_int,
    t_str,
    t_flt,
    t_hex,
    t_bin
]


_instruction = [
    t_op_nop,
    t_op_ldl,
    t_op_stl,
    t_op_ldg,
    t_op_stg,
    t_op_lfd,
    t_op_sfd,
    t_op_ldsc,
    t_op_pop,
    t_op_swp,
    t_op_dup,
    t_op_psh_b,
    t_op_psh_s,
    t_op_psh_d,
    t_op_psh_q,
    t_op_psh_f,
    t_op_psh_a,
    t_op_psh_nil,
    t_op_par_b,
    t_op_par_s,
    t_op_par_d,
    t_op_par_q,
    t_op_par_f,
    t_op_par_a,
    t_op_lai,
    t_op_sai,
    t_op_alen,
    t_op_and,
    t_op_or,
    t_op_xor,
    t_op_not,
    t_op_shl,
    t_op_shr,
    t_op_add_q,
    t_op_sub_q,
    t_op_mul_q,
    t_op_div_q,
    t_op_mod_q,
    t_op_neg_q,
    t_op_add_f,
    t_op_sub_f,
    t_op_mul_f,
    t_op_div_f,
    t_op_mod_f,
    t_op_neg_f,
    t_op_cst_qf,
    t_op_cst_fq,
    t_op_cmp_q,
    t_op_cmp_f,
    t_op_refcmp,
    t_op_jmp_eqz,
    t_op_jmp_nez,
    t_op_jmp_ltz,
    t_op_jmp_lez,
    t_op_jmp_gtz,
    t_op_jmp_gez,
    t_op_jmp,
    t_op_typeof,
    t_op_call,
    t_op_ret,
    t_op_leave,
    t_op_break,
    t_op_throw
]


_jump = [
    t_op_jmp_eqz,
    t_op_jmp_nez,
    t_op_jmp_ltz,
    t_op_jmp_lez,
    t_op_jmp_gtz,
    t_op_jmp_gez,
    t_op_jmp
]


_interned_arg = [
    t_op_psh_a,
    t_op_par_a,
    t_op_call,
    t_op_ldsc,
    t_op_psh_q,
    t_op_psh_f
]


_has_immediate_u8 = [
    t_op_ldl,
    t_op_stl
]


_has_immediate_u16 = [
    t_op_ldg,
    t_op_stg,
    t_op_lfd,
    t_op_sfd
]


_has_immediate_u32 = _jump + [
    t_op_psh_a,
    t_op_par_a,
    t_op_call,
    t_op_ldsc,
    t_op_psh_q,
    t_op_psh_f
]


_has_immediate_u64 = []


_has_immediate_i8 = [ t_op_psh_b ]


_has_immediate_i16 = [ t_op_psh_s ]


_has_immediate_i32 = [ t_op_psh_d ]


_has_immediate_i64 = []


_has_immediate_f32 = []


_has_immediate_f64 = []


_has_immediate = (
    _has_immediate_u8       +
    _has_immediate_u16      +
    _has_immediate_u32      +
    _has_immediate_u64      +
    _has_immediate_i8       +
    _has_immediate_i16      +
    _has_immediate_i32      +
    _has_immediate_i64      +
    _has_immediate_f32      +
    _has_immediate_f64
)


# Tokens that can have varying values.
_non_static = _literals + [t_symbol] + [t_comment] + [t_spaces]


def is_keyword(v):
    return v in _keywords


def is_literal(v):
    return v in _literals


def is_non_static(v):
    return v in _non_static


def is_whitespace(v):
    return v in _whitespace


def is_instruction(v):
    return v in _instruction


def is_jump(v):
    return v in _jump


def has_interned_arg(v):
    return v in _interned_arg


def has_immediate_u8(v):
    return v in _has_immediate_u8


def has_immediate_u16(v):
    return v in _has_immediate_u16


def has_immediate_u32(v):
    return v in _has_immediate_u32


def has_immediate_u64(v):
    return v in _has_immediate_u64


def has_immediate_i8(v):
    return v in _has_immediate_i8


def has_immediate_i16(v):
    return v in _has_immediate_i16


def has_immediate_i32(v):
    return v in _has_immediate_i32


def has_immediate_i64(v):
    return v in _has_immediate_i64


def has_immediate_f32(v):
    return v in _has_immediate_f32


def has_immediate_f64(v):
    return v in _has_immediate_f64


def has_immediate(v):
    return v in _has_immediate
