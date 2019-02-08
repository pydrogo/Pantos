var test = 0;
var attr_list = [];
var temp = '';
var stream_row = 0;
$(document).ready(function () {
    for (var i = 0; i < perm_list2.length; i++) {
        $('#' + perm_list2[i])[0].checked = true;
        $('#' + perm_list2[i]).parent().addClass('checked');

    }
    for (var j = 0; j < my_alarms.length; j++) {
        $('#' + my_alarms[j])[0].checked = true;
        $('#' + my_alarms[j]).parent().addClass('checked');
    }


    $(".modal").on("hidden.bs.modal", function () {
        $('.modal').modal('hide');
        $(".modal-body").modal('hide');
        $(".in_modal").empty();
    });

    $()

});

function pass_validation() {
    var passconfirm_id = document.getElementById('confirm_pass').value;
    var edit_pass_id = (document.getElementById('password')) ? document.getElementById('password').value : '';
    if (typeof edit_pass_id !== 'undefined') {
        if (edit_pass_id == passconfirm_id) {
            $('#user_create_form').submit();
        } else {
            window.alert("Your password and confirm password is not Equal , Please Enter corroct passsword and try again");
        }
    }
}

function edit_pass_validation() {
    var passconfirm_id = document.getElementById('confirm_pass').value;
    var edit_pass_id = (document.getElementById('password')) ? document.getElementById('password').value : '';
    if (typeof edit_pass_id !== 'undefined') {
        if (edit_pass_id == passconfirm_id) {
            $('#user_edit_form').submit();

        } else {
            window.alert("Your password and confirm password is not Equal , Please Enter corroct passsword and try again");
        }
    }
}

function snapshot_model() {
    cdid = $('#select_camera_stream').val();
    $('#stream-frame').attr('src', frameUrl + '?cid=' + cdid);
    $('#modal_stream').modal();

}

function snapshot() {
    $.ajax({
        "type": 'GET',
        "url": '/snapshot?cid=' + $('#select_camera_stream').val(),
        success: function (data) {
            if (typeof (data.camera_status) != 'undefined') {
                if (data.camera_status == false) {
                    alert('دوربین غیرفعال است');
                    return 0;
                }
            }
            debugger;
            row = stream_row;
            stream_row = stream_row + 1;
            $('#show_modal_images').append('<a target="_blank"><img id="image_tag" style="width: 50px" src="data:image/jpeg;base64,' + data + '"></a>');
            $('#show_images').append('<a target="_blank"><img id="stream_img_tag" style="width: 60px" src="data:image/jpeg;base64,' + data + '"></a>');
            if ($('#user_form').length > 0)
                $('#user_form').append('<input name="stream_image' + row + '" type="hidden" value="' + data + '">');
            if ($('#user_edit_form').length > 0)
                $('#user_edit_form').append('<input name="stream_image' + row + '" type="hidden" value="' + data + '">');
            $('#row_id').val(row);
        },

        error: function (request, error) {
            alert('Something Wents Wrong Please Try Again');
        },
    });
}


function show_profile_pic() {
    input = $('#id_image_profile')[0];
    placeToInsertImagePreview = $('#profile_pic_div');
    if (input.files) {
        var filesAmount = input.files.length;

        for (i = 0; i < filesAmount; i++) {
            var reader = new FileReader();

            reader.onload = function (event) {
                $($.parseHTML('<img style="width: 100px">')).attr('src', event.target.result).appendTo(placeToInsertImagePreview);
            };

            reader.readAsDataURL(input.files[i]);
        }
    }
}

function show_dataset_pic() {
    input = $('#id_profile_image')[0];
    placeToInsertImagePreview = $('#dataset_pic_div');
    if (input.files) {
        var filesAmount = input.files.length;

        for (i = 0; i < filesAmount; i++) {
            var reader = new FileReader();

            reader.onload = function (event) {
                $($.parseHTML('<img style="width: 85px;height:85px;padding: 5px">')).attr('src', event.target.result).appendTo(placeToInsertImagePreview);
            };

            reader.readAsDataURL(input.files[i]);
        }
    }
}