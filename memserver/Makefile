all: ../dumps/webkit.elf ../dumps/libc.elf ../dumps/libkernel.elf

../dumps/webkit.bin:
	mkdir -p ../dumps
	echo 'Estimated download size: 20 MB'
	CHUNK_SIZE=30408704 python3 dump_module.py -1,-0x900000 ../dumps/webkit.bin

../dumps/libc.bin:
	mkdir -p ../dumps
	echo 'Estimated download size: 1.2 MB'
	CHUNK_SIZE=300000 python3 dump_module.py 573 ../dumps/libc.bin

../dumps/libkernel.bin:
	mkdir -p ../dumps
	echo 'Estimated download size: 400 KB'
	CHUNK_SIZE=100000 python3 dump_module.py 789 ../dumps/libkernel.bin

../dumps/%.asm: ../dumps/%.bin
	printf 'section .text\nuse64\nincbin "$<"' > $@

../dumps/%.o: ../dumps/%.asm
	yasm -f elf64 $< -o $@

../dumps/%.elf: ../dumps/%.o
	ld --no-check-sections -nostdlib -static -Ttext=0 $< -o $@
