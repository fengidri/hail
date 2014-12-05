function draw_border( callback ){
	var f=$( '#frame')
		var p=f.offset( )
		var target_color='black'
		var source_color='white'
		var time= 1000
		var draw_div = '#draw_frame'
		var source_div = '#frame'
		$( draw_div).offset( p)
		$( draw_div).css( 'border','3pt solid white')
		$( source_div).css( 'border','3pt solid white')
		$( draw_div).css( 'border-top-color',target_color)
		$( draw_div).animate( {width:f.width( )},time,function( )
				{
					$( draw_div).css( 'border-right-color',target_color)
			$( source_div).css( 'border-top-color',target_color)
				}
				)
		$( draw_div).animate( {height:f.height( )},time,function( )
				{
					$( source_div).css( 'border-bottom-color',target_color)
			$( source_div).css( 'border-right-color',target_color)
			$( draw_div).css( 'border-right-color',source_color)
			$( draw_div).css( 'border-right-width','0')
				})
	$( draw_div).animate( {width:'0'},time,function( )
			{
				$( draw_div).css( 'border-right-color',source_color)
		$( source_div).css( 'border-left-color',target_color)
			})

	$( draw_div).animate( {height:'0'},time,function( ){
		$( this).hide()
		callback( )
	})
}
