$(document).ready(function () {
    var temp = time_list_value;
    $('.only-timepicker-example-from').persianDatepicker({
        onlyTimePicker: true,
        format: "HH:mm:ss",
        locale: 'en',
        persian: {
            locale: 'en'
        },
        calendar: {
            persian: {
                locale: 'en'
            }
        }
    });

    $('.only-timepicker-example-to').persianDatepicker({
        onlyTimePicker: true,
        format: "HH:mm:ss",
        language: 'en',
        locale: 'en',
        persian: {
            locale: 'en'
        },
        calendar: {
            persian: {
                locale: 'en'
            }
        }


    });
    debugger;
    for (var i = 0; i < time_list_value.length; i++) {
        $('#start-' + time_list_value[i]['day_number']).val(time_list_value[i]['start']);
        $('#end-' + time_list_value[i]['day_number']).val(time_list_value[i]['end']);
    }


});