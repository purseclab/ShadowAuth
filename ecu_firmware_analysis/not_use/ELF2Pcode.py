from pypcode import Arch, Context, PcodePrettyPrinter

def print_arch():
  langs = {l.id:l for arch in Arch.enumerate() for l in arch.languages}
  for langid in sorted(langs):
    print('%-35s - %s' % (langid, langs[langid].description))
    pass

def run(long, elf_name, output_filename, base, code_offset, codesize, langid):
  langs = {l.id:l for arch in Arch.enumerate() for l in arch.languages}
  with open(input_elf_name, 'rb') as f:
    f.seek(code_offset)
    code = f.read()

  ctx = Context(langs[langid])
  res = ctx.translate(code, base, codesize, bb_terminating=False)

  f = open(output_filename, "w")
  i = 0
  for insn in res.instructions:
    i += 1
    print (f'{i}/{len(res.instructions)}')
    if long:
      f.write('-' * 80)
      f.write("\n")
      f.write('%08x/%d: %s %s' % (insn.address.offset, insn.length, insn.asm_mnem, insn.asm_body))
      f.write("\n")
      f.write('-' * 80)
      f.write("\n")
      for op in insn.ops:
        # print('%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op)))
        a = '%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op))
        # print(a)
        f.write(a)
        f.write("\n")
    else: #SHORT
      if len(insn.ops) > 0:
        f.write(PcodePrettyPrinter.fmt_op(insn.ops[-1]))
    # print('')
    f.write("\n")  
    # input()
  f.close()

  if res.error:
    print('** An error occured during translation: ' + repr(res.error))


# str
# long = False
# input_elf_name = "str.elf"
# output_filename = "str/out9.txt"
# base = 0x8000000 + 0x4e04
# code_offset = 52 + 0x4e04
# codesize = 28556
# langid = "ARM:LE:32:Cortex"
# str

# ms3
# long = False
# input_elf_name = "ms3.elf"
output_filename = "ms3/out9.txt"
base = 0x8000000 + 0x4e04
code_offset = 52 + 0x4e04
codesize = 28556
langid = "ARM:LE:32:Cortex"
# ms3

# # rusefi
# long = True
# input_elf_name = "rusefi.elf"
# output_filename = "out9.txt"
# base = 0x8000000 + 0x4e04
# code_offset = 52 + 0x4e04
# codesize = 28556
# langid = "ARM:LE:32:Cortex"
# # rusefi

# langid = "x86:LE:64:default"
# langid = "68000:BE:32:Coldfire"
# langid = "68000:BE:32:MC68020"
# langid = "68000:BE:32:MC68030"
# langid = "68000:BE:32:default"
# langid = "HC05:BE:16:M68HC05TB"
# langid = "HC05:BE:16:default"
# langid = "HC08:BE:16:MC68HC908QY4"
# langid = "HC08:BE:16:default"
# langid = "HCS08:BE:16:MC9S08GB60"
# langid = "HCS08:BE:16:default"
# langid = "HCS12:BE:24:default"
# langid = "ARM:LE:32:v4"
# langid = "ARM:LE:32:Cortex" # FOR STR
# langid = "ARM:LE:32:v4t"
# langid = "ARM:LE:32:v5"
# langid = "ARM:LE:32:v5t"
# langid = "ARM:LE:32:v6"
# langid = "ARM:LE:32:v7"
# langid = "ARM:LE:32:v8"
# langid = "ARM:LE:32:v8T"
# langid = "ARM:LEBE:32:v7LEInstruction"
# langid = "ARM:LEBE:32:v8LEInstruction"

run(long, input_elf_name, output_filename, base, code_offset, codesize, langid)