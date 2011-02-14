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
                //window.location = data.url;
                location.reload()
                // location.replace(location.href.replace(/\?.*$/, '') + '?' + Math.random());
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
                    $(this).parent().remove()
                }
            })
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
            $.ajax(metadata_url,
                   {
                       type: 'POST',
                       data: {
                           'value' : $('#enter-metadata-value-textarea').val()
                       },
                       success: function(){
                           window.location = "/node/" + nodeid;
                       }
                   })
        }
    );

    $("#edit-metadata-span").click(
        function(evt){
            window.location = window.location + "/metadata/"
                + $(this).attr("data-key") + "?edit";
        });

})
  