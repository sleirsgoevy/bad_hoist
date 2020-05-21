import sys

def prepass(l):
    labels = {}
    sp_offset = 8
    for i in l:
        if i.endswith(':'):
            labels[i[:-1]] = sp_offset
        elif i.startswith('db '):
            q = bytes(list(eval('('+i[3:]+')')))
            assert len(q) % 8 == 0
            sp_offset += len(q)
        elif not i.startswith('$$'): sp_offset += 8
    return labels

def parse_gadgets(l):
    gadgets = {}
    for i in l:
        if i.count(':') < 2: continue
        file, addr, gadget = i.split(':', 2)
        assert file.endswith('-gadgets.txt')
        file = file[:-12]
        try: addr = int(addr, 16)
        except ValueError: continue
        gadget = gadget.strip()
        if gadget == 'ret': gadget = 'nop ; ret'
        if not gadget.endswith(' ; ret'): continue
        gadget = gadget[:-6].replace(' ptr ', ' ')
        gadgets[gadget] = (file, addr)
        for i in 'byte', 'word', 'dword', 'qword':
            gadget = gadget.replace(' '+i+' ', ' ')
            gadgets[gadget] = (file, addr)
    return gadgets

def final_pass(l, ls, gs):
    ans = []
    sp_offset = 8
    for i in l:
        if i.endswith(':'):
            ans.append('//'+i)
            continue
        elif i.startswith('$$'):
            ans.append(i[2:].replace('SP_OFFSET', str(sp_offset)))
            continue
        elif i == '$': pass
        elif i.startswith('$'):
            ans.append('write_ptr_at(ropchain+%d, %s);'%(sp_offset, i[1:]))
        elif i.startswith('dp '):
            offset = eval(i[3:], ls)
            ans.append('write_ptr_at(ropchain+%d, ropchain+%d); //%s'%(sp_offset, offset, i[3:]))
        elif i.startswith('dq '):
            data = eval(i[3:], ls)
            ans.append('write_mem(ropchain+%d, %r);'%(sp_offset, list((data & 0xffffffffffffffff).to_bytes(8, 'little'))))
        elif i.startswith('db '):
            data = bytes(list(eval('('+i[3:]+')')))
            assert len(data) % 8 == 0
            if any(data): ans.append('write_mem(ropchain+%d, %r);'%(sp_offset, list(data)))
            sp_offset += len(data)
            continue
        elif i in gs:
            file, offset = gs[i]
            ans.append('write_ptr_at(ropchain+%d, %s_base+%d); //%s'%(sp_offset, file, offset, i))
        else:
            raise SyntaxError(i)
        sp_offset += 8
    ans.insert(0, 'var ropchain = malloc(%d);'%sp_offset);
    if 'pivot(ropchain);' not in ans: ans.append('pivot(ropchain);')
    return '\n'.join(ans)

def read_gadgets(f):
    with open(f) as file: return list(file)

def read_asm(f):
    return [i for i in (i.split('#', 1)[0].strip() for i in read_gadgets(f)) if i]

def main(f, g):
    asm = read_asm(f)
    gadgets = parse_gadgets(read_gadgets(g))
    labels = prepass(asm)
    return final_pass(asm, labels, gadgets)

if __name__ == '__main__':
    print(main(*sys.argv[1:]))
