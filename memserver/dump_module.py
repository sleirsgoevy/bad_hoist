import sys, threading, signal, os

print('Navigate the PS4 web browser to port 8080 on this PC')
print('(or just press OK if you are already on error screen)')
print('When you hit the error screen (again), press Enter on this PC.')

from client import read_mem, read_ptr, tarea

some_func = read_ptr(read_ptr(read_ptr(tarea+0x18)))

if ',' in sys.argv[1]:
    idx = int(sys.argv[1].split(',')[0])
    offset0 = int(sys.argv[1].split(',')[1], 16)
else:
    idx = int(sys.argv[1])
    offset0 = 0

if idx < 0:
    got_func = some_func
else:
    plt = some_func - 10063176
    plt_entry = plt + idx * 16
    q = read_mem(plt_entry, 6)
    assert q[:2] == b'\xff%', q
    got_entry = plt_entry + 6 + int.from_bytes(q[2:], 'little')
    got_func = read_ptr(got_entry)

got_func += offset0

data = b''

chunk_sz = 1

def watchdog_thread():
    input()
    os.kill(os.getpid(), signal.SIGINT)

threading.Thread(target=watchdog_thread, daemon=True).start()

try:
    while True:
        data += read_mem(got_func + len(data), chunk_sz)
        if chunk_sz < 1024:
            chunk_sz *= 2
        print(len(data), end=' bytes loaded\r')
except KeyboardInterrupt:
    print('\nKeyboardInterrupt')

if len(sys.argv) > 2:
    print('saving to', sys.argv[2])
    with open(sys.argv[2], 'wb') as file: file.write(data)
