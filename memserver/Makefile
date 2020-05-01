all: ../dumps/webkit.elf ../dumps/libc.elf ../dumps/libkernel.elf

../dumps/webkit.bin:
	mkdir -p ../dumps
	echo 'Estimated download size: 25 MB'
	python3 dump_module.py -1 ../dumps/webkit.bin

../dumps/libc.bin:
	mkdir -p ../dumps
	echo 'Estimated download size: 1.2 MB'
	python3 dump_module.py 582 ../dumps/libc.bin

../dumps/libkernel.bin:
	mkdir -p ../dumps
	echo 'Estimated download size: 300 KB'
	python3 dump_module.py 705,-0x10000 ../dumps/libkernel.bin

../dumps/%.asm: ../dumps/%.bin
	printf 'section .text\nuse64\nincbin "$<"' > $@

../dumps/%.o: ../dumps/%.asm
	yasm -f elf64 $< -o $@

../dumps/%.elf: ../dumps/%.o
	ld --no-check-sections -nostdlib -static -Ttext=0 $< -o $@
