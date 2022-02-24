from pypcode import Arch, Context, PcodePrettyPrinter

class Section:
  name = None
  base = None
  offset = None
  size = None
  def __init__(self, name, base, offset, size):
    self.name = name
    self.base = base
    self.offset = offset
    self.size = size

sections = {
  ".text": Section(".text", 0xc000, 24576, 8130),
  ".text3": Section(".text3", 0x4000, 12288, 12823),
  ".texte0": Section(".texte0", 0x390000, 65536, 2818),
  ".textf0": Section(".textf0", 0x3d0000, 69632, 16063),
  ".textf1": Section(".textf1", 0x3d4000, 86016, 15736),
  ".textf2": Section(".textf2", 0x3d8000, 102400, 15094),
  ".textf3": Section(".textf3", 0x3dc000, 118784, 15981),
  ".textf4": Section(".textf4", 0x3e0000, 135168, 16146),
  ".textf5": Section(".textf5", 0x3e4000, 151552, 15770),
  ".textf6": Section(".textf6", 0x3e8000, 167936, 16029),
  ".textf7": Section(".textf7", 0x3ec000, 184320, 16202),
  ".textf8": Section(".textf8", 0x3f0000, 200704, 15590),
  ".textf9": Section(".textf9", 0x3f4000, 217088, 16118),
  ".textfa": Section(".textfa", 0x3f8000, 233472, 14419),
  ".textfb": Section(".textfb", 0x3fc000, 249856, 16179),
  ".textfc": Section(".textfc", 0x400000, 266240, 14663),
  ".textfe": Section(".textfe", 0x408000, 282624, 15384)
}

def row2_to_int(hexstr):
  h = f"0x{hexstr}"
  return int(h, 16)

ff = ""
def lifting(name, base, offset, size):
  LONG = False

  binary = "./elfs/ms3.elf"

  if LONG is True:
    ff = open(f"ms3_pcode_long.txt", "w")

  langs = {l.id:l for arch in Arch.enumerate() for l in arch.languages}
  for langid in sorted(langs):
    # print('%-35s - %s' % (langid, langs[langid].description))
    pass

  langid = "HCS12:BE:24:default"

  with open(binary, 'rb') as f:
    f.seek(offset)
    code = f.read()


  print('%-35s - %s' % (langid, langs[langid].description))

  ctx = Context(langs[langid])
  res = ctx.translate(code, base, size, bb_terminating=False)

  if LONG is False:
    ff = open(f"ms3_w_addr/{name}.txt", "w")
  i = 0
  for insn in res.instructions:
    i += 1
    print (f'{i}/{len(res.instructions)}')
    if LONG:
      ff.write('-' * 80)
      ff.write("\n")
      ff.write('%08x/%d: %s %s' % (insn.address.offset, insn.length, insn.asm_mnem, insn.asm_body))
      ff.write("\n")
      ff.write('-' * 80)
      ff.write("\n")
      for op in insn.ops:
        # print('%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op)))
        a = '%3d: %s' % (op.seq.uniq, PcodePrettyPrinter.fmt_op(op))
        # print(a)
        ff.write(a)
        ff.write("\n")
    else: #SHORT
      for op in insn.ops:
        ff.write('%08x ' % (insn.address.offset))
        ff.write(PcodePrettyPrinter.fmt_op(op))
        ff.write("\n")
    # print('')
    ff.write("\n")
    # input()
  ff.close()

  if res.error:
    print('** An error occured during translation: ' + repr(res.error))


def main():
  with open("elfs/ms3.elf.map", "r") as f:
    for line in f:
      row = line.split(" ")
      section = sections.get(row[1], None)
      print(row2_to_int(row[3]))
      offset = section.offset + (row2_to_int(row[2]) - section.base)
      lifting(row[2], row2_to_int(row[2]), offset, row2_to_int(row[3]))


if __name__ == "__main__":
  main()