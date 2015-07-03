function fill_in(div_info, analy){
    div_info.find('#resource-td-2').text(analy.total);
    div_info.find('#cdn-td-2').text(analy.cdn);
    div_info.find('#gzip-td-2').text(analy.gzip);
    div_info.find('#loadtime-td-2').text(analy.loadtime/1000);
    div_info.find('#hosts-td-2').text(analy.hosts);
    div_info.find('#hit-td-2').text(analy.hit);
    div_info.find('#https-td-2').text(analy.https);

    var st = div_info.find('table#codes');
    st.html('');
    var tr = $('<tr>');
    tr.append($('<td>').text('状态码'));
    for (var i in analy.codes){
        tr.append($('<td>').text(i));
    }
    st.append(tr);

    var tr = $('<tr>');
    tr.append($('<td>').text('次数'));
    for (var i in analy.codes){
        tr.append($('<td>').text(analy.codes[i]));
    }
    st.append(tr);

    var s = analy.size;
    if (s > 1024 * 1024){
        s = s / 1024 / 1024;
        s = s.toFixed(2) + 'M';
    }
    else{
        s = s / 1024;
        s = s.toFixed(2) + 'K'
    }

    div_info.find('#size-td-2').text(s);
    div_info.show();
}
function fill_in_list(list)
{
    var tbody = $('#resources_list tbody');
    tbody.html('');
    for (var i in list)
    {
        var url = list[i][0];
        var size = list[i][1];
        var time = list[i][2];

        var tr = $('<tr>');
        var tt = $("<div style='overflow:scroll;'>").text(url);
        tr.append($('<td>').text(url));
        tr.append($('<td>').text(size));
        tr.append($('<td>').text(time));
        tbody.append(tr);
    }

}

function get_analy(ID){
    var msg    = $('#msg');
    var info   = $('#info');
    url = '/upyun/test?ID=' + ID
    $.ajax({
        url: url + "&_=analy",
        dataType: 'json',
        success: function(data){
            if (data.status == 'waiting'){
                setTimeout(get_anly, 500);
                return;
            }
            if (data.status == 'error'){
                msg = 'Open Url Fail!!'
                return;
            }
            if (data.status == 'complete'){
                msg.text('');
                fill_in(info, data);
                $('#render').show();
                $('#render #small').hide();
                $('#render #small').attr('src', url + '&_=render');
                $('#render #big').attr('src', url + '&_=render');
                $.ajax({
                    url: url + '&_=resource',
                    dataType: 'json',
                    success: fill_in_list
                });
            }
        },
        error: function(){
            msg.text('Error......');
        },
    });
}

function Test(){
    var url    = $('#testurl').val();
    var msg    = $('#msg');
    Clear();

    msg.text('Start Test......');
    $.ajax({
        url: '/upyun/test',
        data: {url: url},
        type: 'POST',
        success: function(id){
            msg.text('Load......');
            get_analy(id)
        },
        error: function(){
            msg.text('Error......');
        }
    });
}
function Clear(){
    $('#render').hide('');
    $('#codes').html('');
    $('#msg').html('');
    $('#info').hide();
}
function resize(obj, width){
    var w = width;
    var img_w = obj.width();//图片宽度
    var img_h = obj.height();//图片高度
    if(img_w>w){//如果图片宽度超出容器宽度--要撑破了
        var height = (w*img_h)/img_w; //高度等比缩放
        obj.css({"width":w,"height":height});//设置缩放后的宽度和高度
    }
}
$(document).ready(function(){
    $('#teststart').click(Test);
    $('#render #small').load(function(){
        resize($(this), 250);
        $(this).show();
    });
    $('#render #small').click(function(){
        resize($('#render #big'), document.body.clientWidth/2 - 20);
        layer.open({
            type: 1,
            title: false,
            closeBtn: false,
            area: [document.body.clientWidth/2, document.body.clientHeight/2],
            skin: 'layui-layer-nobg', //没有背景色
            shadeClose: true,
            content: $('#render #big')
        });
    });
});
