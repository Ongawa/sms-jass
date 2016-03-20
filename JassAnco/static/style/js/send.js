$(document).ready(document_ready_basin);
$(document).ready(document_ready_send);

function document_ready_basin() {
    $("select#basin").change(function () {
        var basin_id = $(this).val();
        $.ajax({
            data:{'basin_id':basin_id},
            url: "/search_reservoir",
            type: "get",            
            success: Update_Reservoir_phone,
            error: Error,
        });
    })
}

function document_ready_send() {
    $("button#send").click(function () {
        var managers_phone = Get_Data_Check();
        var msg = $('input#send').val();
        $.ajax({
            data:{'managers_phone':managers_phone,'msg':msg},
            url: "/send_msg",
            type: "get", 
            success: Msg_Confirm,
            error: Error,
        });
    })
}

function Msg_Confirm(data){
	AlertSend(data);
	Reset();
}

function Update_Reservoir(data){
	var $select = $('select#reservoir').empty();
	for (var i = 0; i < data.length; i++) {
	    var o = $('<option/>', { value: data[i]['manager_id'] })
	        .text(data[i]['manager_id'])
	        .prop('selected', i == 0);
	    o.appendTo($select);
	}    
}

function Update_Reservoir_phone(data){
	//alert(data);
	var $select = $('div#div_ckeck').empty();
	for (var i = 0; i < data.length; i++) {
		var $myNewElement = $("<input class = 'ok' type='checkbox' name='option1' value='"+data[i]['manager_id']+"'> "+data[i]['reservoir_id']+" "+data[i]['manager_id']+" <br>");
		$myNewElement.appendTo('#div_ckeck');
	}  	
}

function Get_Data_Check(){
	var checkboxValues = "";
	$('input[name="option1"]:checked').each(function() {
		checkboxValues += $(this).val() + ",";
	});
	return checkboxValues = checkboxValues.substring(0, checkboxValues.length-1);
}

function AlertSend(data){     
    if (data == 'Error'){
        type = 'error';
    }else{
        type = 'success';
    }
    swal({
        title: data,
        //text: data,
        type: type,
        confirmButtonColor: "#1565C0",
        confirmButtonText: "Cerrar"
    });
}

function Reset() {
    document.getElementById("form_reset").reset();
}
function Error(data){
    alert("Error. " + "Status: " + data.status + " Text: " + data.statusText);
}

