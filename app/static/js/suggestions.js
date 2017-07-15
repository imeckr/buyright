$(document).ready(function(){
    $('#get_more_suggestions').bind('click', function() {
    	console.log("Clicked");
      $.getJSON('/validateInputs', { 
        //a: $('input[name="a"]').val(),
        //b: $('input[name="b"]').val()
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
