var process;
var packinfo;
function proc_time_out()
{
    $("#upload_proc").text(process * 100 + "%");
    alert("call back");
    if (process === 1) return;
    alert("call back");
    setTimeout(proc_time_out, 200);
}
function startproc()
{
    alert("proc");
    $("#upload_proc").text("0%");
    setTimeout(proc_time_out, 200);
}
function upload_request(url, index, file, start, shardSize)
{

    var size = file.size;              //总大小
    var end = Math.min(size, start + shardSize);

    if (end === size) flag = -1; else flag = index;

    var form = new FormData();
    form.append("content", file.slice(start, end));  //slice方法用于切出文件的一部分
    form.append("filename", file.name);
    form.append("flag", flag); //当前是第几片
    if (flag == -1)
    {
        form.append("svn_log", packinfo.svn_log);
        form.append("name", packinfo.name);
        form.append("svn_branch", packinfo.svn_branch);
        form.append("version", packinfo.version);
        form.append("svn_num", packinfo.svn_num);
    }

    //Ajax提交
    $.ajax({
        url: url,
        type: "POST",
        data: form,
        async: true,        //异步
        processData: false,  //很重要，告诉jquery不要对form进行处理
        contentType: false,  //很重要，指定为false才能形成正确的Content-Type
        success: function(){
            if (flag === -1)
            {
                $("#upload_proc").text("100%");
            }
            else
            {
                index += 1;
                $("#upload_proc").text( parseInt(index * shardSize * 100 / size) + "%");
                upload_request(url, index, file, end, shardSize);
            }

        },
        error:function(xml, stat, error)
        {
            alert(stat + " " + error);
            return false;
        }
    });
}

function upload(url, file){

    var shardSize = 20 * 1024; 


    upload_request(url, 0, file, 0, shardSize);
    return ;
}

function read_json()
{
    var file = $("input#packinfo")[0].files[0]; //文件对象
    var reader = new FileReader();  
    //将文件以文本形式读入页面  
    reader.onload=function(f){  
        packinfo = $.parseJSON(this.result);
        $("label#packinfo").text(this.result);
        if (!packinfo.hasOwnProperty('name')) return ;
        if (!packinfo.hasOwnProperty('version')) return ;
        if (!packinfo.hasOwnProperty('svn_log')) return ;
        if (!packinfo.hasOwnProperty('svn_branch')) return ;
        if (!packinfo.hasOwnProperty('svn_num')) return ;
        $("input#packinfo").hide();
        $("input#file").show();
        $("label#file").show();
    };
    reader.readAsText(file);  

}
$(document).ready(function(){
    $("button#upload").hide();
    $("input#file").hide();
    $("input#file").hide();
    $("label#file").hide();
    

    $("input#packinfo").change(function(){
        read_json();
    });

    $("input#file").change(function(){
        $("button#upload").show();
    });
    $("button#upload").click(function(){
        $(this).hide();
        var file = $("input#file")[0].files[0]; //文件对象
        setTimeout(function(){
            upload("/upload", file);
        }, 100);
    });
});
