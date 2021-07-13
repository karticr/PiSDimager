status_elem = document.getElementById("stat_label")
output_elem = document.getElementById("term_out")

$( document ).ready(function() {
    populatePage();

    StatUpdater();
    setInterval(function(){
        StatUpdater()
    }, 1000);

    $("#sd_select").change(function(){
        val = $("#sd_select").val()
        data = {
            "key" : "input",
            "value": val
        }
        updateConf(data)
    })

    $('#zip_img').on('change', function() {
        var val = this.checked
        data = {
            "key" : "zip",
            "value": val
        }
        updateConf(data)
    });

    $('#reset_img').on('change', function() {
        var val = this.checked 
        data = {
            "key" : "reset",
            "value": val
        }
        updateConf(data)
    });

    $("#make_img").on('click', function(){
        MakeImage()
    })

});

function MakeImage(){
    img_name = $('#img_name').val();

    if(img_name == ""){
        msg = "image name is empty"
        alert(msg)
        if (confirm('Are you sure you want to continue with default name')) {
            PostRqMakeImage("empty")
          } else {
            console.log('cancel');
        }
    }
    else{
        if (confirm('Are you sure you want to make the image with selected config')) {
            PostRqMakeImage(img_name)
          } else {

            console.log('cancel');
          }
    }
}

function PostRqMakeImage(img_name){
    data = {"img_name":img_name}
    $.ajax({
        url: "/api/make_img",
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify(data),
        success: function(res) {
            console.log(res)
            $("#term_out").val("");
        }
    });

}

function populatePage(){
    sd_card = server_config['input']
    output  = server_config['output']
    reset   = server_config['reset']
    zip     = server_config['zip']

    $("#sd_select").val(sd_card);
    $("#output_select").val(output);
    $("#zip_img").prop("checked", zip);
    $("#reset_img").prop("checked", reset);
}

function StatUpdater(){
    $.ajax({
        url: "/api/server_stats",
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        success: function(res) {
            
            stat = res['status']
            prog = res['prog']
            old_stat_val = $("#stat_label").val();
            old_term_full= $("#term_out").val()
            old_term_last= old_term_full.substr(old_term_full.lastIndexOf("\n")+1);
            
            last_line = old_term_full.split("\n")
            last_line = last_line[last_line.length - 2]
 
            if (typeof(last_line) == "undefined")
                last_line = "test"

            if(old_stat_val !== stat)
                $("#stat_label").val(stat)
               
            if(prog != "" ){
                $("#term_out").val(old_term_full+ prog).scrollBottom()
                // console.log(prog)
            }
            

        }
    });
}

function updateConf(data){
    $.ajax({
        url: "/api/update_conf",
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify(data),
        success: function(res) {
            console.log(res)
        }
    });
}

$.fn.scrollBottom = function() {
    return $(this).scrollTop($(this)[0].scrollHeight);
};