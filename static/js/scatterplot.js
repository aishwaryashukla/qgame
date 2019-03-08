var global_touchCountData;
var selected_region='AMER'

$.ajax({
   url:"static/data/touchCountChart.csv",
   dataType:"text",
   success:function(data2){ 

    //console.log(data2)

    var data2 = d3.csv.parse(data2, function(d) {
                  return {
                    clientRegion:d.clientRegion,
                    taskId:d.taskId,
                    CreatedDate:d.CreatedDate,
                    AgeDays:+d.AgeDays,
                    taskTouchCount:+d.taskTouchCount
                  };
                });  
    //console.log(data2)
    global_touchCountData=data2
    //console.log(data)

    makeScatterPlotData(data2,selected_region)
    

   }
});

function makeScatterPlotData(data,selected_region){

    scatterPlotData=[]

    filter_data=data.filter(function(x){return x.clientRegion==selected_region})
    //console.log(filter_data)

    filter_data.forEach(function(obj){
        scatterPlotData.push([obj['AgeDays'],obj['taskTouchCount']])
    })

    //console.log(scatterPlotData)
    //console.log(comp_arr)

    scatterPlotconfig={'scatterPlotData': scatterPlotData}
    makeScatterPlot(scatterPlotconfig)

}

function makeScatterPlot(scatterPlotconfig){


    Highcharts.chart('scatterplot_1', {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        credits:{
            enabled:false
        },
        title: {
            text: 'Ticket Touches vs Age'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            title: {
                enabled: true,
                text: 'Ticket Age'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Ticket Touch count'
            }
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    pointFormat: 'Age: {point.x}, TouchCount: {point.y}'
                }
            }
        },
        series: [{
            name:'Ticket Age & TouchCount',
            color: '#27AFAF',
            data: scatterPlotconfig['scatterPlotData']
        }]
    });

} //end of makeScatterPlot

$("#region_select").change(function() {
    var new_sel_region = $("#region_select").find('option:selected').val();
    //console.log(new_sel_region)
    makeScatterPlotData(global_touchCountData,new_sel_region)  
    
});