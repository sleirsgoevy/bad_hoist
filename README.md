# PS5 WebKit ROP

This is a ROP toolchain for the PS5's web browser, based on the FontFace type confusion vulnerability. Works on firmware 4.03.

## ROP compiler setup

In order to run the ROP compiler you need to have dumps of WebKit, libc & libkernel.

You will need userland binaries to use this. Obtain them using [this payload](https://github.com/sleirsgoevy/ps4jb-payloads/tree/bd-jb/ps5-self-dumper/).

Dependencies: `python3`, `gcc`, `ROPgadget`

## Assembly-like ROP format

This toolchain uses assembly-like ROP format that is briefly described below.

`<label>:`

Declare a label. Labels are global and should be valid Python identifiers.

`<asm_instr>`

Find a gadget that looks like `asm_instr ; ret` and insert its address. Will error out if the gadget is not found inside the dumps.

Note: after dumping you can find a `dumps/gadgets.txt` file.

`# comment`

For each line, every character after the first # is considered a comment.

`db <expr>`

`(<expr>)` must be a valid Python expression that evaluates to a collection of integers in `range(256)`. The corresponding bytes will be written into the ropchain.

Examples: `db 1, 2, 3`, `db bytes(256)`

`dq <expr>`

`<expr>` must be a valid Python expression that evaluates to an integer. The integer will be written into the ropchain as a 64-bit little-endian value.

`dp <expr>`

Same as above, but `<expr>` should evaluate to an offset from the start of the ropchain. This will result in an absolute address being written.

For example, the commands

```
pop rsp
dp label_to_jump_to
```

will perform a jump.

`$<expr>`

`<expr>` should be a **JavaScript** expression that evaluates to an integer. The expression will be executed inside the exploited WebKit and the result will be written into the ropchain as a 64-bit little-endian value.

Example: `$infloop_addr`

**Note: in JavaScript numbers only have 52-bit precision.**

`$$<expr>`

`<expr>` will be inserted into the resulting JavaScript code literally.

If `<expr>` reads **exactly** `pivot(ropchain);`, the final pivot statement will be omitted.

Example:

```
$$function(some_params)
$${
...ropchain...
$$pivot(ropchain);
$$}
```

See examples of this language in the `rop/` directory.

## ROP compiler usage

`usage: python3 rop/compiler.py <rop_source> <gadgets.txt> > <rop_js>`

`<rop_source>` is the ropchain source code in the format described above.

`<gadgets.txt>` should point to `dumps/gadgets.txt` (or an alternative gadgets file in the same format).

`<rop_js>` is the resulting JavaScript file that should be executed.

## Running ropchains

To run a compiled ROP chain, add the corresponding `<script>` tag to the end of `index.html`, then load that page in the PS4 web browser.
