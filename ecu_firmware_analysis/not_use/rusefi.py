from pypcode import Arch, Context, PcodePrettyPrinter

# binary = "../ms3.elf"
# binary = "../hello.bin"
binary = "../rusefibuild/rusefi.elf"
base = 0x8026340

langs = {l.id:l for arch in Arch.enumerate() for l in arch.languages}
for langid in sorted(langs):
  print('%-35s - %s' % (langid, langs[langid].description))
  pass

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
langid="ARM:LE:32:Cortex"

with open(binary, 'rb') as f:
  f.seek(65536 + 0x26340)
  code = f.read()


print('%-35s - %s' % (langid, langs[langid].description))

ctx = Context(langs[langid])
res = ctx.translate(code, base, 280644, bb_terminating=False)

f = open("out.txt", "w")
i = 0
for insn in res.instructions:
  i += 1
  print (f'{i}/{len(res.instructions)}')
  # f.write('-' * 80)
  # f.write("\n")
  # f.write('%08x/%d: %s %s' % (insn.address.offset, insn.length, insn.asm_mnem, insn.asm_body))
  # f.write("\n")
  # f.write('-' * 80)
  # f.write("\n")
  # for op in insn.ops:
  #   # print('%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op)))
  #   a = '%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op))
  #   # print(a)
  #   f.write(a)
  #   f.write("\n")
  if len(insn.ops) > 0:
    f.write(PcodePrettyPrinter.fmt_op(insn.ops[-1]))
  # print('')
  f.write("\n")
  # input()
f.close()

if res.error:
  print('** An error occured during translation: ' + repr(res.error))