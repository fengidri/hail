jQuery.fn.message_board=function( ){ 
    $( this).css( 'position','relative');
    var tag=$( this).children( 'div');
    tag.css( 'position','absolute');
    var space      = 10;
    var start_top  = $( this).offset( ).top + space;
    var start_left = $( this).offset( ).left + space;
    var width      = $( this).width( ) - 2* space;
    var height     = $( this).height( ) - 2 * space;
    tag.each( function(){ 
        $( this).css( { 'top':start_top + Math.random() * height,
            'left':start_left + Math.random( ) * width,
        })
    })



}
