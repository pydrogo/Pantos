$(document).ready(function () {
    $('.cam-enable').change(function () {
        $('#final_save').css('visibility', 'hidden');
    })
});


function submitform() {
    Swal.fire({

        type: 'warning',
        title: 'لطفا دوربین ها را مجددا فعالسازی نمایید.',
        showConfirmButton: false,
    });
    window.setTimeout(3000);
    $('#form1').submit();
}

function select_checked(check_id) {
    count = $('#form1').find('input:checked').length;
    if (count > 2) {
        Swal.fire('در حال حاضر تعداد دوربین های مجاز 2 عدد می باشد.');
        $('#' + check_id).prop('checked', false);
        $('#' + check_id).parent().removeClass("checked");
    }
}


function submitSelectform() {
    count = $('#form1').find('input:checked').length;
    if (count == 0) {
        Swal.fire('انتخاب حداقل یک دوربین الزامی است.');
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
        Swal.fire('لطفا حداقل یک دوربین را انتخاب کنید.');
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
                    Swal.fire('دوربین های انتخاب شده فعال می باشند.جهت اعمال تغییرات بر روی ذخیره نهایی کلیک کنید.');

                }
                else {
                    $('#final_save').css('visibility', 'hidden');
                    Swal.fire('' + data.msg + '');

                }
            },
            data: {'cam1': cam1_id, 'cam2': cam2_id},
            error: function (xhr, ajaxOptions, thrownError) {
                Swal.fire('خطا در برقراری ارتباط با سرور');
                Swal.fire('' + xhr.status + '');
                Swal.fire('' + thrownError + '');

            }
        });
    }
}