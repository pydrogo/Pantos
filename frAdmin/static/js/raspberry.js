$(document).ready(function () {
    dhcp = $('#dhcp_id')[0];
    if (dhcp.checked == true) {
        // $('#div_ip_id').css('visibility', 'hidden');
        // $('#div_subnet_id').css('visibility', 'hidden');
        // $('#div_getway_id').css('visibility', 'hidden');
        $('#div_ip_id').hide();
        $('#div_subnet_id').hide();
        $('#div_getway_id').hide();
    } else {
        // $('#div_ip_id').css('visibility', 'visible');
        // $('#div_subnet_id').css('visibility', 'visible');
        // $('#div_getway_id').css('visibility', 'visible');
        $('#div_ip_id').show();
        $('#div_subnet_id').show();
        $('#div_getway_id').show();
    }
        unkown_person_id = $('#unkown_person_id')[0];
    if (unkown_person_id.checked == true) {
        $('#ftp_path_id').hide();
        $('#ftp_username').hide();
        $('#ftp_password').hide();
    } else {
        $('#ftp_path_id').show();
        $('#ftp_username').show();
        $('#ftp_password').show();
    }

    $('#ftp_input').change(function () {
        var x = document.getElementById('ftp_input').value;
        $('.filename')[0].value = x;
        $('#ftp_path_val')[0].value = x;
    });

});

function dhcpchange() {
    dhcp = $('#dhcp_id')[0];
    if (dhcp.checked == true) {

        // $('#div_ip_id').css('visibility', 'hidden');
        // $('#div_subnet_id').css('visibility', 'hidden');
        // $('#div_getway_id').css('visibility', 'hidden');
        $('#div_ip_id').hide();
        $('#div_subnet_id').hide();
        $('#div_getway_id').hide();
    } else {
        // $('#div_ip_id').css('visibility', 'visible');
        // $('#div_subnet_id').css('visibility', 'visible');
        // $('#div_getway_id').css('visibility', 'visible');
        $('#div_ip_id').show();
        $('#div_subnet_id').show();
        $('#div_getway_id').show();

    }
}

function turn_off_wifi() {
    $('#wifi_turn_on')[0].value = '1';
    $('#wifi_form').submit();
}


function unkown_func() {
    unkown_person_id = $('#unkown_person_id')[0];
    if (unkown_person_id.checked == true) {
        $('#ftp_path_id').show();
        $('#ftp_username').show();
        $('#ftp_password').show();
    } else {
        $('#ftp_path_id').hide();
        $('#ftp_username').hide();
        $('#ftp_password').hide();
    }
}
