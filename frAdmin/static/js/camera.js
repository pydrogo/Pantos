$(document).ready(function () {
    $('.cam-enable').change(function () {
        $('#final_save').css('visibility', 'hidden');
    })
});


function submitform() {
    // var pass = $('#id_password').val();
    // var confirm_pass = $('#confirm_password').val();
    // if (pass == confirm_pass) {
    $('#form1').submit();
    // }
    // else {
    //     window.alert("رمز عبور با تکرار آن یکسان نیست. لطفا دوباره تلاش نمایید.")
    // }
}

function select_checked(check_id) {
    count = $('#form1').find('input:checked').length;
    if (count > 2) {
        alert(' در حال حاضر تعداد دوربین های مجاز 2 عدد می باشد.');
        $('#' + check_id).prop('checked', false);
        // $('#' + check_id).parent.removeClass("");
    }
}


function submitSelectform() {
    count = $('#form1').find('input:checked').length;
    if (count == 0) {
        alert('انتخاب حداقل یک دوربین الزامی است.');
    } else {
        $('#form1').submit();
    }
}


function camera_status() {
    // cam1_id = 1;
    // cam2_id = 1;
    var selected = [];
    $('#camera_checkboxes input:checked').each(function () {
        selected.push($(this).attr('id'));
    });
    if (selected.length == 0) {
        alert('لطفا حداقل یک دوربین را انتخاب کنید.')
    }
    else {
        if (typeof (selected[0]) != "undefined") {
            cam1_id = selected[0]
        }
        else {
            cam1_id = -1
        }
        if (typeof (selected[1]) != "undefined") {
            cam2_id = selected[1]
        }
        else {
            cam2_id = -1
        }

        $.ajax({
            type: "GET",
            url: "/camera/status",
            success: function (data) {
                if (data.flag == true) {
                    $('#final_save').css('visibility', 'visible');
                    alert('دوربین های انتخاب شده فعال می باشند.جهت اعمال تغییرات بر روی ذخیره نهایی کلیک کنید.');
                }
                else {
                    $('#final_save').css('visibility', 'hidden');
                    alert(data.msg);
                }
            },
            data: {'cam1': cam1_id, 'cam2': cam2_id},
            error: function (xhr, ajaxOptions, thrownError) {
                alert('خطا در برقراری ارتباط با سرور');
                alert(xhr.status);
                alert(thrownError);
            }
        });
    }
}