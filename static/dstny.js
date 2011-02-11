$(document).ready(function(){
    $('#create-node-div').click(function(){
        $.ajax('/node/' + nodeid,{
            type: 'PUT',
            data: {
                //reference global variable
                id: nodeid
            },
            dataType: "json",
            context: window,
            success: function(data, textStatus){
                //window.location = data.url;
                location.reload()
                // location.replace(location.href.replace(/\?.*$/, '') + '?' + Math.random());
            }
        })
    })
})
  