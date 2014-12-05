$( document).ready( function(){
    form_add = $( 'form#task_add_form' );
    form_add.hide( );
    $( 'div#task_add').click( function(){
        if( this.__input == undefined)
        {

            new_form= form_add.clone( true );
            new_form.find( '#date').val( $(this).parent().prev().html());
            new_form.find( 'input').clear_input( );
            
            this.__input = new_form;
            $(this).parent().append(new_form)
        }
        this.__input.toggle( );

    })
    $( 'li').dblclick( function(){
        date  = $(this).parent().parent().prev().html()
        index = $( this ).index( )

         $.post("/taskpaper/mod",{"flag":"mod","index":index, "date":date},function(result){
             location.reload()
         });
    })
    /*
    Max_Height=0;
    $( "div#day" ).each( function(){
        Max_Height = Math.max($( this ). height( ), Max_Height);
    })
    Max_Height= Max_Height + 70;
    $( "div#day" ).each( function(){
        $( this ). height(Max_Height);
    })
    */
})
 
