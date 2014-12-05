function onclick_add( ){
    var Y =this.target.offset( ).top;
    $( document ).scrollTop( Y );
}

function index_close( ){
    $( '#index' ).toggle( );
}

function index_init( index ){
    headers = $( 'h1, h2, h3, h4, h5, h6' );
    //#var close_obj=$( "<div class='index_close'></div>");
    //#close_obj.click(index_close);

    //close_obj.insertBefore(  index);

    //index.addClass( 'index')
    index.html('');

    h2=h3=h4=h5=h6=0;
    nu='';
    headers.each( function( ){
        header=$( this );
        switch( header[0].nodeName ){
                case 'H2':
                    h3=0;
                    id_div='h2';
                    break;
                case 'H3':
                    h4=0;
                    h3 = h3 + 1;
                    nu= h3.toString() + '. '; 
                    id_div='h3';
                    break;
                case 'H4':
                    id_div='h4';
                    h5=0;
                    h4 = h4 + 1;
                    nu=  h3.toString() +'.' + h4.toString()  + '. ' ; 
                    break;
                case 'H5':
                    id_div='h5';
                    h5 = h5 + 1;
                    h6=0;
                    nu=  h3.toString() +'.' + h4.toString() +
                         '.' + h5.toString()   + '. '; 
                    break;
                case 'H6':
                    id_div='h6';
                    break;
            }
            var new_obj=$('<div id="' + id_div + '">'+ nu +  header.html() + '</div>' );
            new_obj.click(onclick_add);

            //为这个元素增加一个target属性指向其对应的标题,目的是为了可以通过个
            //属性直接得到对应的标题的信息, 如标题的位置
            //注意这个不能设置为jquery的属性, 因为jquery的属性的生命周期的长度不
            //足
            new_obj[ 0 ].target = header;

            index.append( new_obj );

        }
        );
    if (h2 === 0 && h3 === 0)
    {
        index.hide();
    }
    else{
        index.show();
    }
}

