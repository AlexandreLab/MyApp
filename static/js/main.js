var chart;

function updateChart(){

    var updateData = $.get('/live-data');
    
    updateData.done(function(results){
        var i;
        var series = chart.series;
        var shift = series[0].data.length > 10;
        var xAxis = chart.xAxis;
        for(i = 0; i< results.length; i++){
            //console.log(results[i].name);
            //console.log(results[i].data);
            console.log(series[i].name);
            //xAxis[i].setCategories
            series[i].addPoint(["15", results[i].data], false, shift);
            
        }
        
        chart.redraw();
        setTimeout(updateChart, 5000);
    });
    
}



$(function () {
//JQuery shortand for $(document).ready(function() { ... });
    chart = Highcharts.chart({
        chart: {
            renderTo: 'chart_ID', 
            type: 'area',
            height: 500,
            events: {
                load: updateChart    
            }
        },
        title: title,
        
        xAxis: {
            categories: xAxis,
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%e. %b %H:%M'
            }
        },
        

        yAxis: yAxis, 
        tooltip: {
            split: true,
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: series
    });
});