var source_col =    ['#0F2D5D', 'rgb(102,134,191)', 'rgb(204,215,234)', 'rgb(39,175,175)', 'rgb(125,207,207)', 'rgb(212,239,239)', 'rgb(113,211,242)', 'rgb(208,240,251)', 'rgb(159,111,170)'];
var global_piechartData;
var selected_region='AMER'
var source_col = ['#0F2D5D', 'rgb(102,134,191)', 'rgb(204,215,234)', 'rgb(39,175,175)', 'rgb(125,207,207)', 'rgb(212,239,239)', 'rgb(113,211,242)', 'rgb(208,240,251)','rgb(159,111,170)']

$.ajax({
   url:"static/data/ageChartForRegion.csv",
   dataType:"text",
   success:function(data2){ 

    //console.log(data2)

    var data2 = d3.csv.parse(data2, function(d) {
                  return {
                    Category:d.Category,
                    Percentage:+d.Percentage,
                    Region:d.Region
                  };
                });  
    //console.log(data2)
    global_piechartData=data2
    //console.log(data2)

    makepieChartData(data2,selected_region)
    

   }
});

function makepieChartData(data,selected_region){

    //console.log(data)
    //console.log(selected_region)

    var piearr=[]

    filter_data=data.filter(function(x){return x.Region==selected_region})
    //console.log(filter_data)

    filter_data.forEach(function(obj,i){
        //console.log(i)
        //console.log(obj)
        //console.log(obj['Category'])
        var obj1={name:obj['Category'],y:obj['Percentage'],color:source_col[i]}
        piearr.push(obj1)
    })


   //console.log(total_tickets_arr)
   // console.log(piearr)

    pieChartConfig={'pieChartData':piearr}
    makePieChart(pieChartConfig)

}

function makePieChart(pieChartConfig){

        Highcharts.chart('ticket_age_dist', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            credits:{
                enabled:false
            },
            title: {
                text: 'Distribution of Ticket Age'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            legend: {
                        title: {
                            text:'Ticket Age in days'
                        }
                    },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',

                    dataLabels: {
                        enabled: true,
                        format: '{point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }

                    },
                    showInLegend: true,
                    

                }
            },
            series: [{
                colorByPoint: true,
                data: pieChartConfig['pieChartData']
            }]
        });


}//end of makePieChart

$("#region_select").change(function() {
    var new_sel_region = $("#region_select").find('option:selected').val();
    //console.log(new_sel_region)
    makepieChartData(global_piechartData,new_sel_region)  
    
});
    