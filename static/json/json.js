function type(v)
{
    if (v == null)
        return "null";
    var t = typeof v;
    if (t == "object")
    {
        if (Array.isArray(v))
            t = 'array';
    }
    return t;

}

function dump(json, div)
{
    _dump(json, div)
}

function _dump(json, div)
{
    var t = type(json);
    var v = $('<div>');

    v.attr('id', t);
    v.css('margin-left', '2em');
    switch(t)
    {
        case "string":
        case "null":
        case "number":
        case "boolean":
            v.text(json);
            div.append(v);
            break;

        case "array":
            div.append(v);
            v.append($('<div>').text('['));
            for (i in json)
            {
                _dump(json[i], v)
            }
            v.append($('<div>').text(']'));
            break;
        case "object":
            div.append(v);
            v.append($('<div>').text('{'));

            var kv = $('<table>');
            kv.css('margin-left', '2em');
            for (i in json)
            {
                var tr = $('<tr>');
                var td = $('<td>');
                td.text(i);
                td.attr('id', 'key');
                tr.append(td);

                var td = $('<td>');
                _dump(json[i], td)
                tr.append(td);
                kv.append(tr);
            }
            v.append(kv);
            v.append($('<div>').text('}'));
            break;
    }
}
