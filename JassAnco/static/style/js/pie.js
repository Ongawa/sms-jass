$(document).ready(document_ready_basin);
function document_ready_basin() {
    $("select#basin_pie").change(function () {
        var basin_id = $(this).val();
        $.ajax({
            data:{'basin_id':basin_id},
            url: "/search_measurement_graf",
            type: "get",            
            success: Update_Reservoir_Data_Pie,
            error: Error,
        });
    })
}

function Update_Reservoir_Data_Pie(data){
  var $select = $('div#chart_div').empty();
  drawVisualization(data);
}
function drawVisualization(ll) {
  var data = google.visualization.arrayToDataTable(ll);
  var options = {
    animation: {startup: true,
                duration: 500},
    title : 'Usuarios Pagantes',
    vAxis: {title: "Pagos Realizados (%)",
            maxValue: 100,
            minValue: 0},
    hAxis: {title: "Fecha"},
    seriesType: "bars",
    series: {4: {type: "line"}}
  };

  var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}
function Error(data){
    //alert("Error. " + "Status: " + data.status + " Text: " + data.statusText);
}

function Reset() {
    document.getElementById("form_reset").reset();
}
