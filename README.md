# CHASM: ASSEMBLER FOR THE CSM VIRTUAL MACHINE

This was *supposed* to be a simple assembler. The machinery in this project
goes a bit overboard.

In particular, I decided to create a full AST and use AST transformations to
do the following:

- Transforming instructions to their exact widths
- Delayed resolution of jump targets

Any good assembler would want to collect labels while parsing (you'll need to
do at least two passes through the source, since you can jump to labels you
haven't seen yet).

I don't do that. For some reason I've become adverse to doing any form of
semantic analysis while parsing. Does it hurt performance? Yes. Do we care
about performance? No.

Any good assembler would also terminate statements with a newline instead of
a semicolon.

We terminate statements with a semicolon. We'll probably change this later.
Depends on how annoyed I get with it.

The lexer is more of a traditional lexer, and I try my hardest to emulate a
traditional C enumeration. It results in a bit more code compared to using
string values alone. It *feels right*, though, which is why I do it.

Since I went through the effort of building a full fledged parse tree and
doing transforms (even porting over my visitor pattern decorator), I figure
that I can implement a few compile time optimizations for this instruction
set in the future.

For now, though, it's still just a dumb assembler.
