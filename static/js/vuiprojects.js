$(document).ready(
$.get("/vuiprojects",
        function(data){
           var list = $.parseJSON(data);
           var i;
           for (i in list){
               $('div#list').append(
                   "<button >" + list[i] + "</button>");
           }
           $("div#list button").click(function(){

               $.get("/vuiprojects/content/" + $(this).text() , 
                   function(data){
                       init_content($.parseJSON(data));

               })
           });
       }
   )
);

function init_content(json)
{
    content = $("div#content");
    var html = "";
    content.html("");
    html += "<div id='src_path'> ";
    for (var i in json.src_path)
    {
        var path = json.src_path[i].path;
        var name = json.src_path[i].name;
        html += "名称: <span>" + name + "</span><br />";
        html += "路径: <span>" + path + "</span><br />";
        html += "<br />";
    }
    html += "</div>";
    content.html(html);

}
