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
	
});
      