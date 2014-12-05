//useage:
// 
//    ct=$( '#myCanvas')[0].getContext("2d")
//    can =  canvas.createNew( );
//    can.ctx=ct
var canvas={ }
canvas.createNew=function()
{
    var obj       = { }
    var timer_space   = 100;
    var move_fun_list = [];
    var callback      = [];
    obj.width     = 10;
    obj.line      = function( x,y,offset_x,offset_y)
    { 
        this.ctx.beginPath();
        this.ctx.moveTo(x,y);
        this.ctx.lineWidth=obj.width;
        this.ctx.lineTo(offset_x,offset_y);
        this.ctx.stroke();
    }

    obj.move_fun=function( )
    { 
        return 0;
    }

    obj.move=function()
    { 
        timer=setInterval(function()
        {
            if(move_fun_list.length==0)
            {
                if(callback.length>0){
                    callback.shift()();

                }else{
                    clearInterval(timer);
                }
            }else
            {
                back=move_fun_list[0]()
                if(back<1){
                    move_fun_list.shift()
                }
            }
        },this.timer_space)
    }


    obj.draw_line=function(x,y,offset_x,offset_y,time )
    { 
        back=function( ){
            var n             = time*timer_space;
            var x_space       = (offset_x-x)/n;
            var y_space       = (offset_y-y)/n;
            var back          = n
            draw_line_fun = function( ){
                obj.line( x,y,x+x_space,y+y_space);
                x    = x+x_space;
                y    = y+y_space;
                back = back -1
                return back
            }
            return draw_line_fun;
        }
        move_fun_list.push(back())

    }
    obj.callback=function(back )
    { 
        callback.push( back)

    }
    return obj;
}
        //f = {}

        //f.createNew = function(){
        //    obj={}
        //    n                 = time*timer_space;
        //    x_space           = (offset_x-x)/n;
        //    y_space           = (offset_y-y)/n;
        //    back              = n
        //    obj.main = function( ){
        //            obj.line( x,y,x+x_space,y+y_space);
        //            x    = x+x_space;
        //            y    = y+y_space;
        //            back = back -1
        //                return back
        //        }
        //    return obj

        //}
        //back        = function(){

        //}
        //move_fun_list.push(back())
