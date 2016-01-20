function dojob(key){
	var button = document.getElementById(key)
	
	//alert(button.className);
	
	if(button.className == "btn btn-success"){
		button.className = "btn btn-warning"
		
		$("#id_stolovi option[value = '"+ key +"']").prop("selected", true);
		//alert($("#id_stolovi").val());
		
	}else if(button.className == "btn btn-warning"){
		button.className = "btn btn-success"
		
		$("#id_stolovi option[value = '"+ key +"']").prop("selected", false);
		//alert($("#id_stolovi").val());
	}
}

$(document).ready(function(){
	$("#id_stolovi").hide();
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
});

$(document).ready(function(){
	$.ajax({
		type: "GET",
		dataType: "json",
		data: {
			'pk': $("#restoran_pk").val(),
		},
		url: $("#stanje_svih_stolova").val(),
		
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
			    	var zauzet = val["zauzet"];
			    	
			    	if(red == row_num && kolona == column_num){
			    		$(this).empty();

			    		if(stanje == 'F'){
			    			$(this).append("<button onclick='dojob("+key+")' id='"+key+"' type='button' class='btn btn-success' disabled='true'>"+stolice+"</button>");
			    		}else if(stanje == 'R'){
			    			$(this).append("<button data-toggle='tooltip' title='"+zauzet+"' id='"+key+"' type='button' class='btn btn-danger' disabled='true'>"+stolice+"</button>");
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
        $("#check").click(function() {
        	var zauzece = $("#id_zauzece").val();
			var datum =  $("#datum input").val();
			
			if(zauzece == ""){
				$( "#id_zauzece" ).css("border-color", "red");
			}else{
				$( "#id_zauzece" ).css("border-color", "");
			}
			
			if(datum == ""){
				$( "#datum input" ).css("border-color", "red");
			}else{
				$( "#datum input" ).css("border-color", "");
			}
			
			if(zauzece != "" && datum != ""){
	           	$.ajax({
					type: "GET",
					dataType: "json",
					data: {
						'pk': $("#restoran_pk").val(),
						'value': $("#datum input").val(),
						'zauzece': $("#id_zauzece").val(),
					},
					url: $("#check_url").val(),
					
					success: function(data){
						$.each(data, function(key,val){

					        $('#myTable td').each(function () {
								var column_num = parseInt( $(this).index() ) + 1;
					            var row_num = parseInt( $(this).parent().index() )+1;
					            
					            var red = val["red"];
						    	var kolona = val["kolona"];
						    	var stanje = val["stanje"];
						    	var stolice = val["stolice"];
						    	var zauzet = val["zauzet"];
						    	
						    	if(red == row_num && kolona == column_num){
						    		$(this).empty();
						    		
						    		if(stanje == 'F'){
						    			$(this).append("<button onclick='dojob("+key+")' id='"+key+"' type='button' class='btn btn-success'>"+stolice+"</button>");
						    		}else if(stanje == 'R'){
						    			$(this).append("<button data-toggle='tooltip' title='"+zauzet+"' id='"+key+"' type='button' class='btn btn-danger'>"+stolice+"</button>");
						    		}
						    	}
							});
				    	});
					},
					
					error: function(data){
						alert("error");
					}
				})
			}
        });
});