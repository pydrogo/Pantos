

Date.prototype.toPersianDate = function () {
    var object = new persianDate(this);
    object.formatPersian = false;
    return object;
};

var Asiatech = {
    maps: {},
};

Asiatech.maps.dataType = {
    1:{name: 'INTEGER', color: 'success-400'},
    2:{name: 'BOOLEAN', color: 'success-400'},
    3:{name: 'LONG', color: 'success-400'},
    4:{name: 'FLOAT', color: 'success-400'},
    5:{name: 'DOUBLE', color: 'success-400'},
    6:{name: 'BYTE', color: 'success-400'},
    7:{name: 'STRING', color: 'success-400'},
    8:{name: 'ARRAY', color: 'success-400'},
    9:{name: 'DATE', color: 'success-400'},
    10:{name: 'OBJECT', color: 'success-400'},
    11:{name: 'NUMBER', color: 'success-400'},
};
Asiatech.maps.conditionSource = {
    1:{name: 'MODIFIER', color: 'success-400'},
    2:{name: 'PIPELINE', color: 'success-400'}
};
Asiatech.maps.httpMethodInfo = {
    1:{name: 'GET', color: 'success-400'},
    2:{name: 'HEAD', color: 'success-400'},
    3:{name: 'POST', color: 'blue'},
    4:{name: 'PUT', color: 'blue'},
    5:{name: 'DELETE', color: 'danger'},
    6:{name: 'CONNECT', color: 'success-400'},
    7:{name: 'OPTIONS', color: 'success-400'},
    8:{name: 'TRACE', color: 'success-400'},
    9:{name: 'PATCH', color: 'success-400'}
};
Asiatech.maps.methodAttributeType = {
    1:{name: 'QUERY', color: 'success-400'},
    2:{name: 'REQUEST', color: 'success-400'},
    3:{name: 'BODY', color: 'success-400'},
    4:{name: 'RESPONSE', color: 'success-400'},
    5:{name: 'AUTO', color: 'success-400'}
};
Asiatech.maps.operatorType = {
    1:{name: 'NOT_EQUAL', color: 'success-400'},
    2:{name: 'GT', color: 'success-400'},
    3:{name: 'GTE', color: 'success-400'},
    4:{name: 'LT', color: 'success-400'},
    5:{name: 'LTE', color: 'success-400'},
    6:{name: 'CONTAINS', color: 'success-400'},
    7:{name: 'NOT_CONTAINS', color: 'success-400'},
    8:{name: 'IN', color: 'success-400'},
    9:{name: 'NOT_IN', color: 'success-400'},
    10:{name: 'REGEX', color: 'success-400'},
    11:{name: 'IP_MATCH', color: 'success-400'},
    12:{name: 'EQUAL', color: 'success-400'}
};
Asiatech.maps.serviceType = {
    1:{name: 'SOAP', color: 'success-400'},
    2:{name: 'XML_RPC', color: 'success-400'},
    3:{name: 'JSON_RPC', color: 'success-400'},
    4:{name: 'RESTFULL', color: 'success-400'},
    5:{name: 'OTHER', color: 'success-400'},
}
Asiatech.maps.permissionType = {
    1:{name: 'Scope', color: 'success-400'},
    2:{name: 'Method', color: 'success-400'},
    3:{name: 'Message_context', color: 'success-400'},
}

$(document).ready(function () {
    // Styled checkboxes, radios
    CheckboxStyle();
});

function CheckboxStyle(){
    $(".styled").uniform({
        radioClass: 'choice'
    });
}