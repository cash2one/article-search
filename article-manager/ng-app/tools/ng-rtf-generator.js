// generate ng form from RTF options metadata
var log_func = console.log;

var RTFtype2NGtype = {
    'integer' : 'number',
    'string' : 'text',
    'choice' : 'select',
    'datetime' : 'time',
    'field' : 'text'
};
//<select ng-options="item.subItem as item.label for item in values track by item.id" ng-model="selected"></select>

function general_parse(mainModelName, name, inputType, property) {
    var dump_str = '<div class="form-group"> \
	<label class="col-sm-2 control-label" for="'+name+'">'+property.label+'</label> \
    	<div class="col-sm-10"> \
        	<input class="form-control" type="'+inputType+'" name="'+name+'" id="'+name+'" ng-model="'+mainModelName+'.'+name+'" ng-required="'+property.required+'" placeholder="'+property.help_text+'" ng-readonly="'+property.read_only+'"></input> \
        </div> \
	</div>';
    return dump_str;
}

function parse_select(mainModelName, name, property) {
	if (property.choices) {
		var options_str = '';
		for (var i = 0; i < property.choices.length; i++) {
			options_str += '<option value="'+property.choices[i].value+'">'+property.choices[i].display_name+'</option>';
		}
		var dump_str = '<div class="form-group"> \
		<label class="col-sm-2 control-label" for="'+name+'">'+property.label+'</label> \
			<div class="col-sm-10"> \
		    	<select class="form-control" name="'+name+'" id="'+name+'" ng-model="'+mainModelName+'.'+name+'" ng-required="'+property.required+'" ng-readonly="'+property.read_only+'">'+options_str+'</select> \
		    </div> \
		</div>';
		return dump_str;
	}
	return general_parse(mainModelName, name, 'text', property);
}

function gen_from_property(mainModelName, name, property) {
    console.log("property : " + property);
    var res = null;
    // parse required fields
    switch(RTFtype2NGtype[property.type]) {
        case 'number':
            res = general_parse(mainModelName, name, 'number', property);
            break;
        case 'text':
            res = general_parse(mainModelName, name, 'text', property);
            break;
		case 'time':
			res = general_parse(mainModelName, name, 'time', property);
			break;
        case 'select':
            res = parse_select(mainModelName, name, property);
            break;
        default:
            // treat as text type by default
            res = general_parse(mainModelName, name, 'text', property);
    }
    return res;
}

function gen_from_action(mainModelName, name, action) {
    if (action) {
	    var res_form = [];
	    console.log("action name : " + name);
	    for (var property in action) {
			res_form.push(gen_from_property(mainModelName, property, action[property]));
	    }
	    return res_form.join();
    }
    console.log("[GenError] action is null");
    return null;
}

function ng_generate(mainModelName, rtf_metadata) {
    var res_forms = [];
    for (var action in rtf_metadata.actions) {
		console.log("action : "+action);
        res_forms.push(gen_from_action(mainModelName, action, rtf_metadata.actions[action]));
    }
    return res_forms;
}

test_data = {
    "name": "Composition List",
    "description": "",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "id": {
                "type": "integer",
                "required": false,
                "read_only": true,
                "label": "ID"
            },
            "title": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Title",
                "help_text": "作文标题",
                "max_length": 300
            },
            "json_tags": {
                "type": "field",
                "required": true,
                "read_only": false,
                "label": "Json tags"
            },
            "atype": {
                "type": "choice",
                "required": false,
                "read_only": false,
                "label": "Atype",
                "help_text": "作文体裁",
                "choices": [
                    {
                        "display_name": "记叙文",
                        "value": 1
                    },
                    {
                        "display_name": "议论文",
                        "value": 2
                    },
                    {
                        "display_name": "说明文",
                        "value": 3
                    },
                    {
                        "display_name": "散文",
                        "value": 4
                    },
                    {
                        "display_name": "诗歌",
                        "value": 5
                    },
                    {
                        "display_name": "杂文",
                        "value": 6
                    }
                ]
            },
            "grade": {
                "type": "choice",
                "required": false,
                "read_only": false,
                "label": "Grade",
                "help_text": "年级",
                "choices": [
                    {
                        "display_name": "一年级",
                        "value": 1
                    },
                    {
                        "display_name": "二年级",
                        "value": 2
                    },
                    {
                        "display_name": "三年级",
                        "value": 3
                    },
                    {
                        "display_name": "四年级",
                        "value": 4
                    },
                    {
                        "display_name": "五年级",
                        "value": 5
                    },
                    {
                        "display_name": "六年级",
                        "value": 6
                    },
                    {
                        "display_name": "七年级",
                        "value": 7
                    },
                    {
                        "display_name": "八年级",
                        "value": 8
                    },
                    {
                        "display_name": "九年级",
                        "value": 9
                    },
                    {
                        "display_name": "高一年级",
                        "value": 10
                    },
                    {
                        "display_name": "高二年级",
                        "value": 11
                    },
                    {
                        "display_name": "高三年级",
                        "value": 12
                    }
                ]
            },
            "number": {
                "type": "integer",
                "required": true,
                "read_only": false,
                "label": "Number",
                "help_text": "字数"
            },
            "content": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Content",
                "help_text": "正文"
            },
            "source": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Source",
                "help_text": "来源",
                "max_length": 200
            },
            "creator": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Creator"
            },
            "approver": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Approver"
            },
            "status": {
                "type": "choice",
                "required": false,
                "read_only": true,
                "label": "Status",
                "help_text": "作文状态"
            },
            "image": {
                "type": "image upload",
                "required": false,
                "read_only": true,
                "label": "Image"
            },
            "abstract": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Abstract",
                "help_text": "作文摘要",
                "max_length": 500
            },
            "beginning": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Beginning",
                "help_text": "作文开头"
            },
            "ending": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Ending",
                "help_text": "作文结尾"
            },
            "created": {
                "type": "datetime",
                "required": false,
                "read_only": true,
                "label": "Created",
                "help_text": "创建日期"
            },
            "modified": {
                "type": "datetime",
                "required": false,
                "read_only": true,
                "label": "Modified",
                "help_text": "修改日期"
            }
        }
    }
}

//var t = ng_generate('compositionEdit', test_data);
//console.log(t);

