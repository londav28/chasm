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


import src.tokentype as tkt


keyword = {

    # Assembler opcodes, 1-to-1 mapping with CSM bytecode.
    'nop'           : tkt.t_op_nop,
    'ldl'           : tkt.t_op_ldl,
    'stl'           : tkt.t_op_stl,
    'ldg'           : tkt.t_op_ldg,
    'stg'           : tkt.t_op_stg,
    'lfd'           : tkt.t_op_lfd,
    'sfd'           : tkt.t_op_sfd,
    'ldsc'          : tkt.t_op_ldsc,
    'pop'           : tkt.t_op_pop,
    'swp'           : tkt.t_op_swp,
    'dup'           : tkt.t_op_dup,
    'psh_b'         : tkt.t_op_psh_b,
    'psh_s'         : tkt.t_op_psh_s,
    'psh_d'         : tkt.t_op_psh_d,
    'psh_q'         : tkt.t_op_psh_q,
    'psh_f'         : tkt.t_op_psh_f,
    'psh_a'         : tkt.t_op_psh_a,
    'psh_nil'       : tkt.t_op_psh_nil,
    'par_b'         : tkt.t_op_par_b,
    'par_s'         : tkt.t_op_par_s,
    'par_d'         : tkt.t_op_par_d,
    'par_q'         : tkt.t_op_par_q,
    'par_f'         : tkt.t_op_par_f,
    'par_a'         : tkt.t_op_par_a,
    'lai'           : tkt.t_op_lai,
    'sai'           : tkt.t_op_sai,
    'alen'          : tkt.t_op_alen,
    'and'           : tkt.t_op_and,
    'or'            : tkt.t_op_or,
    'xor'           : tkt.t_op_xor,
    'not'           : tkt.t_op_not,
    'shl'           : tkt.t_op_shl,
    'shr'           : tkt.t_op_shr,
    'add_q'         : tkt.t_op_add_q,
    'sub_q'         : tkt.t_op_sub_q,
    'mul_q'         : tkt.t_op_mul_q,
    'div_q'         : tkt.t_op_div_q,
    'mod_q'         : tkt.t_op_mod_q,
    'neg_q'         : tkt.t_op_neg_q,
    'add_f'         : tkt.t_op_add_f,
    'sub_f'         : tkt.t_op_sub_f,
    'mul_f'         : tkt.t_op_mul_f,
    'div_f'         : tkt.t_op_div_f,
    'mod_f'         : tkt.t_op_mod_f,
    'neg_f'         : tkt.t_op_neg_f,
    'cst_qf'        : tkt.t_op_cst_qf,
    'cst_fq'        : tkt.t_op_cst_fq,
    'cmp_q'         : tkt.t_op_cmp_q,
    'cmp_f'         : tkt.t_op_cmp_f,
    'refcmp'        : tkt.t_op_refcmp,
    'jmp_eqz'       : tkt.t_op_jmp_eqz,
    'jmp_nez'       : tkt.t_op_jmp_nez,
    'jmp_ltz'       : tkt.t_op_jmp_ltz,
    'jmp_lez'       : tkt.t_op_jmp_lez,
    'jmp_gtz'       : tkt.t_op_jmp_gtz,
    'jmp_gez'       : tkt.t_op_jmp_gez,
    'jmp'           : tkt.t_op_jmp,
    'typeof'        : tkt.t_op_typeof,
    'call'          : tkt.t_op_call,
    'ret'           : tkt.t_op_ret,
    'leave'         : tkt.t_op_leave,
    'break'         : tkt.t_op_break,
    'throw'         : tkt.t_op_throw,

    # Additional assembler keywords.
    'method'    : tkt.t_method,
    'object'    : tkt.t_object,
    'try'       : tkt.t_try,
    'except'    : tkt.t_except,
    'void'      : tkt.t_void
}


lkone = {

    # LL(1) formatting characters.
    '\n'        : tkt.t_newline,
    '\t'        : tkt.t_tab,

    # LL(1) braces and brackets.
    '('         : tkt.t_lparen,
    ')'         : tkt.t_rparen,
    '{'         : tkt.t_lbrace,
    '}'         : tkt.t_rbrace,
    '['         : tkt.t_lbracket,
    ']'         : tkt.t_rbracket,

    # LL(1) comparison operators.
    '<'         : tkt.t_less,
    '>'         : tkt.t_greater,

    # LL(1) punctuation characters.
    ';'         : tkt.t_semicolon,
    ','         : tkt.t_comma,
    '.'         : tkt.t_period,
    ':'         : tkt.t_colon,

    # LL(1) operators and meta symbols.
    '='         : tkt.t_assign,
    '*'         : tkt.t_star,
    '/'         : tkt.t_fslash,
    '%'         : tkt.t_percent,
    '&'         : tkt.t_amper,
    '@'         : tkt.t_at,
    '$'         : tkt.t_dollar
}

# unused for now!
lktwo = {}
