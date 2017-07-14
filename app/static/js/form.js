var warning_size = true;
var warning_touch = true;
var gaming_section = false;
var video_section = false;
var photo_section = false;
$(document).ready(function(){
    $('.collapsible').collapsible();
	$('input:radio[name=group2]').change( function() {
		if(warning_size){
			Materialize.toast('14 inch and below laptops do not have a numeric keypad', 4000);
		}
		warning_size = false;
	});
	$('input:radio[name=group3]').change( function() {
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
    $('#get_suggestions').bind('click', function() {
    	console.log("Clicked");
      $.getJSON('/getSuggestions', { 
			budget : $('#budget').val(),
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
        //a: $('input[name="a"]').val(),
        //b: $('input[name="b"]').val()
      }, function(data) {
        console.log(data);
      });
      return false;
    });
		      
});
