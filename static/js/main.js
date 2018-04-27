$(function () {
//JQuery shortand for $(document).ready(function() { ... });
    $(chart_id).highcharts({
        chart: chart,
        title: title,
        xAxis: xAxis,
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