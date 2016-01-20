$(document).ready(function(){
	$.ajax({
		type: "GET",
		dataType: "json",
		data: {
			'pk': $("#poseta_pk").val(),
		},
		url: $("#rezervisani_stolovi").val(),
		
		success: function(data){
			$.each(data, function(key,val){
		        //alert("key : "+key);
		        
		        $('#myTable td').each(function () {
					var column_num = parseInt( $(this).index() ) + 1;
		            var row_num = parseInt( $(this).parent().index() )+1;

		            var red = val["red"];
			    	var kolona = val["kolona"];
			    	var stanje = val["stanje"];
			    	var stolice = val["stolice"];
			    	
			    	if(red == row_num && kolona == column_num){
			    		$(this).empty();
			    		
			    		$(this).append("<button id='"+key+"' type='button' class='btn btn-warning'>"+stolice+"</button>");
			    	}
		            
				});
		    });
		},
		
		error: function(data){
			alert("error");
		}
	});
});