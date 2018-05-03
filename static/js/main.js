var chart;

function updateChart(){

    var updateData = $.get('/live-data');
    
    updateData.done(function(results){
    
        if (results.length>0) {
            var i;
            var series = chart.series;
            var shift = series[0].data.length > 30;
            var xAxis = chart.xAxis;
            for(i = 0; i< results.length; i++){
                //console.log(results[i].name);
                //console.log(results[i].data);
                console.log(series[i].name);
                //xAxis[i].setCategories
                series[i].addPoint(results[i].data, false, shift);
                
            }   
            chart.redraw();
        }
        setTimeout(updateChart, 1*60*1000);
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
            type: 'datetime',
            tickInterval: 30*60 * 1000,
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
                pointInterval: 30*60 * 1000,
                pointStart: Date.UTC(year, month, day, hour, minute, 0, 0),
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series:series,
    });
});