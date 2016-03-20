$(document).ready(document_ready_basin);

function document_ready_basin() {
    $("select#reservoir").change(function () {
        var reservoir_id = $(this).val();
        var date = $('input#startDate').val();
        $.ajax({
            data:{'reservoir_id':reservoir_id,'date':date},
            url: "/search_measurement",
            type: "get",            
            success: Update_Reservoir_Data,
            error: Error,
        });
    })
}
function Update_Reservoir_Data(data){
	var $select = $('tbody#table_body').empty();
    
	for (var i = 0; i < data.length; i++) {
        var tds = '<tr>';
        tds += '<td>'+ data[i]['reservoir_id']+'</td>';
        tds += '<td>'+ data[i]['date']+'</td>';
        tds += '<td>'+ data[i]['level_cl']+'</td>';
        tds += '<td>'+ data[i]['add_cl']+'</td>';
        tds += '<td>'+ data[i]['caudal']+'</td>';
        tds += '<td>'+ data[i]['user_pay']+'</td>';

        tds += '</tr>';
        $(".scroll").append(tds);
	}
}
function Error(data){
    alert("Error. " + "Status: " + data.status + " Text: " + data.statusText);
}

function Reset() {
    document.getElementById("form_reset").reset();
}
