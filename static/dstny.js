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
                data: {

                },
                dataType: "json",
                context: this,
                success: function(data){
                    $(this).parent().remove()
                }
            })
        }
    );


})
  