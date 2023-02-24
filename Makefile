ALARM ?= beep # will be called each time user interaction is needed

all: dumps/gadgets.txt dumps/syscalls.txt rop/relocator.txt

dumps/webkit-gadgets.txt: elfs/webkit.elf
	mkdir -p dumps
	ROPgadget --binary elfs/webkit.elf --dump > dumps/webkit-gadgets.txt

dumps/libc-gadgets.txt: elfs/libc.elf
	mkdir -p dumps
	ROPgadget --binary elfs/libc.elf --dump > dumps/libc-gadgets.txt

dumps/gadgets.txt: dumps/webkit-gadgets.txt dumps/libc-gadgets.txt
	cd dumps; grep '' webkit-gadgets.txt libc-gadgets.txt > gadgets.txt

dumps/syscalls.txt: elfs/libkernel.elf
	mkdir -p dumps
	objdump -D elfs/libkernel.elf | python3 rop/syscalls.py > dumps/syscalls.txt

rop/relocator.txt: dumps/gadgets.txt rop/relocator.rop
	python3 rop/compiler.py rop/relocator.rop dumps/gadgets.txt > rop/relocator.txt

clean:
	rm -rf dumps rop/relocator.txt
