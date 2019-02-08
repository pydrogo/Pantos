$(document).ready(function () {
    dhcp = $('#dhcp_id')[0];
    if (dhcp.checked == true) {
        $('#div_ip_id').css('visibility', 'hidden');
        $('#div_subnet_id').css('visibility', 'hidden');
        $('#div_getway_id').css('visibility', 'hidden');
    } else {
        $('#div_ip_id').css('visibility', 'visible');
        $('#div_subnet_id').css('visibility', 'visible');
        $('#div_getway_id').css('visibility', 'visible');

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

        $('#div_ip_id').css('visibility', 'hidden');
        $('#div_subnet_id').css('visibility', 'hidden');
        $('#div_getway_id').css('visibility', 'hidden');
    } else {
        $('#div_ip_id').css('visibility', 'visible');
        $('#div_subnet_id').css('visibility', 'visible');
        $('#div_getway_id').css('visibility', 'visible');

    }
}

function turn_off_wifi() {
    $('#wifi_turn_on')[0].value = '1';
    $('#wifi_form').submit();
}


function unkown_func() {
    unkown_person_id = $('#unkown_person_id')[0];
    if (unkown_person_id.checked == true) {
        $('#ftp_path_id').css('visibility', 'visible');
        $('#ftp_username').css('visibility', 'visible');
        $('#ftp_password').css('visibility', 'visible');
    } else {
        $('#ftp_path_id').css('visibility', 'hidden');
        $('#ftp_username').css('visibility', 'hidden');
        $('#ftp_password').css('visibility', 'hidden');
    }
}
