var components = {
    'textbox': '<div class="form-group">\n' +
    '    <label class="col-md-3 control-label">{{ attr_name }}:</label>\n' +
    '    <div class="col-md-9">\n' +
    '        <input id="{{input_id}}" value="{{{input_val}}}" type="text" name="{{input_id}}"  {{#required}} required="required" data-msg="Please' +
    ' fill this field" {{/required}} class="form-control" />\n' +
    // '        <span class="help-block">{{error}}</span>\n' +
    '    </div>\n' +
    '</div>',
    'textarea': '<div class="form-group">\n' +
    '    <label class="col-md-3 control-label">{{ attr_name }}:</label>\n' +
    '    <div class="col-md-9">\n' +
    '        <textarea id="{{input_id}}" rows="3" cols="5"  {{#required}} required="required" data-msg="Please fill this' +
    ' field" {{/required}}  name="{{input_id}}" class="form-control" >{{{input_val}}}</textarea>\n' +
    '        <label id="{{input_id}}-error" class="validation-error-label" for="{{input_id}}"></label>\n' +
    '    </div>\n' +
    '</div>',
    'checkbox': '<div class="form-group">\n' +
    '    <label class="col-md-6 control-label">{{ attr_name }}:</label>\n' +
    '    <div class="col-md-6">\n' +
    '        <div class="checkbox">\n' +
    '            <label><input type="checkbox" id="{{input_id}}" {{#required}} required="required" data-msg="Please check" {{/required}}' +
    ' name="{{input_id}}" class="styled" {{#input_val}} checked' +
    ' {{/input_val}}' +
    ' /><label>\n' +
    '        </div>\n' +
    '    </div>\n' +
    '</div>'

}