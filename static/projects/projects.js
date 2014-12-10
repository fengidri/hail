var Cfgs = {};
var CfgName;
function getCfgnames()
{
    var cfgnames;
    $.ajax({
        url:'/projects/configs', 
        async:false,
        success:function(_cfgnames){ 
            cfgnames = _cfgnames;
        }
    });
    return cfgnames;

}
function getCfgs(cfgnames)
{
    var Cfgs = {};
    for (var id in cfgnames)
    {
        $.ajax({
            url:'/projects/configs/' + cfgnames[id], 
            async:false,
            success:function(cfg){ 
                var name = cfgnames[id];
                Cfgs[name] = cfg;
            }
        });
    }
    return Cfgs;
}


function structCfgUi(cfg)
{
    var cfgstruct = $('div#cfgstruct');
    var readonly;
    if (cfg) readonly = true;
    else readonly = false;
    cfgstruct.find('input').attr('readonly', readonly);
    cfgstruct.find('input').val('');

    if (!cfg) return cfgstruct;

    CfgName = cfg.name;
    if (cfg.name) cfgstruct.children('input#name').val(cfg.name);

    var src_path = cfgstruct.children('#src_path');
    var sub_src_path = src_path.children('#sub_src_path');
    if (cfg.src_path.length > 1)
    {
        for (var i=0; i < cfg.src_path.length - 1; ++i)
            src_path.append(sub_src_path.clone());
    }

    sub_src_path = src_path.children('#sub_src_path');
    for (i in cfg.src_path)
    {
        var sub = sub_src_path.eq(i);
        var info = cfg.src_path[i];
        sub.children('#name').val(info.name);
        sub.children('#path').val(info.path);
        sub.children('#cmp_path').val(info.cmp_path);
    }


    if (cfg.compile_info){
        var compile_info = cfgstruct.children('#compile_info');
        compile_info.children('#host').val(cfg.compile_info.host);
        compile_info.children('#user').val(cfg.compile_info.user);
        compile_info.children('#pwd').val(cfg.compile_info.pwd);
        compile_info.children('#port').val(cfg.compile_info.port);
        compile_info.children('#srcs').val(cfg.compile_info.srcs);
    }
    if(cfg.events)
    {
        var events = cfgstruct.children('#events');
        if(cfg.events.Enter)
            events.children('#Enter').val(events.Enter);

        if(cfg.events.Leave)
            events.children('#Leave').val(events.Leave);
    }
    return cfgstruct;
}

function init_list()
{
    var list =  $('#list');
    var button = $('<button>');
}

function getcfg(name)
{
    for (var id in Cfgs)
    {
        if (Cfgs[id].name === name)
        {
            return Cfgs[id];
        }
    }
}
function getID(name)
{
    for (var id in Cfgs)
    {
        if (Cfgs[id].name === name)
        {
            return id;
        }
    }
}
$(document).ready(function(){
    var names = getCfgnames();
    Cfgs = getCfgs(names);
    for (var id in Cfgs)
    {
        var info = Cfgs[id];
        var t = $('<button>').text(info.name);
        $('div#list').append(t);
    }
    $('#list button').click(function(){
        var ID = $(this).text();
        if (!ID) return ;
        var info = getcfg(ID);
        structCfgUi(info);
    });
    $('button#delete').click(function()
    {
        var CfgID = getID(CfgName);
        if (!CfgID)
        {
            alert('NOT SELECT CFG');
            return;
        }

        $.ajax({
            type:'DELETE',
            url: '/projects/configs/' + CfgID,
            success:function()
            {
                alert('Delete Success');
                location = location;
            }
        });

    });

});
