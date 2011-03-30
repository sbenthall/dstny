function on_metadata_load(data){
    mval = data[key];
    
    if(typeof mval == 'string'){
        $("#metadata-input-string").val(mval);
        mval_type = 'string';
    } else if (typeof mval == 'boolean'){
        $("#metadata-input-boolean").attr("checked",mval)
        mval_type = 'boolean';
    }
    
    set_metadata_input_visibility();
    $("#metadata-type-radio-" + mval_type).attr("checked","true");
}

function set_metadata_input_visibility(){
    $(".metadata-input").each(function(){
        if($(this).attr("id") == "metadata-input-" + mval_type){
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

$(document).ready(function(){
    var metadata = $.get(
        "/node/" + nodeid + "/metadata", 
        on_metadata_load,
        "json"
    )
    
    $("input:radio[name=metadata-type-radio]").click(function(){
        mval_type = $("input:radio[name=metadata-type-radio]:checked").val();
        set_metadata_input_visibility();
    });
    
})

