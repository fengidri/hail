jQuery.fn.clear_input = function(){
    //error in jquery
    this.each(function(){
        
        this.__original_val = $(this).val();
        $(this).css('color','grey');

        $(this).click(function(){
            if($(this).val() == this.__original_val){
                $(this).val('');
                $(this).css('color','black');
            }
        })
        $(this).blur(function(){

                if($(this).val()==''){
                    $(this).val(this.__original_val);
                    $(this).css('color','grey');
                }

            })
    })
    
}
jQuery.fn.form_send=function(){ 

    var arg=arguments;
    this[0].onsubmit=function(){
        var url=$( this).attr( 'action');
        var dict_send={ }
        $( this).children( 'input').each( function(index){ 
            dict_send[$(this).attr('name')]=$( this).val( )
        })
        $( this).children( 'textarea').each( function(index){ 
            dict_send[$(this).attr('name')]=$( this).val( )
        })

        if ( arg.lenght==0){ 
            $.post( url, dict_send )
        }else{
            $.post( url, dict_send ,arg[0])
        }
        return false; 
    }
}
//use
//$( 'click').float_show( '#target_div')
jQuery.fn.float_show=function(sel){
    var width=$(sel).width();
    var height=$(sel).height();
    var space=10;

    $(this).live('click',function(e){
        var sel_x = e.pageX + space;
        var sel_y = e.pageY + space;
        if(sel_x + width > $(window).width()){
            sel_x = sel_x - width;
        }
      //  if(sel_y + width> $(window).height()){
      //      sel_y = sel_y -height;
      //  }
        $(sel).css({'top':sel_y,'left':sel_x}).show()


        
    })
    $(sel).hover(
            function(){

            }
            ,
            function(){
                $(this).hide();

            }
            )


}
jQuery.fn.message_board=function( ){ 
    $( this).css( {'position':'relative',
        'width':$(this).parent().width(),
    'height':$(this).parent().height(),
    });

    var tag=$( this).children( 'div');
    tag.css( 'position','absolute');
    var space      = 100;
    var width      = $( this).width( ) - 2* space;
    var height     = $( this).height( ) - 2 * space;
    tag.each( function(){ 
        $( this).css( { 'top':Math.random() * height,
            'left': Math.random( ) * width,
        })
    })
}
