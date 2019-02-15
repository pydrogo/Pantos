/* ------------------------------------------------------------------------------
*
*  # Datatables data sources
*
*  Specific JS code additions for datatable_data_sources.html page
*
*  Version: 1.0
*  Latest update: Aug 1, 2015
*
* ---------------------------------------------------------------------------- */
var booleanTemplateFrAdmin = function(data, type, row, meta) {
    if (type == 'display') {
        return data ? '<span class="label bg-blue"><i class="icon-checkmark4 position-relative"></i></span>' : '<span class="label bg-danger"><i class="icon-cross2 position-relative"></i></span>';
    }
    return data;
};
var booleanTemplate = function(data, type, row, meta) {
    if (type == 'display') {
        return data ? '<span class="label bg-blue">فعال</span>' : '<span class="label bg-danger">غیرفعال</span>';
    }
    return data;
};
var yesNoTemplate = function(data, type, row, meta) {
    if (type == 'display') {
        return data ? '<span class="label bg-blue">Yes</span>' : '<span class="label bg-danger">No</span>';
    }
    return data;
};
var enabledTemplate = function(data, type, row, meta) {
    if (type == 'display') {
        return data ? '<span class="label bg-blue">Enabled</span>' : '<span class="label bg-danger">Disabled</span>';
    }
    return data;
};
function persianDateTimeTemplate(data, type, row, meta) {
    if (type == 'display') {
        var persianDateObject = (new Date(data)).toPersianDate();
         return persianDateObject.format('YYYY/MM/DD HH:mm:ss');
    }
    return data;
};
function persianModifiedDateTimeTemplate(data, type, row, meta) {
    if (type == 'display') {
        var persianDateObject = (new Date(data)).toPersianDate();
        if(data == row.created){
            return '-'
        }
        else
         return persianDateObject.format('YYYY/MM/DD HH:mm:ss');
    }
    return data;
};
function dataTypeTemplate(data, type, row, meta) {
    if (type == 'display' && data) {
        return Asiatech.maps.dataType[data].name;
    }
    return data;
};
function conditionSourceTemplate(data, type, row, meta) {
    if (type == 'display' && data) {
        return Asiatech.maps.conditionSource[data].name;
    }
    return data;
};
function httpMethodTemplate(data, type, row, meta) {
    if (type == 'display' && data) {
        return Asiatech.maps.httpMethodInfo[data].name;
    }
    return data;
};
function methodAttributeTypeTemplate(data, type, row, meta) {
    if (type == 'display' && data) {
        return Asiatech.maps.methodAttributeType[data].name;
    }
    return data;
};
function operatorTypeTemplate(data, type, row, meta) {
    if (type == 'display' && data) {
        return Asiatech.maps.operatorType[data].name;
    }
    return data;
};
function serviceTypeTemplate(data,type,row,meta) {
  if(type == 'display' && data) {
      return Asiatech.maps.serviceType[data].name;
  }
  return data;
};
function permissionTypeTemplate(data, type, row, meta) {
    if (type == 'display' && data) {
        return Asiatech.maps.permissionType[data].name;
    }
    return data;
};

$(function() {
    $.extend( $.fn.dataTable.defaults, {
        autoWidth: false,
        scrollX: true,
        columnDefs: [{
            orderable: false,
            targets: [ 5 ]
        }],
        dom: '<"datatable-header"fl><"datatable-scroll"t><"datatable-footer"ip>',
        language: {
            search: '<span> </span> _INPUT_',
            searchPlaceholder: 'فیلتر',
            lengthMenu: '<span></span> _MENU_',
            paginate: {'first': '«', 'last': '»', 'next': '›', 'previous': '‹'},
            info: 'نمایش _START_ - _END_ از _TOTAL_',
            emptyTable: "رکوردی برای نمایش وجود ندارد",
            infoEmpty: "نمایش 0 از 0",
        },
        drawCallback: function () {
            $(this).find('tbody tr').slice(-3).find('.dropdown, .btn-group').addClass('dropup');
        },
        preDrawCallback: function() {
            $(this).find('tbody tr').slice(-3).find('.dropdown, .btn-group').removeClass('dropup');
        }
    });

    $(document).ready(function () {
        $('.frAdmin-datatable').each(function () {
            var url = $(this).data('url');

            var columns = [],
                columnDefs = [],
                tableOptions = $(this).find('.table-options');

            var targetIndex = 0;
            tableOptions.find('.table-column').each(function () {
                var col = $(this);
                var option = {
                    "data": col.data('field')
                };
                var defOption = {};

                if (col.data('template') !== undefined && typeof window[col.data('template')] === "function") defOption['render'] = window[col.data('template')];

                if (Object.values(defOption).length > 0) {
                    defOption['targets'] = targetIndex;
                    defOption['data'] = null;

                    columnDefs.push(defOption);
                }
                columns.push(option);
                targetIndex++;
            });

            var dtOptions = {
                ajax: url,
                serverSide: true,
                columns: columns,
                columnDefs: columnDefs
            }, dtElement = $(this);

            var dtObject = dtElement.DataTable(dtOptions);

            if (dtElement.data('draw') !== undefined && typeof window[dtElement.data('draw')] === "function") {
                dtObject.on('draw', window[dtElement.data('draw')]);
            }
        });

    });
});
