var source_col = ['#0F2D5D', 'rgb(102,134,191)', 'rgb(204,215,234)', 'rgb(39,175,175)', 'rgb(125,207,207)', 'rgb(212,239,239)', 'rgb(113,211,242)', 'rgb(208,240,251)','rgb(159,111,170)']

stackedBarData=[{
            name: 'BLK ',
            data: [
                [1514764800000, 70],
                [1517443200000, 55],
                [1519862400000, 30],
                [1522540800000,40],
                [1525132800000,35],
                [1527811200000,60],
                [1530403200000,50],
                [1533081600000,80]
            ],
            color:'#0F2D5D'
        },
        {
            name: 'DAWM',
            data: [
                [1514764800000, 9],
                [1517443200000, 7],
                [1519862400000, 13],
                [1522540800000,15],
                [1525132800000,20],
                [1527811200000,18],
                [1530403200000,24],
                [1533081600000,18]
            ],
            color:'rgb(102,134,191)'
        },
        {
            name: 'AVIVA',
            data: [
                [1514764800000, 4],
                [1517443200000, 5],
                [1519862400000, 6],
                [1522540800000,8],
                [1525132800000,4],
                [1527811200000,8],
                [1530403200000,9],
                [1533081600000,10]
            ],
            color:'rgb(204,215,234)'
        },
        {
            name: 'MSIM',
            data: [
                [1514764800000, 20],
                [1517443200000, 55],
                [1519862400000, 30],
                [1522540800000,40],
                [1525132800000,35],
                [1527811200000,60],
                [1530403200000,50],
                [1533081600000,45]
            ],
            color:'rgb(39,175,175)'
        },
        {
            name: 'NBG',
            data: [
                [1514764800000, 20],
                [1517443200000, 55],
                [1519862400000, 30],
                [1522540800000,40],
                [1525132800000,35],
                [1527811200000,60],
                [1530403200000,50],
                [1533081600000,45]
            ],
            color:'rgb(125,207,207)'
        }]

//console.log(stackedBarData)

stackedBarConfig={'stackedBarData':stackedBarData}


function makeStackedBar(stackedBarConfig) {

    Highcharts.chart('stacked_bar',{
        chart: {
            zoomType: 'x',
            spacingRight: 20,
            type: 'column'
        },
        credits:{
          enabled:false
        },
        title: {
            text: 'Top clients'
        },
        xAxis: {
            title: {
                text: 'Date'
            },
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Tickets Count'
            }
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                stacking: 'percent'
            }
        },
        series:stackedBarData
    });

}; //end of makeStackedBar

makeStackedBar(stackedBarConfig)
