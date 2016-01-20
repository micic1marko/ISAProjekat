
$(document).ready(function(){
        $("#myTable td ").click(function() {     
 
            var column_num = parseInt( $(this).index() ) + 1;
            var row_num = parseInt( $(this).parent().index() )+1;  
 			
 			if($(this).text() == "x"){
 				$("#restoran_stolice").val(0);
 				$("#delete_btn").attr("disabled", true);
 			}else{
 				$("#restoran_stolice").val($(this).text());
 				$("#delete_btn").attr("disabled", false);
 			}
 			
            $("#kolona_key").val(column_num);
            $("#red_key").val(row_num);
            $("#myModal").modal();
        });
    });
    
$(document).ready(function(){
	$.ajax({
		type: "GET",
		dataType: "json",
		data: {
			'pk': $("#pk").val(),
		},
		url: $("#url").val(),
		
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
			    		
			    		if(stanje == 'F'){
			    			$(this).append("<button id='"+key+"' type='button' class='btn btn-success'>"+stolice+"</button>");
			    		}else if(stanje == 'R'){
			    			$(this).append("<button id='"+key+"' type='button' class='btn btn-danger'>"+stolice+"</button>");
			    		}
			    	}
		            
				});
		    });
		},
		
		error: function(data){
			alert("error");
		}
	});
        
});


$(document).ready(function(){
	$("#save").click(function() {
		$.ajax({
			type: "GET",
			dataType: "json",
			data: {
				'pk': $("#pk").val(),
				'number': $("#restoran_stolice").val(),
				'stolice': $("#sto_key").val(),
				'kolona': $("#kolona_key").val(), 
				'vrsta': $("#red_key").val(),
			},
			url: $("#update").val(),
			
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
				    		
				    		if(stanje == 'F'){
				    			$(this).append("<button id='"+key+"' type='button' class='btn btn-success'>"+stolice+"</button>");
				    		}else if(stanje == 'R'){
				    			$(this).append("<button id='"+key+"' type='button' class='btn btn-danger'>"+stolice+"</button>");
				    		}
				    	}
			            
					});
			    });
			},
			
			error: function(data){
				alert("error");
			}
		});
	});  
});



$(document).ready(function(){
	$("#delete").click(function() {
		$.ajax({
			type: "GET",
			dataType: "json",
			data: {
				'pk': $("#pk").val(),
				'stolice': $("#sto_key").val(),
			},
			url: $("#delete_url").val(),
			
			success: function(data){
			
				$.each(data, function(key,val){
			        //alert("key : "+key);
			        
			        $('#myTable td').each(function () {
						var column_num = parseInt( $(this).index() ) + 1;
			            var row_num = parseInt( $(this).parent().index() )+1;
			            
			            var red = val["red"];
				    	var kolona = val["kolona"];
				    	
				    	if(red == row_num && kolona == column_num){
				    		$(this).empty();
				    		$(this).append("<button type='button' class='btn btn-default'>x</button>");
				    	}
			            
					});
			    });
			},
			
			error: function(data){
				alert("error");
			}
		});
	});  
});


