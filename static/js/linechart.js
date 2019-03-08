var global_completedRatioData;
var selected_region='AMER'

function Comparator(a, b) {
   if (a[0] < b[0]) return -1;
   if (a[0] > b[0]) return 1;
   return 0;
 }

 $.ajax({
   url:"static/data/completedRatioChart_1.csv",
   dataType:"text",
   success:function(data2){ 

    //console.log(data2)

    var data2 = d3.csv.parse(data2, function(d) {
                  return {
                    clientRegion:d.clientRegion,
                    createdTimeUTC:d.createdTimeUTC,
                    completedTickets:+ d.completedTickets,
                    totalTickets:+ d.totalTickets
                  };
                });  
    //console.log(data2)
    global_completedRatioData=data2
    //console.log(data)

    makeLineChartData(data2,selected_region)
    

   }
});

function makeLineChartData(data,selected_region){

    //console.log(data)
    //console.log(selected_region)

    total_tickets_arr=[]
    comp_arr=[]

    filter_data=data.filter(function(x){return x.clientRegion==selected_region})
    //console.log(filter_data)

    filter_data.forEach(function(obj){
        //console.log(obj)
        date=convertDateToTimestamp(obj['createdTimeUTC'])
        //console.log(obj['createdTimeUTC'])
        console.log(date)
        total_tickets_arr.push([date,obj['totalTickets']])
        comp_arr.push([date,obj['completedTickets']])
    })


    total_tickets_arr=total_tickets_arr.sort(Comparator)
    comp_arr=comp_arr.sort(Comparator)

    //console.log(total_tickets_arr)
    //console.log(comp_arr)

    linechart1_config={'y_title':'Tickets count',
        'chart_title':'Created vs Completed',
        'tickets_created_arr':total_tickets_arr,
        'tickets_completed_arr':comp_arr
        }

    makeLineChart_1(linechart1_config)

}
//function to make linechart_1; this is for ticket_age>10
function makeLineChart_1(linechart1_config){

        Highcharts.chart('linechart_1', {

            credits:{
                enabled:false
            },
            title: {
                text: linechart1_config['chart_title']
            },

            subtitle: {
                text: ''
            },

            yAxis: {
                title: {
                    text: linechart1_config['y_title']
                }
            },
            xAxis: {
                type: 'datetime',

            },
            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: true
                    }
                },
                zoomType:'xy'
            },

            series: [{
                name: 'Created',
                color: 'rgb(135,185,37)',
                data: linechart1_config['tickets_created_arr']
            }, {
                name: 'Completed',
                color: 'rgb(0,53,148)',
                data: linechart1_config['tickets_completed_arr']
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            
                        }
                    }
                }]
            }

        });

} //end of makeLineChart_1


$("#region_select").change(function() {
    var new_sel_region = $("#region_select").find('option:selected').val();
    //console.log(new_sel_region)
    makeLineChartData(global_completedRatioData,new_sel_region)  
    
});
    
//makeLineChart_1(linechart1_config)
