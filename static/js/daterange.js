$(document).ready(function() {
    
    $("#from").datepicker({
        dateFormat: 'yy-mm',
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        beforeShow: function(input, inst) {
            if (!$(this).val()) {
                $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1)).trigger('change');
            }
        },
        onClose: function(dateText, inst) {
            $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
            $("#to").datepicker("option", {minDate: new Date(inst.selectedYear, inst.selectedMonth, 1)})
        }
    });
    $('#from').datepicker('setDate', new Date());
    $('#to').datepicker({
        dateFormat: 'yy-mm',
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        onClose: function(dateText, inst) {
            $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1)).trigger('change');
        }
    });

    $("#btnShow").click(function() {
        if ($("#from").val().length == 0 || $("#to").val().length == 0) {
            alert('All fields are required');
        } else {
            var startDay = new Date($("#from").val());
            var endDay = new Date($("#to").val());
            var date2_UTC = new Date(Date.UTC(endDay.getUTCFullYear(), endDay.getUTCMonth()));
            var date1_UTC = new Date(Date.UTC(startDay.getUTCFullYear(), startDay.getUTCMonth()));

            var months = date2_UTC.getMonth() - date1_UTC.getMonth();
            if (months < 0) {
                date2_UTC.setFullYear(date2_UTC.getFullYear() - 1);
                months += 12;
            }
            var years = date2_UTC.getFullYear() - date1_UTC.getFullYear();

            if (years > 0) {
                if(months > 0)
                  $('#result').html(years + " year " + " " + months + " month");
                else
                  $('#result').html(years + " year ");
                
            } else {
                $('#result').html(months + " month");
            }

        }
    });
});