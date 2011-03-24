$(document).ready(function(){
    $('#create-node-div').click(function(){
        $.ajax('/node/' + nodeid,{
            type: 'PUT',
            data: {
                //reference global variable
                id: nodeid
            },
            dataType: "json",
            success: function(data, textStatus){
                location.reload();
            }
        })
    });

    $('#add-node-button').click(
        function(evt){
            nodeid = $('#add-node-input').val();
            node_url = '/node/' + nodeid;
            $.ajax(node_url, {
                type: 'PUT',
                data: {
                    id: nodeid
                },
                success: function(){
                    window.location = node_url;
                }
            })
        });

    $('.remove-node-span').click(
        function(evt){
            var nodeid = $(this).attr('data-node');
            $.ajax('/node/' + nodeid, {
                type: 'DELETE',
                data: {},
                dataType: "json",
                context: this,
                success: function(data){
                    var nodeid = $(this).attr('data-node');
                    $(this).parent().parent().find('[data-node="'+nodeid+'"]').parent().remove()
                }
            })
        }
    );

    $('.rename-node-span').click(
        function(evt){
            if($(this).attr('data-live')){
                var nodeid = $(this).attr('data-node');
                var newid = $('#rename-node-input').val();
                $.ajax('/node/' + nodeid, {
                    type: 'POST',
                    data: {
                        'rename' : newid
                    },
                    dataType: "json",
                    context: this,
                    success: function(data){
                        window.location = "/node/" + newid;
                    }
                })
            } else {
                rename_node_input = $('<input />');
                rename_node_input.attr('id','rename-node-input');
                $(this).before(rename_node_input);
                $(this).attr('data-live', true)
            }
        }
    );

    $('.remove-edge-span').click(
        function(evt){
            edge_url = '/edge/'+ nodeid + '/'
                + $(this).attr('data-node');
            $.ajax(edge_url, {
                type: 'DELETE',
                data: {},
                dataType: "json",
                context: this,
                success: function(data){
                    $(this).parent().remove()
                }
            })
        }
    );

    $('#add-edge-button').click(
        function(evt){
            edge_url = '/edge/'+ nodeid + '/'
                + $('#to-node-input').val();
            $.ajax(edge_url, {
                type: 'PUT',
                data: {},
                success: function(){
                    location.reload();
                }
            })
        });


    $('#add-metadata-key-button').click(
        function(evt){
            window.location = window.location + "/metadata/"
                + $("#metadata-key-input").val();
        });

    $('#enter-metadata-value-button').click(
        function(evt){
            metadata_url = "/node/" + nodeid + "/metadata/" + key;

            mval = function(){
                if(mval_type == "string"){
                    return '"' + $('#metadata-input-string').val() + '"';
                } else if (mval_type == "boolean"){
                    return $('#metadata-input-boolean').attr("checked");
                }
            }();

            $.ajax(metadata_url,
                   {
                       type: 'POST',
                       data: {
                           'value' : mval
                       },
                       success: function(){
                           window.location = "/node/" + nodeid;
                       }
                   })
        }
    );

    $(".edit-metadata-span").click(
        function(evt){
            window.location = window.location + "/metadata/"
                + $(this).attr("data-key") + "?edit";
        });

    $(".remove-metadata-span").click(
        function(evt){
            metadata_url = window.location + "/metadata/"
                + $(this).attr("data-key");
            $.ajax(metadata_url, {
                type: 'DELETE',
                data: {},
                context: this,
                success: function(data){
                    $(this).parent().parent().parent().remove()
                }
            })
        });
})
  