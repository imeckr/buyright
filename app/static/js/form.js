var warning_size = true;
var warning_touch = true;
var gaming_section = false;
var video_section = false;
var photo_section = false;
$(document).ready(function(){
    $('.collapsible').collapsible();
	$('#budget').on("keyup", function() {
		if ( $.inArray( event.keyCode, [38,40,37,39] ) !== -1 ) {
			return;
		}
		var $this = $( this );
		var input = $this.val();
		var input = input.replace(/[\D\s\._\-]+/g, "");
		input = input ? parseInt( input, 10 ) : 0;
		$this.val( function() {
			return ( input === 0 ) ? "" : input.toLocaleString( "en-US" );
		});
		//Materialize.toast('14 inch and below laptops do not have a numeric keypad', 4000);
	});
	$('input:checkbox[id=screen_tiny]').change( function() {
		if(warning_size){
			Materialize.toast('14 inch and below laptops do not have a numeric keypad', 4000);
		}
		warning_size = false;
	});
	$('input:radio[id=tc_yes]').change( function() {
		if(warning_touch){
			Materialize.toast('Touch Screen laptops are Rs.10,000-15,000 costlier than their non-touch versions', 4000);
		}
		warning_touch = false;
	});
	
	$('input:checkbox[id=usage_gaming]').change( function() {
		if (gaming_section){
			$('#gaming_section').hide();
		}
		else{
			console.log("Usage Gaming");
			$('#gaming_section').show();
		}
		gaming_section = !gaming_section;
	});
	
	$('input:checkbox[id=usage_photo]').change( function() {
		if (photo_section){
			$('#photo_section').hide();
		}
		else{
			console.log("Usage Photo");
			$('#photo_section').show();
		}
		photo_section = !photo_section;
	});	
	
	$('input:checkbox[id=usage_video]').change( function() {
		if (video_section){
			$('#video_section').hide();
		}
		else{
			console.log("Usage Video");
			$('#video_section').show();
		}
		video_section = !video_section;
	});
	function get_ids (x) {
		new_ids = [];
		for (var i = x.length - 1; i >= 0; i--) {
			new_ids.push(x[i].id);
		};
		return new_ids;
	}
	function validateInputs(){
		var validate = true;
		if($('#budget').val()===""){
			validate = false;
			Materialize.toast("Please enter a valid budget",3000);
		}
		if($('#email_address').val()===""){
			validate = false;
			Materialize.toast("Please enter a valid email address",3000);
		}
		if($('.laptop_brand:checkbox:checked').length===0){
			validate = false;
			Materialize.toast("Please select at least one brand",3000);
		}
		if($("input[name='screen_size']:checked").length===0){
			validate = false;
			Materialize.toast("Please select at least one screen size",3000);
		}
		return validate;
	}
    $('#get_suggestions').bind('click', function() {
    	console.log("Clicked");
    	if (!validateInputs()){
    		return false;
    	}
		$.getJSON('/validateInputs', { 
			budget : $('#budget').val().replace(/[\D\s\._\-]+/g, ""),
			usages : get_ids($('.usage:checkbox:checked')),
			other_usages :$('#other_usage').val(),
			windows: get_ids($("input[name='windows']:checked")),
			photo_editing: get_ids($("input[name='photo_editing']:checked")),
			video_editing: get_ids($("input[name='video_editing']:checked")),
			laptop_brand: get_ids($('.laptop_brand:checkbox:checked')),
			gaming: get_ids($("input[name='gaming']:checked")),
			screen_size: get_ids($("input[name='screen_size']:checked")),
			touch_screen: get_ids($("input[name='touch_screen']:checked")),
			buying: get_ids($("input[name='buying']:checked")),
			email_address: $('#email_address').val(),
			contact_no: $('#contact_no').val()
		}, function(data) {
	      	if (data.data_validation){
	      		window.location.href = "/suggestions";
	      	}
	        else {
	        	console.log("Server Data Validation Error");
	        }
	    });
		return false;
    });      
});
