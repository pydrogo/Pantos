$(document).ready(function () {
    var maxId = 0;
    var graph = new joint.dia.Graph;
    var paper_width = $('#diagram-container').parent().css('width').match(/\d+/)[0];
    var paper = new joint.dia.Paper({
        el: document.getElementById('diagram-container'),
        model: graph,
        width: paper_width - 50,
        height: 500,
        gridSize: 20,
        defaultLink: new joint.dia.Link({
            attrs: {'.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}}
        }),
        markAvailable: true,
        validateConnection: function (cellViewS, magnetS, cellViewT, magnetT, end, linkView) {
            if (magnetS && magnetS.getAttribute('port-group') === 'in') return false;
            if (cellViewS === cellViewT) return false;
            return magnetT && magnetT.getAttribute('port-group') === 'in';
        },
        validateMagnet: function (cellView, magnet) {
            return magnet.getAttribute('magnet') !== 'passive';
        },
        snapLinks: {radius: 75}
    });
    var loaded_graph = $('#id_steps_graph').val();
    if (loaded_graph) {
        graph.fromJSON(JSON.parse(loaded_graph))
    }
    $('.add-step-type').on('click', function (e) {
        var step_name = $(this).attr('data-name');
        var step_color = $(this).attr('data-color');
        var step_icon = $(this).attr('data-icon');
        create_element(40, 40, step_color, step_name, 'white');
        e.preventDefault();
    });

    joint.shapes.devs.EreborModel = joint.shapes.devs.Model.extend({
        step_type: '',
    });

    function create_element(start_x, start_y, fill_color, label_text, label_color) {
        maxId++;
        var el = new joint.shapes.devs.EreborModel({
            step_type: label_text,
            step_id: maxId,
            position: {x: start_x, y: start_y},
            size: {width: 60, height: 60},
            inPorts: ['in'],
            outPorts: ['out'],
            ports: {
                groups: {
                    'in': {
                        attrs: {
                            '.port-body': {
                                fill: '#16A085',
                                magnet: 'passive'
                            }
                        }
                    },
                    'out': {
                        attrs: {
                            '.port-body': {
                                fill: '#E74C3C'
                            }
                        }
                    }
                }
            },
            attrs: {
                '.label': {text: label_text, 'ref-x': .5, 'ref-y': .2},
                rect: {fill: fill_color}
            }
        });
        graph.addCell(el);
    }


    paper.on('cell:pointerdown',
        function (cellView, evt, x, y) {
            // alert('cell view ' + cellView.model.id + ' was clicked');
            // alert('cell view ' + cellView.model.attr('data-name') + ' was clicked');
        });

    paper.on('element:pointerdblclick', function (cellView) {
        if (confirm("delete step?"))
            cellView.model.remove();
    });
    var attrValues = [];

    paper.on('cell:pointerclick', function (cellView) {
        $('#save-attr-msg').hide();
        var url = attr_list
            .replace('NaN4', cellView.model.attributes.step_type)
            .replace('NaN3', cellView.model.attributes.id)
            .replace('NaN2', $(location).attr('href').split("/")[6])
            .replace('NaN', pipeline_id);
        $.get(url, function (data) {
            debugger;
            $('#attrs_from').html('');
            $('#step_id').val(cellView.model.attributes.step_id);
            $('#step_type').val(cellView.model.attributes.step_type);
            processed_attrs = [];
            $.each(data.data, function (index, value) {
                var model = {
                    attr_name: value.name,
                    input_id: value.name,
                    input_val: value.value,
                    required: value.is_require
                };
                switch (value.data_type) {
                    case 1:
                    case 3:
                    case 4:
                    case 5:
                    case 6:
                    case 7:
                    case 11:
                        var input;
                        if (value.is_multiple === true) {
                            if (processed_attrs.find(m => m == value.name)) return true;

                            var same_records = data.data.filter(x => x.name == value.name)
                            if (same_records && same_records.length > 1) {
                                var final_val = "";
                                same_records.forEach(function (item, index) {
                                    processed_attrs.push(item.name);
                                    final_val = final_val + "\r\n" + item.value;
                                });
                                model.input_val = final_val;
                            }
                            input = components.textarea;
                        }
                        else {
                            input = components.textbox;
                        }
                        var output = Mustache.render(input, model);
                        $('#attrs_from').append(output);
                        break;
                    case 2:
                        var output = Mustache.render(components.checkbox, model);
                        $('#attrs_from').append(output);
                        break;
                    default:
                }
            });
            applyCheckboxStyle();
            enable_required();
            load_attrs_data(cellView.model.attributes.step_id)
        });

    });

    $('#save-attr').click(function () {
        debugger;
        $('#attr_container').addClass('blr');
        var step_id = $('#step_id').val();
        var step_type = $('#step_type').val();
        if ($("#attrs_from").valid()) {
            if (!step_id && !step_type) {
                alert("error in loading step info!! please try adding this step again.");
            }
            else {
                var form_vals = $('#attrs_from').serializeArray()//serialize(document.getElementById("attrs_from"));
                var newFormValues = {
                    step: step_id,
                    step_type: step_type,
                    data: form_vals
                }
                var greped_data = $.grep(attrValues, function (e) {
                    return e.step == step_id;
                }, true);
                attrValues = greped_data;
                attrValues.push(newFormValues);
                $('#save-attr-msg')
                    .text('Saved')
                    .addClass('validation-valid-label')
                    .removeClass('validation-error-label')
                    .show()
            }
        }
        else {
            $('#save-attr-msg')
                .text('Error')
                .addClass('validation-error-label')
                .removeClass('validation-valid-label')
                .show()
        }

        $('#attr_container').removeClass('blr');

    });
    $('#save').click(function () {
        debugger;
        var res = JSON.stringify(graph);
        $('#id_steps_graph').val(res);
        var res = JSON.stringify(attrValues);
        $('#steps_attrs').val(res)
    });

    function serialize(form) {
        if (!form || form.nodeName !== "FORM") {
            return;
        }
        var i, j, q = [];
        for (i = form.elements.length - 1; i >= 0; i = i - 1) {
            if (form.elements[i].name === "") {
                continue;
            }
            switch (form.elements[i].nodeName) {
                case 'INPUT':
                    switch (form.elements[i].type) {
                        case 'text':
                        case 'hidden':
                        case 'password':
                        case 'button':
                        case 'reset':
                        case 'submit':
                            q.push({[form.elements[i].name]: encodeURIComponent(form.elements[i].value)});
                            break;
                        case 'checkbox':
                        case 'radio':
                            if (form.elements[i].checked) {
                                q.push({[form.elements[i].name]: encodeURIComponent(form.elements[i].value)});
                            }
                            break;
                    }
                    break;
                case 'file':
                    break;
                case 'TEXTAREA':
                    q.push({[form.elements[i].name]: encodeURIComponent(form.elements[i].value)});
                    break;
                case 'SELECT':
                    switch (form.elements[i].type) {
                        case 'select-one':
                            q.push({[form.elements[i].name]: encodeURIComponent(form.elements[i].value)});
                            break;
                        case 'select-multiple':
                            for (j = form.elements[i].options.length - 1; j >= 0; j = j - 1) {
                                if (form.elements[i].options[j].selected) {
                                    q.push({[form.elements[i].name]: encodeURIComponent(form.elements[i].options[j].value)});
                                }
                            }
                            break;
                    }
                    break;
                case 'BUTTON':
                    switch (form.elements[i].type) {
                        case 'reset':
                        case 'submit':
                        case 'button':
                            q.push({[form.elements[i].name]: encodeURIComponent(form.elements[i].value)});
                            break;
                    }
                    break;
            }
        }
        return q;
    }

    function load_attrs_data(id) {
        debugger;
        var saved_attrs = attrValues.find(x => x.step == id);
        if (saved_attrs) {
            var form = document.getElementById("attrs_from");
            var x, i, j, q = [];
            for (i = form.elements.length - 1; i >= 0; i = i - 1) {
                if (form.elements[i].name === "") {
                    continue;
                }
                switch (form.elements[i].nodeName) {
                    case 'INPUT':
                        switch (form.elements[i].type) {
                            case 'text':
                            case 'hidden':
                            case 'password':
                            case 'button':
                            case 'reset':
                            case 'submit':
                                for (x = 0; x < saved_attrs.data.length; x++) {
                                    if (saved_attrs.data[x].name === form.elements[i].name)
                                        form.elements[i].value = saved_attrs.data[x].value;
                                }

                                break;
                            case 'checkbox':
                            case 'radio':
                                for (x = 0; x < saved_attrs.data.length; x++) {
                                    if (saved_attrs.data[x].name === form.elements[i].name)
                                        if (saved_attrs.data[x].value && (saved_attrs.data[x].value == "on" || saved_attrs.data[x].value == true)) {
                                            form.elements[i].checked = true;
                                            applyCheckboxStyle();
                                        } else if (saved_attrs.data[x].value == false) {
                                            form.elements[i].checked = false;
                                            applyCheckboxStyle();
                                        }
                                }
                                break;
                        }
                        break;
                    case 'file':
                        break;
                    case 'TEXTAREA':
                        for (x = 0; x < saved_attrs.data.length; x++) {
                            if (saved_attrs.data[x].name === form.elements[i].name)
                                form.elements[i].value = saved_attrs.data[x].value;
                        }
                        break;
                    case 'SELECT':
                        switch (form.elements[i].type) {
                            case 'select-one':
                                q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                                break;
                            case 'select-multiple':
                                for (j = form.elements[i].options.length - 1; j >= 0; j = j - 1) {
                                    if (form.elements[i].options[j].selected) {
                                        q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].options[j].value));
                                    }
                                }
                                break;
                        }
                        break;
                    case 'BUTTON':
                        switch (form.elements[i].type) {
                            case 'reset':
                            case 'submit':
                            case 'button':
                                q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                                break;
                        }
                        break;
                }
            }
        }

    }

    function applyCheckboxStyle() {
        $(".styled").uniform({
            radioClass: 'choice'
        });
    }
});