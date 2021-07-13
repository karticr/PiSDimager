status_elem = document.getElementById("stat_label")
output_elem = document.getElementById("term_out")

$( document ).ready(function() {
    console.log(server_config)

    populatePage();

    StatUpdater();
    setInterval(function(){
        StatUpdater()
    }, 1000);

    $("#sd_select").change(function(){
        console.log($("#sd_select").val())
    })
});

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
        url: "/msgs",
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
                console.log(prog)
            }
            

        }
    });
}

$.fn.scrollBottom = function() {
    return $(this).scrollTop($(this)[0].scrollHeight);
};