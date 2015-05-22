function savecfg(){
    localStorage.redis_host = $('input#host').val();
    localStorage.redis_port = $('input#port').val();
    localStorage.redis_db   = $('input#db').val();
    localStorage.filter = $('input#filter').val();
}

function loadcfg(){
    var host = localStorage.redis_host;
    var port = localStorage.redis_port;
    var db = localStorage.redis_db;
    var filter = localStorage.filter;
    if (host == null) host = '127.0.0.1';
    if (port == null) port = 6379;
    if (db   == null) db = 0;
    if (filter == null) filter = "*"
    $('input#host').val(host);
    $('input#port').val(port);
    $('input#db').val(db);
    $('input#filter').val(filter);
}
function redis_localtion(){
    var host = $('div#setting input[name=host]').val();
    var port = $('div#setting input[name=port]').val();
    var db = $('div#setting input[name=db]').val();
    var filter = $('div#setting input[name=filter]').val();

    return "/redis/" + host + "/" + port + "/" + db + '/';
}
function get()
{
    $(this).parent().find('li').css('color', 'black');
    $(this).css('color', 'blue');

    var key = $(this).text();
    var value = $('div#value').html('');

    var value_type = $('div#content span#type').html('');
    var value_key  = $('div#content span#key').html('');
    var value_num  = $('div#content span#num').html('');
    var msg        = $('#info #msg').html('loading  ...');


    $.ajax({
        url: redis_localtion() + "KEYS/" + key,
        dataType: "json",
        async:false,
        success: insert_val,
    })
    ////////////////////////////////////////////////////////////////////////////
    function insert_val(data)
    {
        msg.html('');
        value_type.text(data.type);
        value_key.text(key);

        switch(data.type)
        {
            case 'none': break;
            case 'string':
                value.html(data.value);
                break;
            default:
                var t = $("<table>");
                var l = 0;
                for (k in data.value){
                    var tr = $("<tr>");
                    tr.append($("<td>").text(k));
                    tr.append($("<td>").text(data.value[k]));
                    t.append(tr);
                    l += 1;
                }
                value.append(t);
                value_num.html(l);

                if (data.type != 'hash'){
                    t.attr('class', 'index_table');
                }
        }
    }

}

function refresh(){
    var filter = $('div#setting input[name=filter]').val();
    var url = redis_localtion()+"KEYS?filter="+ encodeURIComponent(filter)

    var msg = $('div#keys #msg').html('');
    var list = $("div#keys ul").html('');
    var num = $('div#keys #num').html('');

    var height = document.body.clientHeight - $('div#keys').offset().top;
    $('div#keys').css('height', height - 10);

    var value = $('div#value');
    var height = document.body.clientHeight - value.offset().top;
    value.css('height', height - 60);

    flush_value();

    if(filter == ""){
        msg.html("waring: filter is empty!<br>");
    }

    $.ajax({
        url: url,
        dataType: "json",
        async:false,
        success: function(data){
            if(!data.status)
            {
                $('div#keys #msg').append('连接出错......');
                return;
            }
            num.html('Num: ' + data.data.length);
            data = data.data;
            for( i in  data){
                var k = data[i];
                var s = $("<li>").text(k);
                s.click(get);
                list.append(s);
            }
            var content = $('div#content');
            var width = document.body.clientWidth - content.offset().left;
            content.css("width",width - 100);
        },
    })
}

function flushdb(){
    if(!confirm("确定清空当前数据库？")) return;

    var url = redis_localtion() + "DB";
    $.ajax({
        url: url,
        type: "delete",
        async:false,
        success:function(data){
            refresh( );
        },
        error:function(textStatus){
            alert(textStatus);
            refresh( );

        }
    });
}

$(document).ready(function(){
    loadcfg();

    refresh();
    $('#refresh').click(refresh);
    $('input#host, input#port, input#db').blur(savecfg);
    $('#flushdb').click(flushdb);
    $('#delete').click(delete_key);
})
function delete_key(){
    var url = redis_localtion();
    var keys = $("div#content #key").text();

    if(!confirm("确定删除key:" + keys)) return;

    url += "KEYS?key=" + encodeURIComponent(keys);
    $.ajax({
        url: url,
        type:"delete",
        success:function(data){
            alert("删除成功！");
            refresh();
        },
        error:function(textStatus){
            alert(textStatus);
            refresh();
        }
    });
}

function flush_value()
{
    var value = $('div#value');
    var key = $("div#info span#key");
    var type = $("div#info span#type");
    var num = $("div#info span#num");
    value.html('');
    key.html('');
    type.html('');
    num.html('');
}
