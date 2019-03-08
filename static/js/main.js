var region_arr=['AMER','AMRS','APAC','ASIA','Australia','EMEA','MX','Other']
//console.log(region_arr)
var team_arr=['GPAS','DIG','BRS']
//console.log(team_arr)
var default_region=''
var default_team=''
var default_time=[]

//function to poulate a dropdown, given select id and the data array
function appendDropdown(dropdown_id,dropdown_arr){

	$.each(dropdown_arr, function(key,value) {   
     $('#'+dropdown_id)
         .append($("<option></option>")
                    .attr("value",value)
                    .text(value)); 
	});

}

//convert a string date in timestamp ; requird by highcharts timeseries
function convertDateToTimestamp(date){
     d_str = new Date(date.split('/')[1]+',01,'+date.split('/')[0]+' 00:00:00 GMT')
     date_time=d_str.getTime();
     return date_time
}

function Comparator(a, b) {
   if (a[0] < b[0]) return -1;
   if (a[0] > b[0]) return 1;
   return 0;
 }

appendDropdown('region_select',region_arr)
appendDropdown('team_select',team_arr)


$('.time_range').daterangepicker(
		{
          startDate: moment().subtract('days', 30),
          endDate: moment(),
          minDate: '01/01/2010',
          maxDate: moment(),
          dateLimit: { days: 3000 },
          showDropdowns: true,
          showWeekNumbers: true,
          timePicker: false,
          timePickerIncrement: 1,
          timePicker12Hour: true,
          ranges: {
	     		'Current Year': [moment().year(moment().year()).startOf('year'), moment()],
	     		'Current Quarter': [moment().quarter(moment().quarter()).startOf('quarter'), moment()],
             	'Last 30 Days': [moment().subtract('days', 29), moment()],
             	'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')],
	     		'Last 90 Days':  [moment().subtract('days', 89), moment()], 
	     		'Last 1 Year': [moment().subtract(1, 'year').add(1,'day'), moment()],
	     		'Last 2 Years': [moment().subtract(2, 'year').add(1,'day'), moment()]
          },
          opens: 'center',
          buttonClasses: ['btn btn-default'],
          applyClass: 'btn-small btn-primary',
          cancelClass: 'btn-small',
          format: 'DD/MM/YYYY',
          separator: ' to ',
          locale: {
              applyLabel: 'Select',
              fromLabel: 'From',
              toLabel: 'To',
              customRangeLabel: 'Custom Range',
              daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr','Sa'],
              monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
              firstDay: 1
          }
       },
       function(start, end) {
        $('#reportrange1 span').html(start.format('D MMMM YYYY') + ' - ' + end.format('D MMMM YYYY'));
	
        startDate = start;
        endDate = end;
		//console.log("start----"+typeof(start))
		//console.log("end-----"+ typeof(end))

		//change the selected date range of that picker
		$('#reportrange1').data('daterangepicker').setStartDate(start);
		$('#reportrange1').data('daterangepicker').setEndDate(end);
		
		$('#reportrange2').data('daterangepicker').setStartDate(start);
		$('#reportrange2').data('daterangepicker').setEndDate(end);

       }
    


	);

