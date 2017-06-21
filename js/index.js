var warning_size = true;
var warning_touch = true;
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
});
      