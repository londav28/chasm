# PARSER GRAMMAR


<pre>

Module = {"$" Pragma | "method" Method | "object" Object}

Pragma = Symbol ["=" (Int | Hex | Flt | Symbol) ] ";"

Method = Symbol "<" [Type {"," Type}] ">" ( Type | "void" ) "{" Statement* "}"

Object = Symbol "{" [Type {"," Type}] "}"

Symbol = ```

Type = Symbol {"*"}

Statement = "$" Pragma | "@" Label | Instruction | "try" Try

Int = ```

Hex = ```

Flt = ```

Label = Symbol ":"

Instruction = Opcode [ Int | Hex | Flt | Str | Symbol ]

Try = "{" Statement* "}" "except" Except { "except" Except }

Except = Symbol "{" Statement* "}"

Opcode = (See opcode listing for mnemonics!)

</pre>